# Amazon_Rekognition
Step by step process flow on how to build your own facial recognition service using Amazon Rekognition

## Architectural Flow :mage:
![awsrek](https://github.com/vijayaraghavanv/Amazon_Face_Rekognition/assets/25921640/4d778f20-0ca4-4131-96ce-340a2ad3e9ab)


### :atom: Configuring the AWS CLI with secure access keys
:pushpin: You can use either AWS-shell or AWS CLI to interact with AWS console. In this example, am going to take AWS CLI. Below is the command to configure the secure token in AWS console
```
aws configure
```
![AWS CLI](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/f1de2e06-5af2-49ad-a7dc-ab7b608cb49d)


### :atom: Create a collection on aws rekognition
 :pushpin: Create a collection in aws rekognition. Below is the command to create a collection in amazon rekognition.
```
aws rekognition create-collection --collection-id <collection_name> --region us-east-1
```

### :atom: Creation of an S3 Bucket
:pushpin: Create an S3 bucket we can achieve this in either way through AWS Console or AWS CLI. In this example, Had created through an AWS CLI
```
aws s3 mb s3://<bucket_name> --region us-east-1
```
![s3 bucket creation](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/48df40a5-9924-4f64-8586-2eefc46fe1d5)

### :atom: Creation of an DynamoDB Table
:pushpin: Create a table with table name celebrity_recognition. We can create table either way through console or AWS CLI. In this example, Had created through an AWS CLI.
```

aws dynamodb create-table --table-name <table_name> --attribute-definitions AttributeName=RekognitionId,AttributeType=S --key-schema AttributeName=RekognitionId,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-east-1
```
![Dynamo DB](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/6c2459d4-026e-4462-9704-99b4ba43e547)

### :atom: Creation of new IAM role to access AWS Lambda, Dynamo DB and S3 bucket
:pushpin: Go to IAM in management console, create a new role and name the role as aws_rekognition_role as below.

:pushpin: Once the role is created, Go to the newly created role and create the inline policy to it. Copy and paste the below json in the json format. 
 Replace the s3 bucket name and dynamo DB ARN with the one you had created newly.
 ```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::bucket-name/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:aws-region:account-id:table/table_name"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "rekognition:IndexFaces"
            ],
            "Resource": "*"
        }
    ]
}

![AWS Role](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/0a6d292b-5f34-479c-b102-1f83cade490d)

```
:pushpin: Give the policy name as aws_rekognition_policy and click on create policy. Attach this policy to the new role created.

### :atom: Setting up an lambda function
:pushpin: Go to AWS Lambda in management console and create the new function called aws_rekognition_lambda. 
Use the existing role which we created aws_rekognition_role. Click on create function.

![AWS Lambda](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/0b13a815-74b4-4d7b-8148-d0fb0e68b7c0)


### :atom: Setting up an trigger to the lambda function
:pushpin: Go to configuration tab, click on triggers and click add trigger. Search for an S3 Bucket, give the bucket name as sportsperson-images. Event type as All object create events, give the prefix as index/. Click on the check box and add the trigger as below
![s3 trigger](https://github.com/vjraghavanv/Amazon_Rekognition/assets/25921640/6e34c442-52b8-4a74-b65f-2766fb85e346)

### :atom: Adding lambda function code in AWS Lambda
:pushpin: Go to code tab, replace the lambda_function.py with below code.
```
from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


# --------------- Helper Functions ------------------

def index_faces(bucket, key):

    response = rekognition.index_faces(
        Image={"S3Object":
            {"Bucket": bucket,
            "Name": key}},
            CollectionId="celebrities")
    return response
    
def update_index(tableName,faceId, fullName):
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName}
            }
        ) 
    
# --------------- Main handler ------------------

def lambda_handler(event, context):

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("Records: ",event['Records'])
    key = event['Records'][0]['s3']['object']['key']
    print("Key: ",key)
    # key = key.encode()
    # key = urllib.parse.unquote_plus(key)

    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        
        response = index_faces(bucket, key)
        
        # Commit faceId and full name object metadata to DynamoDB
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            ret = s3.head_object(Bucket=bucket,Key=key)
            personFullName = ret['Metadata']['fullname']

            update_index('celebrity_recognition',faceId,personFullName)

        # Print response to console
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e
```
### :atom: Uploading the images into an S3 bucket for training the model
:pushpin: Upload the images into an S3 bucket through AWS CLI, below is the python file. 
Change the bucket name and train your model accordingly as per image upload
```
import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('image1.jpg','M S Dhoni'),
      ('image2.jpg','M S Dhoni'),
      ('image3.jpg','Sachin'),
      ('image4.jpg','Sachin'),
      ('image5.jpg','Virat'),
      ('image6.jpg','Virat')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('sportsperson-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})
```
:pushpin: Command to upload this images into an S3 Bucket
```
python .\putimages.py
```
:pushpin: Similarly, navigate to Dynamo DB console and validate the index been created 

### :atom: Testing the model with new images by faceprint
:pushpin: Below is the code used to test the new images with already trained images. If face print matches it will say name of the person otherwise it will say person cannot be recognized.

:pushpin: Before running the below ‘test.py’. Run this command to install Pillow or make sure pillow been installed
```
pip install Pillow
```
```
import boto3
import io
from PIL import Image

rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

image_path = input("Enter path of the image to check: ")

image = Image.open(image_path)
stream = io.BytesIO()
image.save(stream,format="JPEG")
image_binary = stream.getvalue()

response = rekognition.search_faces_by_image(
        CollectionId='celebrities',
        Image={'Bytes':image_binary}                                       
        )

found = False
for match in response['FaceMatches']:
    print (match['Face']['FaceId'],match['Face']['Confidence'])
        
    face = dynamodb.get_item(
        TableName='celebrity_recognition',  
        Key={'RekognitionId': {'S': match['Face']['FaceId']}}
        )
    
    if 'Item' in face:
        print ("Found Person: ",face['Item']['FullName']['S'])
        found = True

if not found:
    print("Person cannot be recognized")
```

### :broom: Instructions to clean up AWS resource to avoid Billing

:recycle: Delete the collection created using the following command
```
aws rekognition delete-collection --collection-id celebrities
```
:recycle: Delete an S3 bucket created through AWS Console after the deleting the images

:recycle: Delete the dynamo DB created through AWS Console after deleting the indexes

:recycle: Delete the new IAM role created

:recycle: Delete the trigger in lambda configuration

:recycle: Delete the lambda function newly created
