import boto3
import os

s3 = boto3.resource('s3')

# Get list of objects for indexing
images = [
    ('image01.jpeg', 'M S Dhoni'),
    ('image02.jpeg', 'M S Dhoni'),
    ('image03.jpeg', 'Sachin'),
    ('image04.jpeg', 'Sachin'),
    ('image05.jpeg', 'Virat'),
    ('image06.jpeg', 'Virat')
]

# Ensure the images are in the "images" folder under the current directory
image_path = os.path.join(os.getcwd(), 'images')


# Iterate through list to upload objects to S3
for image in images:
    file_path = os.path.join(image_path, image[0])
    try:
        with open(file_path, 'rb') as file:
            object = s3.Object('sportsperson-images-jipx', 'index/' + image[0])
            ret = object.put(Body=file, Metadata={'FullName': image[1]})
            print(f"Uploaded {image[0]} successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
