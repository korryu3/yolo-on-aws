"""
FastAPI backend for YOLO object detection
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.services.model_loader import ModelLoader
from backend.services.image_processing import ImageProcessor
from backend.api import dependencies
from backend.api.routes import router
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # 起動時
    logger.info("Starting YOLO backend application...")
    
    # モデルローダーを初期化
    model_loader = ModelLoader(settings.model_path)
    model_loader.load()
    dependencies.model_loader = model_loader
    
    # 画像処理サービスを初期化
    image_processor = ImageProcessor(input_size=settings.input_size)
    dependencies.image_processor = image_processor
    
    logger.info("Application startup complete")
    
    yield
    
    # 終了時
    logger.info("Shutting down application...")


# FastAPIアプリケーション
app = FastAPI(
    title="YOLO Detection API",
    description="YOLOv10 based object detection API",
    version="1.0.0",
    lifespan=lifespan
)

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
