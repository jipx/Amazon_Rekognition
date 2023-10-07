import boto3

s3 = boto3.resource('s3')

# Get list of objects for indexing
images=[('image01.jpeg','M S Dhoni'),
      ('image02.jpeg','M S Dhoni'),
      ('image03.jpeg','Sachin'),
      ('image04.jpeg','Sachin'),
      ('image05.jpeg','Virat'),
      ('image06.jpeg','Virat')
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('sportsperson-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})