from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from database.conn import db
from database.schema import UserRegister, Login
from service.auth_service import (
    create_user, 
    check_user_info, 
    is_username_exist, 
    password_validation_check, 
)

router = APIRouter(prefix='/auth')


@router.post("/signup")
async def signup(reg_info: UserRegister, session: Session = Depends(db.session)):
    if not reg_info.user_id or not reg_info.password:
        return JSONResponse(status_code=400, content=dict(msg="ID AND PASSWORD REQUIRED"))
    if await is_username_exist(reg_info.user_id):
        return JSONResponse(status_code=400, content=dict(msg="ID ALREADY EXISTS"))
    if not password_validation_check(reg_info.password):
        return JSONResponse(status_code=400, content=dict(msg="WRONG PASSWORD FORMAT"))
    
    create_user(reg_info, session)

    return JSONResponse(status_code=201, content=dict(msg="SUCCESSFULLY REGISTERED"))


@router.post("/login")
async def user_login(user_info: Login, session: Session = Depends(db.session)):
    if not user_info.user_id or not user_info.password:
        return JSONResponse(status_code=400, content=dict(msg="ID AND PASSWORD REQUIRED"))
    token = await check_user_info(user_info, session)
    if not token:    
        return JSONResponse(status_code=400, content=dict(msg="WRONG ID OR PASSWORD"))
    
    return JSONResponse(status_code=200, content=dict(Authorization=token, token_type="bearer"))
