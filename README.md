# StudentManagementAWSSERVICES

<img width="676" alt="StudentManagementArchitecture" src="https://github.com/phaniteja5789/StudentManagementAWSSERVICES/assets/36558484/cb4cc1a2-5b55-4a68-803f-d3dca944bcb0">

**Problem Statement**

Files will be uploaded into different S3 Buckets, Based on S3 Bucket Object data process the data insert the data into Dynamo DB Tables, and send an email to the respective user mail.

**AWS Services Used**
 AWS S3
 AWS DynamoDB
 AWS Lambda
 AWS SNS
 AWS CloudShell
 AWS IAM

**Packages used**

JSON, Boto3,Requests,s3fs, AWS CLI

**Application Stages**

**Stage - 1**  <br/>

    1.) Created an IAM Role with S3 Read Access, SNS publish Access, and DynamoDB Access  <br/>
    
    2.) Created a Layer using AWS CloudShell which includes **Boto3, JSON, Requests** packages <br/> 
    
    3.) Created a Lambda Function and attached the IAM Role and Layer that is created from AWS Cloudshell   <br/>
    
      3.1.) Changed the Lambda Default Configurations
              TimeOut Execution = 5 Mins
    4.) Created an SNS Topic and added a subscription to the SNS Topic as an Email Type. With a specific email <br/>

From AWS Management Console Stage-1 has been developed <br/>

**Stage-2**
    1.) Installed required modules in the Local virtual environment <br/>
    2.) Created a JSON File with the required details <br/>
    3.) Created the S3 client and Lambda Client using BOTO3 API <br/>
    4.) Created a S3 Bucket using BOTO3 API <br/>
    5.) Added Permission to the Lambda client from the S3 Bucket <br/>
    6.) Attached is the put_bucket_notification_configuration event to the s3 bucket with Lambda ARN <br/>
    7.) Uploaded the created JSON File into the S3 Bucket <br/>

The Code for Stage 2 is present in SourceCode.ipynb <br/>

  **Stage-3**
    1.) In the Lambda Function the uploaded object data event will be fetched <br/>
    2.) Created 2 Dynamo DBs tables with StudentId as Partition Key and StudentName as SortKey in both tables <br/>
    3.) Based on object data the record will be inserted into the respective dynamodb table <br/>
    4.) Once the data has been inserted into the table. <br/>
    5.) Lambda Function will publish the message to the SNS Topic that is created in Stage-1 <br/>
    6.) The Message will be sent to the Subscriber Email from Boto3 API using the SNS Client <br/>

    
