# Backend - YOLO Object Detection API

YOLO物体検出のバックエンドAPIです。FastAPIで構築されています。

## 技術スタック

- **フレームワーク**: FastAPI
- **言語**: Python 3.12+
- **パッケージマネージャー**: uv
- **推論エンジン**: ONNX Runtime（予定）
- **モデル**: YOLOv10n

## 機能

- ヘルスチェックエンドポイント（`/healthz`）
- 画像アップロードと検証（`/api/detect`）
- CORS設定（開発環境とVercel対応）
- 将来的にYOLO物体検出機能を実装予定

## セットアップ

### 前提条件

- Python 3.12以上
- uv（推奨）または pip

### インストール

```bash
# プロジェクトルートで依存関係をインストール
uv sync
```

## 開発

### 開発サーバー起動

```bash
# ポート8080で起動（推奨）
cd backend
uv run fastapi dev --port 8080
```

開発サーバーが起動したら:
- API: http://127.0.0.1:8080
- ドキュメント: http://127.0.0.1:8080/docs
- ReDoc: http://127.0.0.1:8080/redoc

### フロントエンドとの連携

フロントエンドとバックエンドを同時に起動:

#### 1. ターミナル1（バックエンド）

```bash
cd backend
uv run uvicorn main:app  --host localhost --port 8080
```

#### 2. ターミナル2（フロントエンド）

```bash
cd frontend
npm run dev
```

## API エンドポイント

### `GET /healthz`

ヘルスチェック用エンドポイント

**レスポンス:**

```json
{
  "ok": true
}
```

### `POST /api/detect`

画像ファイルをアップロードし、物体検出を実行します（現在は仮実装）。

**リクエスト:**

- Content-Type: `multipart/form-data`
- Body: `file` - 画像ファイル（image/*）

## プロジェクト構造

```text
backend/
├── __init__.py              # Pythonパッケージ初期化
├── main.py                  # FastAPIアプリケーション
├── YOLOv10n.onnx           # YOLOモデルファイル
├── static/                 # 静的ファイル（予定）
└── __pycache__/            # Pythonキャッシュ
```

## CORS設定

以下のオリジンからのリクエストを許可:

- `http://localhost:5173` - Vite開発サーバー
- `https://*.vercel.app` - Vercel本番/プレビュー環境

本番環境で特定のVercelドメインのみ許可する場合は、[main.py](main.py) の `allow_origins` を更新してください。

## デプロイ

### Docker ビルド

```bash
# プロジェクトルートで実行
docker build -t yolo-on-aws .
docker run -p 8080:8080 yolo-on-aws
```

詳細は[プロジェクトルートのREADME](../README.md)を参照してください。

## 次のステップ

- [ ] ONNX Runtimeの依存関係追加
- [ ] YOLOv10nモデルのロード処理実装
- [ ] 画像前処理・後処理の実装
- [ ] 検出結果の可視化データ生成
- [ ] ユニットテスト追加
- [ ] ロギング強化
- [ ] エラーハンドリング改善
