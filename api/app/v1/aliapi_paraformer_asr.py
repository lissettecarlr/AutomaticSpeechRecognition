from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.responses import StreamingResponse
import os
import sys
from typing import List
import logging
import uuid
import json
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from response import OkResponse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','..')))
from kuonasr import AliyunParaformerASR

router = APIRouter()

# 初始化ASR实例，从环境变量获取api_key
api_key = os.getenv('ALIYUN_API_KEY')
asr = AliyunParaformerASR(config={"api-key": api_key})


from pydantic import BaseModel
class AudioItem(BaseModel):
    index: int    # 音频项的序号，用于保持顺序
    tts: str      # 音频文件的URL地址

class RecognitionResult(BaseModel):
    index: int    # 对应请求的序号
    tts: str      # 原始音频URL
    text: str     # 识别出的文本结果



@router.get("/test")
def test():
    return OkResponse(msg="test ok")

@router.post("/asr/recognize")
async def recognize(audio_items: List[AudioItem]):
    """
    批量语音识别接口
    支持同时发送多个音频URL，按顺序返回识别结果
    
    Args:
        audio_items: 包含音频URL的列表，每项包含index和tts(URL)
    Returns:
        返回OkResponse，data中包含按index排序的识别结果列表
    """
    request_id = str(uuid.uuid4())
    try: 
        logging.info(f"[{request_id}] Received recognition request with {len(audio_items)} audio items")
        logging.debug(f"[{request_id}] Request details: {audio_items}")
        # 提取所有音频URL
        audio_urls = [item.tts for item in audio_items]

        # 获取识别结果
        start_time = time.time()
        raw_results = await asr.async_recognize(audio_urls)
        end_time = time.time()
        logging.info(f"[{request_id}] Recognition completed in {end_time - start_time:.2f} seconds")
        logging.debug(f"[{request_id}] Raw recognition results: {raw_results}")

        # 构建带index的结果
        recognition_results = []
        for result in raw_results:
            rec_audio_url = result["result"]["file_url"]
            text = ""
            for transcript in result['result']["transcripts"]:
                text += transcript["text"]                
            for item in audio_items:
                if item.tts == rec_audio_url:
                    logging.info(f"[{request_id}] Processed audio {rec_audio_url} (index: {item.index}): {text}")
                    recognition_results.append(RecognitionResult(
                        index=item.index,
                        tts=item.tts,
                        text=text
                    ))

        # 对recognition_results进行排序
        recognition_results.sort(key=lambda x: x.index)
        logging.info(f"[{request_id}] Recognition completed successfully")
        response = OkResponse(data=recognition_results)
        return response.create_response(headers={"X-Request-ID": request_id})
    except Exception as e:
        logging.error(f"[{request_id}] Recognition failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=str(e), 
            headers={"X-Request-ID": request_id}
        )

@router.post("/asr/recognize_stream")
async def recognize_stream(audio_items: List[AudioItem]):
    """
    流式语音识别接口
    使用SSE(Server-Sent Events)协议，实时返回每个音频的识别结果
    """
    async def event_generator():
        request_id = str(uuid.uuid4())
        last_heartbeat = time.time()
        HEARTBEAT_INTERVAL = 15  # 15秒发送一次心跳

        try:
            # 发送初始连接消息
            yield f"id: {request_id}\nevent: connect\ndata: {json.dumps({'status': 'connected'})}\nretry: 3000\n\n"
            
            logging.info(f"[{request_id}] Received streaming recognition request with {len(audio_items)} audio items")
            audio_urls = [item.tts for item in audio_items]
            
            async for result in asr.async_recognize_stream(audio_urls):
                # 检查是否需要发送心跳
                current_time = time.time()
                if current_time - last_heartbeat >= HEARTBEAT_INTERVAL:
                    yield f"id: {request_id}\nevent: heartbeat\ndata: {json.dumps({'timestamp': current_time})}\n\n"
                    last_heartbeat = current_time

                if result["status"] == "SUCCEEDED":
                    rec_audio_url = result["result"]["file_url"]
                    text = "".join(t["text"] for t in result['result']["transcripts"])
                    
                    for item in audio_items:
                        if item.tts == rec_audio_url:
                            recognition_result = RecognitionResult(
                                index=item.index,
                                tts=item.tts,
                                text=text
                            )
                            response = OkResponse(data=recognition_result)
                            yield f"id: {request_id}\nevent: recognition\ndata: {response.model_dump_json()}\n\n"
                            
                elif result["status"] == "FAILED":
                    # 处理单个音频识别失败的情况
                    error_data = {
                        "error": "Recognition failed",
                        "file_url": result.get("file_url"),
                        "details": result.get("error", "Unknown error")
                    }
                    yield f"id: {request_id}\nevent: error\ndata: {json.dumps(error_data)}\n\n"

            # 发送结束消息
            yield f"id: {request_id}\nevent: complete\ndata: {json.dumps({'message': 'All audio files processed'})}\n\n"
                            
        except Exception as e:
            logging.error(f"[{request_id}] Streaming recognition failed: {str(e)}", exc_info=True)
            error_data = {
                "error": str(e),
                "type": type(e).__name__
            }
            yield f"id: {request_id}\nevent: error\ndata: {json.dumps(error_data)}\n\n"
            
    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        }
    )