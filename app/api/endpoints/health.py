from typing import Optional, Annotated
from fastapi import APIRouter

router = APIRouter()

@router.get('/ping')
def ping():
    return {'ping': 'pong'}