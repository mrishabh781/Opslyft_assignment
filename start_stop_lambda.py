import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    ec2 = boto3.client('ec2')
    task = event['task']
    instance = event['instanceId']
    client = boto3.client('events')
    if task == 'start':
        response = ec2.start_instances(InstanceIds=[instance])
        x = {"Current State":response['StartingInstances'][0]['CurrentState'], "previous state":response['StartingInstances'][0]['PreviousState']}
        print(x)
        message = "Start requested successfully"
    if task == 'stop':
        response = ec2.stop_instances(InstanceIds=[instance])
        print(response)
        x = {"Current State":response['StoppingInstances'][0]['CurrentState'], "previous state":response['StoppingInstances'][0]['PreviousState']}
        message = "Stop requested successfully"
    
    return {
        'statusCode': 200,
        'body': json.dumps(x),
        'message': message
    }
