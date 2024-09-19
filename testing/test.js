const { RekognitionClient, SearchFacesByImageCommand } = require('@aws-sdk/client-rekognition');
const { DynamoDBClient, GetItemCommand } = require('@aws-sdk/client-dynamodb');
const fs = require('fs');

// Initialize AWS clients
const rekognition = new RekognitionClient({ region: 'us-east-1' });
const dynamodb = new DynamoDBClient({ region: 'us-east-1' });

// Load image
const imagePath = './msd.jpeg';
//const imagePath = './sachin.jpeg';
const imageBinary = fs.readFileSync(imagePath);

const searchFaces = async () => {
    try {
        const rekogParams = {
            CollectionId: 'sportspersons',
            Image: {
                Bytes: imageBinary
            }
        };
        const response = await rekognition.send(new SearchFacesByImageCommand(rekogParams));

        let found = false;
        for (const match of response.FaceMatches) {
            console.log(`FaceId: ${match.Face.FaceId}, Confidence: ${match.Face.Confidence}`);

            const dynamoParams = {
                TableName: 'sportsperson_recognition',
                Key: {
                    'RekognitionId': { S: match.Face.FaceId }
                }
            };
            const faceData = await dynamodb.send(new GetItemCommand(dynamoParams));

            if (faceData.Item) {
                console.log(`Found Person: ${faceData.Item.FullName.S}`);
                found = true;
            }
        }
        if (!found) {
            console.log("Person cannot be recognized");
        }
    } catch (error) {
        console.error("Error:", error);
    }
};

searchFaces();

