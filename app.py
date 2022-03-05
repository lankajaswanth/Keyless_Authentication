import cv2
import crypto
from flask import Flask, Response, render_template, request, redirect, session, url_for, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from facedetector import faceencodingvalues, predata, detect
import tokens
import db
import os


app = Flask(__name__)
mail= Mail(app)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('SECRET_KEY')


dbconnect = db.connect()


global recorded,cap
recorded = "NO"

# =============================================================================================================

def mailing(tomail,username,token):
	try:
		app.config['MAIL_SERVER']='smtp.gmail.com'
		app.config['MAIL_PORT'] = 465
		app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
		app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')
		app.config['MAIL_USE_TLS'] = False
		app.config['MAIL_USE_SSL'] = True
		mail = Mail(app)
		msg = Message('Hello', sender = os.getenv('EMAIL'), recipients = [tomail])
		msg.body = "<h1>Hello Flask message sent from Flask-Mail</h1>"
		msg.subject = "Login to your account"
		link = "http://127.0.0.1:8000/logincheck/{}".format(token)
		msg.html = "<div><h1>Login to your account</h1><h1><a href='"+link+"'}>click here</a></h1></div>"
		msg.html = '''<div
		style="text-align:center;max-width:600px;background:rgba( 255, 255, 255, 0.25 );box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );backdrop-filter: blur( 4px );border-radius: 10px;border: 1px solid rgba( 255, 255, 255, 0.18 );">
			<h1>Authenticator</h1>
			<h2>Login to your account</h2>
			<h2>hi {} click the link below to Login to your account</h2>
			<h3><a href='{}' >Click Here</a></h3>
			<p>Copy paste in browser if the above link is not working: {}</p>
		</div>'''.format(username,link,link)
		mail.send(msg)
		return True
	except:
		return False

# ============================================================================================================

@app.route("/")
@app.route("/home")
def home():
	if "user" in session:
		if "verify" in session:
			return render_template("index.html", user = session["user"])
		else:
			return render_template("verify.html", user = session["user"])
	elif "admin" in session:
		return redirect(url_for("admin"))
	else:
		return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
	if request.method == "GET":
		if "user" in session:return redirect(url_for("home"))
		return render_template("login.html",RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY'))
	if request.method == "POST":
		email = request.form.to_dict()["email"]
		q = "select username,email from tempusers where email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 0:
			flash("Invalid email")
			return redirect(url_for("login"))
		elif len(result) == 1:
			result = result[0]
			username,email = result[0],result[1]

			token = tokens.generate_confirmation_token(email)
			q = "update tempusers set token = '{}' where email = '{}'".format(token,email)
			if db.insert(q):
				if mailing(email,username,token):
					flash("Check your email to for login link")
					return redirect(url_for("login"))
				else:
					flash("Something went wrong during mailing")
					return redirect(url_for("login"))
			else:
				flash("Something went wrong with our database")
				return redirect(url_for("login"))

			return redirect(url_for("login"))
		else:
			flash("Something went wrong")
			return redirect(url_for("login"))

# ============================================================================================================

@app.route("/logincheck/<token>")
def logincheck(token):
	email = tokens.confirm_token(token)
	if email == "The token has expired":
		flash("The token has expired")
		return redirect(url_for("login"))
	elif email == "the token is invalid":
		flash("the token is invalid")
		return redirect(url_for("login"))
	elif email:
		q = "select username,email,token from tempusers where email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 1:
			result = result[0]
			username,email = result[0],result[1]
			if token == result[2]:
				q = "update tempusers set token = 'no' where email = '{}'".format(email)
				if db.insert(q):
					session["user"] = email
					return redirect(url_for("home"))

				else:
					flash("Something went wrong with our database")
					return redirect(url_for("login"))
			else:
				flash("use the link that was last sent to your email")
				return redirect(url_for("login"))
		else:
			flash("Something went wrong")
			return redirect(url_for("login"))
	else:
		flash("Something went wrong")
		return redirect(url_for("login"))


# ============================================================================================================

@app.route("/admin",methods=["GET","POST"])
def admin():
	if request.method == "GET":
		q = "select username,email from tempusers"
		details = db.select(q)
		if "admin" in session:return render_template("admin/admin.html",user=session["admin"],details = details)
		else:return render_template("admin/adminlogin.html")
	if request.method == "POST":
		values = request.form.to_dict()
		mode = values["mode"]
		if mode == "login":
			email,password = values["email"],values["password"]
			if email == "perumallasasank123@gmail.com" and password == "12345":
				session["admin"] = email
				return redirect(url_for("admin"))
			else:
				flash("Invalid email or password")
				return redirect(url_for("admin"))
		if mode == "add":
			username = values["username"]
			email = values["email"]

			q = "select * from tempusers where email = '{}'".format(email)
			result = db.select(q)
			if len(result) == 0:
				q = "select * from tempusers where username = '{}'".format(username)
				result = db.select(q)
				if len(result) == 0:
					file = request.files['file']
					if file:
						filename = username+os.path.splitext(secure_filename(file.filename))[1]
						pathtoimg = os.path.join(app.config['UPLOAD_FOLDER'], filename)
						file.save(pathtoimg)
					faceencodings,facelocs = faceencodingvalues(pathtoimg)
					if len(facelocs)==0:
						flash("No face detected")
						return redirect(url_for("admin"))
					q = "insert into tempusers(username,email,token,encodings) values('{}','{}','{}','{}')".format(username,email,"no",crypto.encryption(str(faceencodings.tolist())))
					db.insert(q)
					flash("User added")
					return redirect(url_for("admin"))
				elif len(result) == 1:
					flash("Username already exists")
					return redirect(url_for("admin"))
				else:
					flash("Something went wrong")
					return redirect(url_for("admin"))
			elif len(result) == 1:
				flash("Email already exists")
				return redirect(url_for("admin"))
			else:
				flash("Something went wrong")
				return redirect(url_for("admin"))


# ============================================================================================================

cap = cv2.VideoCapture(0)
# =============================for attendence recording============================================================================================
# def gen_frames(email):
# 	global recorded,cap
# 	cap = cv2.VideoCapture(0)
# 	while True:
# 		print("================yeilding frame=====================================================================")
# 		sucess,img = cap.read()
# 		cv2.imshow('Video window', img)
# 		frame,recorded = detect(img,email)
# 		if recorded == "YES":
# 			session["verify"] = "True"
# 			print(recorded)
# 			break
def gen_frames(email):
	global recorded,cap
	# predata(regnosofstudent)
	while True:
		sucess,img = cap.read()
		(frame,ans) = detect(img,email)
		recorded = ans
		if recorded == "YES":
			print("verified*******************************************************************************************************************************")
			break
		yield(b'--frame\r\n'
					b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	print("yield condition exit")
	cap.release()

@app.route("/video_feed")
def video_feed():
	predata(session["user"])
	return Response(gen_frames(session["user"]),
					mimetype='multipart/x-mixed-replace; boundary=frame')

# ============================================================================================================

@app.route('/recorde')
def recorde():
	global recorded
	if recorded == "YES":
		return jsonify("YES")
	else:return jsonify("NO")

@app.route('/recorddone', methods = ['POST', 'GET'])
def recorddone():
	global recorded
	cap.release()
	recorded = "NO"
	if request.method == 'GET':
		# return session["verify"]
		session["verify"] = "True"
		print("session verify========================================================")
		if "verify" in session:
			print("yes")
		else:
			print("no")
		return redirect(url_for("home"))


# ============================================================================================================

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
	flash("Page not found")
	return redirect("/")


if __name__ == '__main__':
	app.run(debug=True,port=8000)