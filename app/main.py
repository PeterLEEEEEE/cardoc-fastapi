from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database.conn import db
from common.config import conf
from router import auth, tire


def create_app():
    c = conf()
    app = FastAPI()

    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(auth.router)
    app.include_router(tire.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
