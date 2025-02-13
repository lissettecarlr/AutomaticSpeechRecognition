from fastapi import APIRouter, Request, HTTPException, Header
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from response import OkResponse

router = APIRouter()

@router.get("/test")
def test():
    return OkResponse(msg="test ok")