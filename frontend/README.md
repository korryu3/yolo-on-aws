# Frontend - YOLO Object Detection UI

YOLO物体検出APIのフロントエンドアプリケーションです。Vite + React + TypeScriptで構築されています。

## 技術スタック

- **フレームワーク**: React 19
- **ビルドツール**: Vite 7
- **言語**: TypeScript
- **スタイリング**: Tailwind CSS 3

## 機能

- 画像ファイルのアップロード
- 画像プレビュー表示
- バックエンドAPI（`/api/detect`）への画像送信
- 検出結果の表示
- エラーハンドリング

## セットアップ

### 前提条件

- Node.js 18以上
- npm

### インストール

```bash
# 依存関係のインストール
npm install

# 環境変数ファイルの作成
cp .env.development.example .env.development
```

### 環境変数

`.env.development`ファイルを作成し、以下の環境変数を設定してください：

```env
VITE_API_URL=http://localhost:8080
```

**環境変数の説明:**
- `VITE_API_URL`: バックエンドAPIのベースURL
  - 開発環境: `http://localhost:8080`
  - 本番環境: Vercelの環境変数で設定（例: `http://<ALB-URL>`）

## 開発

### 開発サーバー起動

```bash
npm run dev
```

ブラウザで http://localhost:5173/ にアクセスしてください。

### バックエンドとの連携

フロントエンドとバックエンドを同時に起動する必要があります：

1. **ターミナル1（バックエンド）**:
   ```bash
   cd ../backend
   uv run fastapi dev
   # または
   uvicorn main:app --reload --port 8080
   ```

2. **ターミナル2（フロントエンド）**:
   ```bash
   cd frontend
   npm run dev
   ```

## ビルド

### プロダクションビルド

```bash
npm run build
```

ビルド成果物は `dist/` ディレクトリに出力されます。

### プレビュー

```bash
npm run preview
```

ビルドした成果物をローカルでプレビューできます。

## デプロイ

### Vercel デプロイ

1. **GitHubリポジトリにプッシュ**:
   ```bash
   git add .
   git commit -m "Add frontend"
   git push
   ```

2. **Vercelプロジェクト作成**:
   - [Vercel Dashboard](https://vercel.com/dashboard) にアクセス
   - "New Project" をクリック
   - GitHubリポジトリを選択
   - **Root Directory**: `frontend` を設定
   - **Environment Variables**: 
     - `VITE_API_URL`: `http://<ALB-DNS-NAME>` を設定

3. **ALB URLの取得**:
   ```bash
   cd ../infra
   terraform output alb_dns_name
   ```

4. **デプロイ実行**:
   - Vercelが自動的にビルドとデプロイを実行します

### CLI経由でのデプロイ

```bash
# Vercel CLIのインストール（初回のみ）
npm install -g vercel

# デプロイ
vercel --prod
```

## ディレクトリ構造

```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUpload.tsx      # 画像アップロードコンポーネント
│   │   └── ImageUpload.css      # スタイリング
│   ├── App.tsx                  # メインアプリケーション
│   ├── App.css
│   ├── main.tsx                 # エントリーポイント
│   └── vite-env.d.ts
├── public/
├── .env.development             # 開発環境変数（gitignore対象）
├── .env.development.example     # 環境変数サンプル
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## スクリプト

| コマンド | 説明 |
|---------|------|
| `npm run dev` | 開発サーバー起動（http://localhost:5173） |
| `npm run build` | プロダクションビルド |
| `npm run preview` | ビルド成果物のプレビュー |
| `npm run lint` | ESLintによるコードチェック |

## トラブルシューティング

### CORS エラーが発生する

バックエンドでCORSが正しく設定されていることを確認してください：

```python
# backend/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 環境変数が読み込まれない

- ファイル名が `.env.development` になっているか確認
- `VITE_` プレフィックスが付いているか確認（Viteの仕様）
- サーバーを再起動してください

### API接続エラー

1. バックエンドが起動しているか確認: `curl http://localhost:8080/healthz`
2. `.env.development` のURLが正しいか確認
3. ブラウザの開発者ツールでネットワークタブを確認

## 次のステップ

- [ ] バックエンドAPI実装（`/api/detect`エンドポイント）
- [ ] YOLO検出結果の可視化（バウンディングボックス表示）
- [ ] レスポンシブデザインの改善
- [ ] ダークモード対応
- [ ] 検出履歴機能
