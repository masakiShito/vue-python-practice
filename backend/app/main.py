from fastapi import FastAPI
from .database import engine
from app.models.base import Base  # ← 絶対パスに修正
from .controller import room_controller  # ← 修正

app = FastAPI()

# テーブル作成
Base.metadata.create_all(bind=engine)

# ルーター登録
app.include_router(room_controller.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI + PostgreSQL + Vue.js"}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
