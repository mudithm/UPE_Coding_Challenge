import requests, json

currX = 0
currY = 0

def returnPos(xpos, ypos):
	global currX, currY
	if (currX > xpos):
		while(currX != xpos):
			(requests.post(API_url + "/game?token=" + token, data=json.dumps(tryLEFT), headers=postHeaders))
			currX -= 1
	else:
		while(currX != xpos):
			(requests.post(API_url + "/game?token=" + token, data=json.dumps(tryRIGHT), headers=postHeaders))
			currX += 1

	if (currY > ypos):
		while(currY != ypos):
			(requests.post(API_url + "/game?token=" + token, data=json.dumps(tryUP), headers=postHeaders))
			currY -= 1
	else:
		while(currY != ypos):
			(requests.post(API_url + "/game?token=" + token, data=json.dumps(tryDOWN), headers=postHeaders))
			currY += 1


def findSolution(array, xpos, ypos, width, height):
	global currX, currY

	array[ypos][xpos] = 1
	#print (array)

	# Check by going right first
	if xpos + 1 < width and visited[ypos][xpos + 1] != 1:
		nStep = (requests.post(API_url + "/game?token=" + token, data=json.dumps(tryRIGHT), headers=postHeaders)).json()
		if nStep["result"]	== "END":
			return True
		elif nStep["result"] == "SUCCESS":
			currX += 1
			if findSolution(array, xpos+1, ypos, width, height):
				return True

	# return to original position
	returnPos(xpos, ypos)



	# Check Down
	if ypos + 1 < height and visited[ypos+1][xpos] != 1:
		nStep = (requests.post(API_url + "/game?token=" + token, data=json.dumps(tryDOWN), headers=postHeaders)).json()
		if nStep["result"]	== "END":
			return True
		elif nStep["result"] == "SUCCESS":
			currY += 1
			if findSolution(array, xpos, ypos+1, width, height):
				return True


	# return to original position
	returnPos(xpos, ypos)


	# Check Left
	if xpos - 1 > -1 and visited[ypos][xpos-1] != 1:
		nStep = (requests.post(API_url + "/game?token=" + token, data=json.dumps(tryLEFT), headers=postHeaders)).json()
		if nStep["result"]	== "END":
			return True
		elif nStep["result"] == "SUCCESS":
			currX -= 1
			if findSolution(array, xpos-1, ypos, width, height):
				return True

	# return to original position
	returnPos(xpos, ypos)


		# Check Up
	if ypos - 1 > -1 and visited[ypos-1][xpos] != 1:
		nStep = (requests.post(API_url + "/game?token=" + token, data=json.dumps(tryUP), headers=postHeaders)).json()
		if nStep["result"]	== "END":
			return True
		elif nStep["result"] == "SUCCESS":
			currY -= 1
			if findSolution(array, xpos, ypos-1, width, height):
				return True

	# return to original position
	returnPos(xpos, ypos)


	#print(False)
	return False






# General Request info
API_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com"
payload = {'uid':'404937201'}
postHeaders = {'content-type': 'application/json'}
getHeaders = {'content-type': 'application/x-www-form-urlencoded'}

# Data for the action post requests
tryUP = {"action":"UP"}
tryDOWN = {"action":"DOWN"}
tryLEFT = {"action":"LEFT"}
tryRIGHT = {"action":"RIGHT"}

# get tokem
r = requests.post(API_url + "/session", data=json.dumps(payload), headers=postHeaders)
token = r.json()["token"]
stat = ""
# Loop to solve all 12 mazes
while stat != "FINISHED":

	# get information about current maze
	gameStatus = (requests.get(API_url + "/game?token=" + token, headers=getHeaders)).json()
	if gameStatus["status"] == "FINISHED":
		stat = "FINISHED"
		break	
	width = gameStatus["maze_size"][0]
	height = gameStatus["maze_size"][1]
	xpos = gameStatus["current_location"][0]
	ypos = gameStatus["current_location"][1]

	visited = [[0 for j in range(width)] for k in range(height)]


	findSolution(visited, xpos, ypos, width, height)
	visited.clear()



	
		



		