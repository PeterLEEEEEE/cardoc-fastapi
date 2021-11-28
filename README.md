# WANTED X CARDOC Pre-Onboarding Course

Cardoc 개인 기업 과제 #7

<br><br>

## 📚 Stack 📚 
<br>
<p>
Back-End : <img src="https://img.shields.io/badge/Python 3.9-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img alt="Python" src = "https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Mysql-0064a5?style=for-the-badge&logo=Mysql&logoColor=white"/>&nbsp;
</p>

<p>
Tool : <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/SWAGGER-5B8C04?style=for-the-badge&logo=Swagger&logoColor=white"/>&nbsp;
</p>

<br><br>


## 배포 주소(Naver Cloud 배포)
- 주소(BASE): http://101.101.209.173:8000
- API 테스트: http://101.101.209.173:8000/docs

<br><br>

## 과제 안내

1. 사용자 생성 API(회원가입, 로그인)
2. 사용자가 소유한 타이어 정보를 저장하는 API
3. 사용자가 소유한 타이어 정보 조회 API

<br><br>


## ERD

![image](https://user-images.githubusercontent.com/52132160/143681939-b521fea1-c765-483e-8edc-b4d8327ead70.png)



<br><br>

## 프로젝트 구조
```
├── app
│   ├── common
│   │   ├── config.py
│   │   └── consts.py
│   ├── dao
│   │   └── tire_dao.py
│   ├── database
│   │   ├── conn.py
│   │   ├── models.py
│   │   └── schema.py
│   ├── main.py
│   ├── router
│   │   ├── auth.py
│   │   └── tire.py
│   ├── service
│   │   ├── auth_service.py
│   │   └── tire_service.py
│   └── utils
│       └── token.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       ├── c98f9a31dafa_migration1.py
│       ├── cf40dcd66556_migration1.py
│       ├── d48c840a46cf_migration1.py
│       └── ed36d8b109c4_migration1.py
├── README.md
└── requirements.txt
```

<br><br>

## 서버 구조 및 디자인 패턴 

- sqlalchemy는 session이 사용자와 db 간에 인터페이스 역할을 하는 프록시 패턴이기에 싱글턴 패턴을 이용하여 session을 관리함

- 레이어드 아키텍쳐를 통해 라우팅 역할을 하는 라우트 레이어와 비즈니스 로직을 관리하는 서비스 레이어 그리고 데이터 베이스 로직을 관리하는 persistence 레이어가 dao 폴더에서 관리되고 있다.

<br><br>

## 기능 구현 사항

<br>

### 1. 회원가입 API

**Endpoint**: {BASE}/auth/signup  (POST)

- user_id: 유저 아이디, password: 비밀번호를 입력받아 회원가입 
- role은 미입력하거나 아무거나 입력 시 기본적으로 client(고객)이며 admin(관리자)으로 설정 시 admin role 부여 

입력 예시
```json
{
    "user_id": "peter",
    "password": "abcd1234^",
    "role": "admin"  // admin: 관리자, 그 외: 고객
}
```
**회원가입 성공 시** 
```json
{
  "msg": "SUCCESSFULLY REGISTERED"
}
```
에러처리 1) 동일 아이디가 존재할 시
```json
{
  "msg": "ID ALREADY EXISTS"
}
```
에러처리 2) 비밀번호 양식 미준수 시
```json
{
  "msg": "WRONG PASSWORD FORMAT"
}
```
에러처리 3) 아이디 혹은 비밀번호 미입력 시
```json
{
  "msg": "ID AND PASSWORD REQUIRED"
}
```

<br><br>

### 2. 로그인 API  

**Endpoint**: {BASE}/auth/login  (POST)

<br>

**입력 예시**
```json
{
    "user_id": "peter",
    "password": "abcd1234^"
}
```

**로그인 성공 시** 
```json
{
  "Authorization": "성공 시 토큰",
  "token_type": "bearer"
}
```
에러처리 1) 아이디 혹은 비밀번호 미입력 시
```json
{
  "msg": "ID AND PASSWORD REQUIRED"
}
```
에러처리 2) 없는 아이디 이거나 비밀번호 틀렸을 시
```json
{
  "msg": "WRONG ID OR PASSWORD"
}
```

<br><br>

### 3. 사용자가 소유한 타이어 정보 저장 API

- 정보는 최대 5개까지 허용, 길이 계산하여 초과 시 에러 반환
- trimId(차종)을 이용해 front, rear tire를 구분 후 각각 림 직경, 편평비, 타이어 구조, 휠 사이즈로 나누어 디비에 저장함 
* 타이어 구조는 검색해보니 주로 ZR, R, D가 쓰이는 것으로 확인되어 이를 염두하여 만들었음

<br>

**Endpoint**: {BASE}/tire/register-info  (POST)

**입력 예시**
```json
{
  "item": [
    {
      "id": "peter",
      "trimId": 1
    },
    {
      "id": "peter1",
      "trimId": 2
    },
    {
      "id": "peter2",
      "trimId": 3
    },
    {
      "id": "peter3",
      "trimId": 4
    },
    {
      "id": "peter4",
      "trimId": 5
    }
  ]
}
```
**성공 시**
```json
{
  "msg": "SUCCESS"
}
```
에러처리 1) 입력된 정보가 5개가 넘어갈 시
```json
{
  "msg": "MORE THAN FIVE INFOS"
}
```
에러처리 2) 토큰을 소유한 사용자가 유효한지 검사
```json
{
  "msg": "NO USER EXIST"
}
```
에러처리 3) 등록되지 않은 사용자의 타이어 정보를 기입할 시
```json
{
  "msg": "NOT REGISTERED USER: peter5"
}
```

<br>
<br>

### 4. 사용자가 소유한 타이어 정보 조회 API

- query parameter로 사용자의 아이디를 입력하여 사용자 소유 타이어 정보를 조회함
- 관리자는 본인 여부 상관없이 고객의 타이어 정보 조회 가능
- 고객은 본인의 타이어 정보만 조회 가능
- 조회 성공 시 데이터베이스에 저장되어 있는 타이어의 정보를 담아 반환

**Endpoint**: {BASE}/tire/tire-info/user?name={사용자의 아이디}   (GET)

<br>

조회 성공 시
```json
[
  {
    "user_id": "peter4",
    "tire_position": "front",
    "tire_rim_inch": 205,
    "tire_wheel_size": 15,
    "tire_stucture": "R",
    "tire_aspect_ratio": 60,
    "tire_updated_at": "2021.11.27"
  },
  {
    "user_id": "peter4",
    "tire_position": "front",
    "tire_rim_inch": 195,
    "tire_wheel_size": 15,
    "tire_stucture": "R",
    "tire_aspect_ratio": 55,
    "tire_updated_at": "2021.11.26"
  },
  {
    "user_id": "peter4",
    "tire_position": "rear",
    "tire_rim_inch": 205,
    "tire_wheel_size": 15,
    "tire_stucture": "R",
    "tire_aspect_ratio": 60,
    "tire_updated_at": "2021.11.27"
  },
  {
    "user_id": "peter4",
    "tire_position": "rear",
    "tire_rim_inch": 195,
    "tire_wheel_size": 15,
    "tire_stucture": "R",
    "tire_aspect_ratio": 55,
    "tire_updated_at": "2021.11.26"
  }
]
```

조회하려하는 사용자가 없는 경우
```json
{
    "msg": "NO USER EXIST"
}
```

조회하는 사람이 관리자가 아닐 경우 혹은 본인이 아닐 경우
```json
{
    "msg": "NOT AUTHORIZED"
}
```
<br><br>

## Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
