"""ロギング設定"""
import logging
import sys
from config import settings


def setup_logger(name: str = __name__) -> logging.Logger:
    """ロガーをセットアップ"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.log_level.upper()))
    
    # ハンドラーが既に設定されている場合はスキップ
    if logger.handlers:
        return logger
    
    # コンソールハンドラー
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.log_level.upper()))
    
    # フォーマッター
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


# デフォルトロガー
logger = setup_logger("yolo_backend")
