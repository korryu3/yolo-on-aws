from fastapi import FastAPI
app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

# TODO: 1. 簡易的に触れるフロントエンドを実装する
# 画像を入れれる雛形を作る
# vite + react + tsで簡易的に作りたいな
# ディレクトリ構成も考慮して実装する




# TODO: 2. FargateのCPUでONNX　Runtimeを動かす
# runtimeで動かす処理は、関数分離させてテスト可能性を保証したい
# 推論したら、とりあえずDoneを返すだけで良い
# modelのロードは、コンテナ起動時に一度だけ行うようにする
