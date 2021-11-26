from typing import Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from database.conn import db
from utils.token import AuthHandler
from database.schema import TireInfoRegister
from service.tire_service import tire_info_register, get_user_tire_info
from service.auth_service import (
    is_admin,
    is_id_exist, 
    update_user, 
    is_username_exist, 
    is_id_name_same
)

router = APIRouter(prefix='/tire')


@router.post("/register-info")
async def user_tire_info(tire_info: TireInfoRegister, id=Depends(AuthHandler().auth_wrapper), session: Session = Depends(db.session)):
    if not await is_id_exist(id):
        return JSONResponse(status_code=400, content=dict(msg="NO USER EXIST"))
    for info in dict(tire_info)['item']:
        if not await is_username_exist(info.id):
            return JSONResponse(status_code=400, content=dict(msg=f"NOT REGISTERED USER: {info.id}"))
        update_user(info.id, info.trimId, session)
    
    tire_info_register(dict(tire_info), session)
    
    return JSONResponse(status_code=201, content=dict(msg="SUCCESS"))


@router.get("/tire-info/user")
async def user_tire_info(name: Optional[str], id=Depends(AuthHandler().auth_wrapper), session: Session = Depends(db.session)):
    if not await is_username_exist(name):
        return JSONResponse(status_code=400, content=dict(msg="NO USER EXIST"))
    if not await is_admin(id):
        if not await is_id_name_same(name, id):
            return JSONResponse(status_code=400, content=dict(msg="NOT AUTHORIZED"))
    
    tire_info_data = get_user_tire_info(name, session)

    return JSONResponse(status_code=200, content=tire_info_data)
