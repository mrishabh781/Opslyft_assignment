# Opslyft_assignment

Task : To create crud operation for EC2 scheduling.

# Approach:
* Written two lambda function, one which take two input params (task:['start','stop'] and instanceid)
* Other lambda function creates the schedule and assign target to it and handels all the api call via api gateway.
* one flask application is deployed on ec2 with nginix proxy server whiche handels crud operation from user and accordingly calls the lambda api.

# Endpoints:
For now code is handling only one instance
* Get :- http://65.1.5.171/schedule/<instance-id>
  URL - http://65.1.5.171/schedule
  
  Response:- {
    "response": {
        "schedules": [
            {
                "Arn": "arn:aws:events:ap-south-1:250244046406:rule/new_event_i-0bdd329c638b15451",
                "Description": "Scheduling instance as per api call",
                "EventBusName": "default",
                "Name": "new_event_i-0bdd329c638b15451",
                "RoleArn": "arn:aws:iam::250244046406:role/service-role/lamdaRole",
                "ScheduleExpression": "rate(5 minutes)",
                "State": "ENABLED"
            }
        ]
    }
}


* Post:- http://65.1.5.171/schedule   body={"task":"start", "instanceId":"i-0bdd329c638b15451","days":"rate(5 minutes)"} #days can be corn expression
Response: {
    "response": {
        "message": "Scheduled successfully!"
    }
}

* Put:- http://65.1.5.171/schedule   body={"task":"start", "instanceId":"i-0bdd329c638b15451","days":"rate(5 minutes)"} #days can be corn expression
Response: {
    "response": {
        "message": "Scheduled successfully!"
    }
}

* Delete :- http://65.1.5.171/schedule   body={"instanceId":"i-0bdd329c638b15451"}

{
    "response": {
        "message": "Schedule deleted susseccfully!"
    }
}
