"""
FastAPI backend for YOLO object detection
"""

from contextlib import asynccontextmanager

from api.routes import router
from config import settings
from container import Container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import logger

# DIコンテナを初期化
container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時
    logger.info("Starting YOLO backend application...")

    # コンテナのリソースを初期化
    container.init_resources()

    logger.info("Application startup complete")

    yield

    # 終了時
    logger.info("Shutting down application...")
    container.shutdown_resources()


# FastAPIアプリケーション
app = FastAPI(
    title="YOLO Detection API",
    description="YOLOv10 based object detection API",
    version="1.0.0",
    lifespan=lifespan,
)

# DIコンテナをワイヤリング
container.wire(modules=["api.dependencies", "api.routes"])

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(router)
