from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union, List, Any
from typing import Union, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')


# class OkResponse(BaseModel, Generic[T]):
#     code: int = 200
#     msg: str = "ok"
#     data: T | List[T] | None = None

class OkResponse(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "ok"
    data: T | List[T] | None = None

    def create_response(self, headers: dict = None) -> Response:
        return JSONResponse(
            content=self.model_dump(),
            headers=headers
        )

class ServerErrorResponse(BaseModel):
    code: int = 500
    msg: str = "server error"
    data: Union[list, dict, str, None]


class BadRequestResponse(BaseModel):
    code: int = 400
    msg: str = "bad request"
    data: Union[list, dict, str, None]
