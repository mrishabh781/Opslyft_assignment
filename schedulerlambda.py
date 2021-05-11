import json
import boto3
import random

def lambda_handler(event, context):
	iam_role_arn = "arn:aws:iam::250244046406:role/service-role/lamdaRole"
	lambda_role_arn = "arn:aws:lambda:ap-south-1:250244046406:function:startInstance"
	client = boto3.client('lambda')
	#x = client.add_permission(FunctionName="instanceScheduler", StatementId="samplestatementtocheck", Action="lambda:InvokeFunction", Principal="ec2.amazonaws.com")
	#print(x)
	method = event['httpMethod']
	message =""
	if method == "POST" or method == "PUT":
		data = json.loads(event['body'])
		print(data)
		print(data['instanceId'])
		instanceid = data['instanceId']
		task = data['task']
		days = data['days']
		input_dict = {"task": task, "instanceId":instanceid}
		#cron(0 12 * * ? *)
		client = boto3.client('events')
		event_name = "new_event_"+ instanceid
		new_event = client.put_rule(
				Name = event_name,
				ScheduleExpression = days,
				State = "ENABLED",
				Description = "Scheduling instance as per api call",
				RoleArn = iam_role_arn
			)
		set_target = client.put_targets(
				Rule = event_name,
				Targets = [
						{
							'Id' : "target_startInstance",
							'Arn' : lambda_role_arn,
							'Input': json.dumps(input_dict)
						}
					]
			)
		put_event = client.put_events(
				Entries = [
					{
						'Detail':json.dumps({ "task": "start","instanceId": "i-0bdd329c638b15451"}),
						'DetailType': 'appRequestSubmitted',
						'Resources': [
							new_event['RuleArn'],
						],
						'Source': 'com.company.myapp'
					}
					]
			)
		client = boto3.client('ec2')
		client.create_tags(Resources=[instanceid], Tags=[{'Key':'scheduled', 'Value':'True'}])
		print(put_event)
		#print(perm)
		message = "Scheduled successfully!"
		return {'statusCode': 200, "body": json.dumps({'message': message})}
	
	if method== "GET":
		#data =  json.loads(event['body'])
		#instance_id = data.get("instanceId")
		client = boto3.client('events')
		
		rules = client.list_rules(NamePrefix="new_event")
		print(rules)
		return { 
				'statusCode': 200,
				"body":json.dumps({"schedules":rules['Rules']})
				}
	
	if method== "DELETE":
		data =  json.loads(event['body'])
		instance_id = data.get("instanceId")
		client = boto3.client('events')
		try :
			response = client.list_targets_by_rule(Rule="new_event_" + instance_id,)
			targets = client.remove_targets(Rule="new_event_" + instance_id, Ids=[response['Targets'][0]['Id']])
			client.delete_rule(Name="new_event_" + instance_id)
			rules = {"message":"Schedule deleted susseccfully!"}
			print(rules)
			client = boto3.client('ec2')
			client.delete_tags(Resources=[instance_id], Tags=[{'Key':'scheduled', 'Value':'True'}])
		except:
			rules = {"message":"No schedule found for the give instanceId!"}

		return { 
				'statusCode': 200,
				'body': json.dumps(rules)
			}
	
