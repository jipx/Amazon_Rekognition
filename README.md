# Amazon_Face_Rekognition
Use case example of face rekognition with an example

## Architectural Flow
![awsrek](https://github.com/vijayaraghavanv/Amazon_Face_Rekognition/assets/25921640/4d778f20-0ca4-4131-96ce-340a2ad3e9ab)


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
