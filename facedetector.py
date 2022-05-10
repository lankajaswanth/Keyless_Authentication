from base64 import encode
import face_recognition
import numpy as np
import cv2
import db
import crypto

dbconnect = db.connect()

global knownencodings,count,sub
knownencodings =[]
count = 0
sub=""

def faceencodingvalues(img):
	print("===============start=====================================================")
	imgload = face_recognition.load_image_file(img)
	imgload = cv2.cvtColor(imgload,cv2.COLOR_BGR2RGB)
	try:
		faceloc = face_recognition.face_locations(imgload)[0]  # (260, 825, 528, 557)
	except:
		return [],[]
	encodeimg = face_recognition.face_encodings(imgload)[0]
	print("===============faceloc=====================================================")
	print(faceloc)
	print("==================encodeimg==================================================")
	print(encodeimg)

	return (encodeimg,faceloc)



def predata(email):
	encodinglist = []
	emaillist = []
	q = "select email,encodings from tempusers"
	result = db.select(q)
	for i in result:
		emaillist.append(i[0])
		arr = crypto.decryption(i[1])
		arr = np.array(eval(arr))
		encodinglist.append(arr)
	global knownencodings,count
	knownencodings = encodinglist
	count = emaillist.index(email)


def detect(img,email):
	imgS = cv2.resize(img,(0,0),None,0.25,0.25)
	imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
	facesS = face_recognition.face_locations(imgS)
	encodeS = face_recognition.face_encodings(imgS,facesS)

	for encodeFace,faceLoc in zip(encodeS,facesS):
		matches = face_recognition.compare_faces(knownencodings,encodeFace)
		faceDis = face_recognition.face_distance(knownencodings,encodeFace)
		matchindex = np.argmin(faceDis)
		# print("=======matchindex========================================")
		print(matchindex)
		print(count)
		print(matches[matchindex])
		print(faceDis[matchindex])
		if matches[matchindex] and count == matchindex and faceDis[matchindex]<0.6:
			print("================detect=================================================================")
			ret,buffer = cv2.imencode('.jpg',img)
			frame = buffer.tobytes()
			return (frame,"YES")
	ret,buffer = cv2.imencode('.jpg',img)
	frame = buffer.tobytes()
	return (frame,"NO")