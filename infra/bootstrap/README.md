# Terraform Bootstrap

このディレクトリには、Terraformのstateファイルを保存するためのS3バケットを作成するためのTerraform構成が含まれています。

## 目的

メインのインフラストラクチャをデプロイする前に、Terraformのリモートバックエンド用のS3バケットを作成する必要があります。このbootstrap構成により、以下が作成されます:

- S3バケット (`yolo-on-aws-terraform-state`)
- バケットバージョニング（有効化）

## セットアップ手順

### 1. Bootstrap環境の初期化と適用

まず、このbootstrapディレクトリでTerraform stateバケットを作成します:

```bash
cd infra/bootstrap
terraform init
terraform plan
terraform apply
```

**重要**: このbootstrapディレクトリのstateファイルは**ローカル**に保存されます（`.terraform/`および`terraform.tfstate`ファイル）。これらのファイルは大切に保管してください。

### 2. メインインフラストラクチャの設定

bootstrapが完了したら、親ディレクトリに戻ってメインのインフラストラクチャをデプロイできます:

```bash
cd ..  # infra/ディレクトリに戻る
terraform init  # S3バックエンドが設定されます
terraform plan
terraform apply
```

## 注意事項

- `bootstrap/terraform.tfstate`ファイルはGit管理から除外し、安全な場所にバックアップしてください
- S3バケット名は一意である必要があります。必要に応じて`main.tf`のバケット名を変更してください
- このbootstrap構成を削除する場合は、先にメインインフラストラクチャを削除してから行ってください
