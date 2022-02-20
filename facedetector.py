import face_recognition
import numpy as np
import cv2

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
	# print(faceloc)
	print("==================encodeimg==================================================")
	# print(encodeimg)

	return (encodeimg,faceloc)