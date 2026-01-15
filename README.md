# yolo-on-aws

1. `cd bootstrap`
   1. `tf init`
   2. `tf apply`
2. Build & Push ECR image
   1. `cd infra`
   2. `tf apply -target=aws_ecr_repository.api -var="image_uri=xxx"`
   3. `cd ..`
   4. `bash api-push.sh`
   5. Copy the `IMAGE_URI` output from the script
3. main infra
   1. `cd infra`
   2. `tf init`
   3. `tf apply -var="image_uri=xxx.dkr.ecr.us-east-1.amazonaws.com/yolo-on-aws-api:v0-healthz" -var="execution_role_arn=arn:aws:iam::xxx:role/LabRole"`
      1. `xxx`は自分のAWSアカウントIDに置き換えてください
