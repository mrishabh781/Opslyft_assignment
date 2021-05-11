from flask import (
	Flask,
	request,
	url_for,
	make_response
)
import random
import requests
import json

app = Flask(__name__)
app.secret_key = "f3f46b84345dea28c1a294a3"


@app.route("/", methods=["GET", "POST"])
def home_page():
	return make_response({"test":"this is test end point"})
@app.route("/schedule/", methods=["GET","POST","PUT","DELETE"])
@app.route("/schedule/<ins_id>", methods=["GET"])
def set_schedule(ins_id=None):
	if request.method == "POST":
		data = request.get_json(force=True)
		task = data.get("task")
		days = data.get("days")
		instanceId = data.get("instanceId")
		print(data)
		url = "https://gvlm1oa781.execute-api.ap-south-1.amazonaws.com/default/instanceScheduler"
		req = requests.post(url,json={"task":task, "instanceId":instanceId,"days":days})
		print(req.text)
		print(data)
	if request.method == "PUT":
		data = request.get_json(force=True)
		task = data.get("task")
		days = data.get("days")
		instanceId = data.get("instanceId")
		print(data)
		url = "https://gvlm1oa781.execute-api.ap-south-1.amazonaws.com/default/instanceScheduler"
		req = requests.put(url,json={"task":task, "instanceId":instanceId,"days":days})
		print(req.text)
		print(data)
		
	if request.method == "GET":
		url = "https://gvlm1oa781.execute-api.ap-south-1.amazonaws.com/default/instanceScheduler"
		req = requests.get(url)
		print(req.text)
		#print(data)

	if request.method == "DELETE":
		data = request.get_json(force=True)
		#task = data.get("task")
		#days = data.get("days")
		instanceId = data.get("instanceId")
		url = "https://gvlm1oa781.execute-api.ap-south-1.amazonaws.com/default/instanceScheduler"
		req = requests.delete(url, json={"instanceId":instanceId})
		print(req.text)
		#print(data)
	return make_response({"response":req.json()})



if __name__ == '__main__':
	app.run(debug=True)