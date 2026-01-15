ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

cd infra
ECR_URL=$(terraform output -raw ecr_repository_url)
cd ..

aws ecr get-login-password --region $REGION \
    | docker login --username AWS --password-stdin $ECR_URL

TAG=v0-healthz
IMAGE_URI="$ECR_URL:$TAG"

# amd64(x86_64)向けにビルドしてプッシュ (ECS Fargate用)
docker buildx build --platform linux/amd64 -t $IMAGE_URI --push .
echo "IMAGE_URI=$IMAGE_URI"
