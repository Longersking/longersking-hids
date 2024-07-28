from fastapi import APIRouter, status
from ..controllers import user_controller
router = APIRouter()

# @router.post("/addUser", status_code=status.HTTP_201_CREATED)
# async def add():
