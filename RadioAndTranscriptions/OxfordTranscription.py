import http.client, urllib.parse, json
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re

def getOxfordDataFromWAVAudio(filename):
	#using microsoft sample code
	#Note: Sign up at http://www.projectoxford.ai to get a subscription key.
	#Search for Speech APIs from Azure Marketplace.
	#Use the subscription key as Client secret below.
	clientId = "itsme"
	clientSecret = "e2e7bb45f91d4e50ad35501ebaa08f14"
	ttsHost = "https://speech.platform.bing.com"

	params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': ttsHost})

#	print ("The body data: %s" %(params))

	headers = {"Content-type": "application/x-www-form-urlencoded"}

	AccessTokenHost = "oxford-speech.cloudapp.net"
	path = "/token/issueToken"

	# Connect to server to get the Oxford Access Token
	conn = http.client.HTTPSConnection(AccessTokenHost)
	conn.request("POST", path, params, headers)
	response = conn.getresponse()
	#print(response.status, response.reason)

	data = response.read()
	conn.close()
	accesstoken = data.decode("UTF-8")
	#print ("Oxford Access Token: " + accesstoken)

	#decode the object from json
	ddata=json.loads(accesstoken)
	access_token = ddata['access_token']

	# Read the binary from wave file
	f = open(filename,'rb')
	try:
		body = f.read();
	finally:
		f.close()

	headers = {"Content-type": "audio/wav; samplerate=8000",
		"Authorization": "Bearer " + access_token}

	#Connect to server to recognize the wave binary
	conn = http.client.HTTPSConnection("speech.platform.bing.com")
	conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=en-US&device.os=wp7&version=3.0&format=xml&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
	response = conn.getresponse()
	#print(response.status, response.reason)
	data = response.read()

	conn.close()

	return data


def transcribeAndWriteToFile(audioFilePath, number):
	timeString = datetime.utcnow().isoformat()
	data = getOxfordDataFromWAVAudio(audioFilePath)
	datastr = data.decode('utf-8')

#	print('Data String Starting: ')
#	print(datastr)
#	print('End data string.')


	transcribedText = ''
	confidenceString = 'NOSPEECH'
	confidence = -1

	root = ET.fromstring(datastr)
	for result in root.iter('result'):
		for text in result.iter('name'):
			transcribedText = text.text
		for conf in result.iter('property'):
			confidenceString = conf.attrib['name']
		for conf in result.iter('confidence'):
			confidence = float(conf.text)


	print('ID: {0}'.format(number))
	print('Confidence Level: {1}, {2}\nTranscribed Text: "{0}"'.format(
		transcribedText, confidenceString, confidence))
	print()

	#For testing Purposes
	#transcribedText = 'fire has a gun'

	if transcribedText != '':
		#convert to percentage in a string
		if confidence == -1: 'NA'
		else: confidence = confidence = str(int(confidence * 100 )) + '%'
		
		#look for tags in the transcription
		messageType = ''
		types = ('fire', 'gun', 'dead', 'not breathing', 'shot')
		for type in types:
			if type in transcribedText:
				messageType = type
		
		#remove the "<profanity>" tags
		transcribedText = re.sub('<profanity>', '', transcribedText)
		transcribedText = re.sub('</profanity>', '', transcribedText)

		jstr = json.dumps({"message":{"body": transcribedText, "message_type":messageType, 'confidence_%': confidence,
			'confidence_string': confidenceString, "transcribed_at": timeString, "locale":"Pittsburgh"}})

#		print("Writing to file. ", jstr)

		if not os.path.exists("json data files/"):
			os.mkdir("json data files/")

		outfile = open('json data files/message{0}.txt'.format(number), 'wt')
		outfile.write(jstr)
		outfile.close()
