#!/usr/bin/python3
import requests, csv, json
iq_session = requests.Session()
iq_session.auth = requests.auth.HTTPBasicAuth("admin", "admin123")
iq_url = "http://localhost:8070"

def pp(c):
	print( json.dumps(c, indent=4) )

roles = {}
users = {}

url = f'{iq_url}/api/v2/applications/roles'
resp = iq_session.get(url).json()["roles"]
for role in resp:
	roles.update({role["id"]: role["name"]})

url = f'{iq_url}/api/v2/organizations'
organizations = iq_session.get(url).json()["organizations"]
for org in organizations:
	org_id = org["id"]
	org_name = org["name"]
	url = f'{iq_url}/api/v2/organizations/{org_id}/roleMembers'
	resp = iq_session.get(url).json()["memberMappings"]
	for role in resp:
		role_name = roles[role["roleId"]]
		for member in role["members"]:
			if member["ownerId"] == org_id:
				name = member["userOrGroupName"]
				member_type = member["type"]
				print(f'{org_name} - {role_name} - {member_type} - {name}')
				if member_type == "USER":
					if not name in users.keys():
						users.update({name:[]})
					users[name].append({"org":org_name, "role":role_name})

pp(users)



