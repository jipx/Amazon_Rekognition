# Amazon_Face_Rekognition
Use case example of face rekognition with an example

- Configure
```
aws configure
```

- Create a collection on aws rekognition
```
aws rekognition create-collection --collection-id sportspersons --region us-east-1
```

- Create table on DynamoDB
```
aws dynamodb create-table --table-name sportsperson_recognition \
--attribute-definitions AttributeName=RekognitionId,AttributeType=S \
--key-schema AttributeName=RekognitionId,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--region us-east-1
```

- Create S3 bucket
```
aws s3 mb s3://bucket-name --region us-east-1
```