"""設定管理"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # モデル設定
    model_path: Path = Path(__file__).parent / "YOLOv10n.onnx"
    
    # 推論設定
    default_confidence_threshold: float = 0.25
    input_size: int = 640
    
    # CORS設定
    cors_origins: list[str] = [
        "http://localhost:5173",
        "https://*.vercel.app",
    ]
    
    # ログ設定
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
