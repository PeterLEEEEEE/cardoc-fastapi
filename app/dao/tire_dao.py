import re
from fastapi import HTTPException
from database.models import User, Tire, Position



def create_tire_info(user_name, tire_info, position_id, session):
    try:
        structures = ['ZR', 'R', 'D']
        structure = ''
        if re.match('[^0-9]',tire_info[0]):
            tire_info = tire_info[1:]
        
        for s in structures:
            if s in tire_info:
                structure = s
                break

        info = tire_info.replace(structure, '/')
        rim_inch, aspect_ratio, wheel_size = info.split('/')
        
        user = User.get(user_id=user_name)
        Tire.create(
            session, auto_commit=True,
            structure=structure,
            rim_inch=int(rim_inch),
            aspect_ratio=int(aspect_ratio),
            wheel_size=int(wheel_size),
            position_id=position_id,
            user_id=user.id
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="WRONG TIRE DATA FORMAT")


def user_tire_info_dao(name, session):
    try:
        user = User.get(user_id=name)
        data = session.query(
            User.user_id,
            Position.name,
            Tire.rim_inch, 
            Tire.wheel_size,
            Tire.structure, 
            Tire.aspect_ratio,
            Tire.updated_at 
            )\
            .join(User, User.id == Tire.user_id) \
            .join(Position, Tire.position_id == Position.id) \
            .filter(User.id==user.id)
    except:
        raise HTTPException(status_code=400, detail="CANNOT FIND DATA")
    
    return data