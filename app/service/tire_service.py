import requests
from common.consts import BASE_DIR
from dao.tire_dao import create_tire_info, user_tire_info_dao


def tire_info_register(tire_info: dict, session):
    for info in tire_info['item']:
        url_parser([info.id, f"{BASE_DIR}/{info.trimId}"], session)


def url_parser(url, session):
    req = requests.get(url[1]).json()
    user_name = url[0]
    front_tire_info = req['spec']['driving']['frontTire']['value']
    rear_tire_info = req['spec']['driving']['rearTire']['value']
    
    if not front_tire_info == '':
        create_tire_info(user_name, front_tire_info, 1, session)
    if not rear_tire_info == '':
        create_tire_info(user_name, rear_tire_info, 2, session)
    

def get_user_tire_info(name, session):
    tire_infos = user_tire_info_dao(name, session)
    
    tire_info_list=[{
        "user_id": tire_info[0],
        "tire_position": tire_info[1],
        "tire_rim_inch": tire_info[2],
        "tire_wheel_size": tire_info[3],
        "tire_stucture": tire_info[4],
        "tire_aspect_ratio": tire_info[5],
        "tire_updated_at": tire_info[6].strftime("%Y.%m.%d"),
    }for tire_info in tire_infos]

    return tire_info_list