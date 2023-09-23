import json
import boto3

def putItemIntoTable(dynamodb_client, tableName, parsed_data):
    
    print(tableName,parsed_data)
    dynamodb_client.put_item(
        TableName = tableName,
        Item = {
            "StudentId" : {
                
                "S": str(parsed_data["student_id"])
            },
            "StudentName" : {
            
                "S" : str(parsed_data["student_name"])        
            },
            
            "StudentMarks" :
                {
                    "S" : str(parsed_data["student_marks"])
                }
            
        }
    )

def insertItemIntoTable(tableName, parsed_data,dynamodb_client):
    ## Dynamo db table creation using Boto3 API and Insertion
        
	available_tables = dynamodb_client.list_tables()['TableNames']
	
	if tableName not in available_tables:
		
		table_creation_response = dynamodb_client.create_table(
			
			AttributeDefinitions = [
				
				{
					"AttributeName" : "StudentId",
					"AttributeType" : "S"
				},
				
				{
					"AttributeName" : "StudentName",
					"AttributeType" : "S"
				}],
				
			TableName = tableName,
			KeySchema=[
				{
					'AttributeName': 'StudentId',
					'KeyType': 'HASH'
				},
				{
					'AttributeName': 'StudentName',
					'KeyType': 'RANGE'
				}
			],
			BillingMode = "PAY_PER_REQUEST"
			
			)
			
		print(table_creation_response)
	else:
		pass

	putItemIntoTable(dynamodb_client,tableName,parsed_data)


def lambda_handler(event, context):
    # TODO implement
    s3_event = event["Records"][0]['s3']
    bucket_name = s3_event["bucket"]["name"]
    object_key = s3_event["object"]["key"]
    print(bucket_name,object_key)
    
    s3_client = boto3.client('s3')
    
    dynamodb_client = boto3.client('dynamodb')
    
    sns_client = boto3.client('sns')
    
    sns_topic_name = "StudentManagementTopic"
    
    sns_topic_arn = "arn:aws:sns:us-east-1:433169439701:StudentManagementTopic"
    
    object_response = s3_client.get_object(Bucket = bucket_name, Key = object_key)
    
    object_data = object_response['Body'].read().decode('utf-8')
    
    parsed_data = json.loads(object_data)
    
    if(parsed_data["student_marks"] > 50):
        
        print("student details needs to be inserted into dynamodb table")
        
        tableName = "PassedStudentsTable30101999"
        
        insertItemIntoTable(tableName,parsed_data,dynamodb_client)
        
        ## SNS Topic Message Publish and Subscribe
        
        sns_topic_response = sns_client.publish(TopicArn = sns_topic_arn, Message = parsed_data["student_name"]+" has been inserted into the dynamodb table")
        
        print(sns_topic_response["MessageId"])
        
    else:
        
        print("student details needs to be inserted into dynamodb table failed table")
        
        ## Dynamo db table creation using BOTO3 API and Insertion
        
        tableName = "FailedStudentsTable30101999"
        
        insertItemIntoTable(tableName,parsed_data,dynamodb_client)
        
        ## SNS Topic Message Publish and Subscibe
        
        sns_topic_response = sns_client.publish(TopicArn = sns_topic_arn, Message = parsed_data["student_name"]+" has been inserted into the dynamodb table")
        
        print(sns_topic_response["MessageId"])

    print("Completed")