import re
import bcrypt
from enum import Enum

from database.schema import UserRegister, Login
from database.models import User
from utils.token import AuthHandler


authhandler = AuthHandler()


class UserRole(Enum):
    admin = 1
    client = 2


async def is_username_exist(user_id: str):
    get_user_id = User.get(user_id=user_id)
    if get_user_id:
        return True
    return False


async def is_id_exist(id: int):
    get_id = User.get(id=id)
    if get_id:
        return True
    return False

async def is_admin(id: int):
    user = User.get(id=id)
    if user.role_id == UserRole.admin.value:
        return True
    return False

async def is_id_name_same(name, id):
    user = User.get(id=id)
    if user.user_id == name:
        return True
    return False

def password_validation_check(password: str):
    if re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,20}$',password):
        return True 
    return False


def create_user(info: UserRegister, session):
    hash_pw = bcrypt.hashpw(info.password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
    
    if info.role == UserRole.admin.name:
        User.create(session, auto_commit=True, password=hash_pw, user_id=info.user_id, role_id=UserRole.admin.value)
    else:
        User.create(session, auto_commit=True, password=hash_pw, user_id=info.user_id, role_id=UserRole.client.value)


def update_user(user_id, trimId, session):
    user = session.query(User).filter(user_id == user_id).first()
    user.trim_id = trimId
    session.commit()
    

async def check_user_info(info: Login, session):
    if not await is_username_exist(info.user_id):
        return False
    user = User.get(user_id=info.user_id)
    pw_check = bcrypt.checkpw(info.password.encode('utf-8'), user.password.encode('utf-8'))
    if user and pw_check:
        token = authhandler.encode_token(user.id)
        return token
    return False


def check_token(id):
    try:
        user = User.get(id=id)
    except:
        return False
    
    if not (user.role_id == UserRole.admin.value):
        return False
    
    return True
    
