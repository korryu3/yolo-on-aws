# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AWS上にデプロイされるYOLOv10ベースの物体検出アプリケーション（雑草検出用）。フロントエンド（React/Vercel）、バックエンド（FastAPI/ECS Fargate）、インフラ（Terraform）の3層構成。

## Development Commands

### Frontend (frontend/)
```bash
npm run dev       # 開発サーバー起動 (localhost:5173)
npm run build     # プロダクションビルド
npm run lint      # ESLint実行
```

### Backend (backend/)
```bash
uv sync                              # 依存関係インストール
cd backend/
uv run uvicorn main:app --reload --port 8080  # 開発サーバー起動 (localhost:8080)
uv run test_inference.py     # 推論テスト実行
```

### Infrastructure (infra/)
```bash
# 初回: Bootstrap → ECR → 全体デプロイの順で実行
cd infra/bootstrap && terraform init && terraform apply
cd infra && terraform init
terraform apply

# ECS サービス管理
aws ecs update-service --cluster yolo-on-aws-cluster --service yolo-on-aws-api-service --desired-count 1  # 起動
aws ecs update-service --cluster yolo-on-aws-cluster --service yolo-on-aws-api-service --desired-count 0  # 停止

# ECS Image デプロイ
bash api-deploy.sh  # 新しいイメージでサービス更新
aws ecs update-service --cluster yolo-on-aws-cluster --service yolo-on-aws-api-service --force-new-deployment
```

## Architecture

```
[Vercel Frontend] ←CORS→ [AWS ALB:80] → [ECS Fargate] → [FastAPI + ONNX Runtime]
     React 19                                              YOLOv10n Model
```

### Backend Request Flow

1. `POST /api/detect` で画像バイト受信
2. `ImageProcessor.preprocess()` - Letterbox (640x640) + 正規化
3. `InferenceService.run()` - ONNX Runtime推論
4. `ImageProcessor.postprocess()` - 座標スケーリング + フィルタリング
5. `DetectionResponse` 返却

### Key Files

- `backend/services/inference.py` - ONNX推論実行
- `backend/services/image_processing.py` - 前処理・後処理
- `backend/utils/constants.py` - 定数（INPUT_SIZE=640, CLASSES=['weed']）
- `frontend/src/hooks/useDetection.ts` - 検出ロジック・状態管理
- `infra/main.tf` - AWS リソース定義（VPC, ALB, ECS）

### Environment Variables
- Frontend: `VITE_API_URL` (APIエンドポイント)
- Backend: `MODEL_PATH`, `CORS_ORIGINS` (Pydantic Settings経由)

## AWS Resources

- **Region:** us-east-1
- **ECS:** 0.25 vCPU, 512 MB
- **ALB:** HTTP:80 → ECS:8080
- **Logs:** CloudWatch `/ecs/yolo-on-aws-api`
