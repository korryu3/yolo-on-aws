from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite開発サーバー
        "https://*.vercel.app",   # Vercel本番/プレビュー
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/api/detect")
async def detect(file: UploadFile = File(...)):
    """
    画像ファイルを受け取り、物体検出を実行する（現在は仮実装）
    """
    # ファイル情報の検証
    if not file.content_type.startswith("image/"):
        return {
            "status": "error",
            "message": "画像ファイルのみアップロード可能です",
            "detections": []
        }
    
    # 現時点では仮レスポンスを返す
    # TODO: YOLO推論処理を実装
    return {
        "status": "ok",
        "detections": [],
        "message": f"画像 '{file.filename}' を受信しました（推論処理は未実装）"
    }

# TODO: 1. 簡易的に触れるフロントエンドを実装する
# 画像を入れれる雛形を作る
# vite + react + tsで簡易的に作りたいな
# ディレクトリ構成も考慮して実装する




# TODO: 2. FargateのCPUでONNX　Runtimeを動かす
# runtimeで動かす処理は、関数分離させてテスト可能性を保証したい
# 推論したら、とりあえずDoneを返すだけで良い
# modelのロードは、コンテナ起動時に一度だけ行うようにする
