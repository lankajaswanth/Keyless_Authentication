from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from facedetector import faceencodingvalues
from flask_recaptcha import ReCaptcha
import db
import os


app = Flask(__name__)
mail= Mail(app)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('SECRET_KEY')

recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED = True,
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY'),
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY'),
	RECAPTCHA_SIZE = 'invisible',
	RECAPTCHA_THEME = "dark",
))

# RECAPTCHA_DATA_ATTRS = {'bind': 'recaptcha-submit', 'callback': 'onSubmitCallback', 'size': 'invisible'}

recaptcha = ReCaptcha()
recaptcha.init_app(app)


dbconnect = db.connect()

# =============================================================================================================

def mailing(tomail,username,token,no):
	if no == 1:
		x,y = "conformation Email","confirm_email"
	elif no == 2:
		x,y = "reset password","reset_password"
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
		msg.subject = x
		link = "https://adist.herokuapp.com/{}/{}".format(y,token)
		msg.html = "<div><h1>change password</h1><h1><a href='"+link+"'}>click me</a></h1></div>"
		msg.html = '''<div
		style="text-align:center;max-width:600px;background:rgba( 255, 255, 255, 0.25 );box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );backdrop-filter: blur( 4px );border-radius: 10px;border: 1px solid rgba( 255, 255, 255, 0.18 );">
			<h1>Adist</h1>
			<h2>Verification mail</h2>
			<h2>hi {} click the link below to conform your mail</h2>
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
		return render_template("index.html",user=session["user"])
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
		q = "select * from tempusers where email = '{}'".format(email)
		result = db.select(q)
		if len(result) == 0:
			flash("Invalid email")
			return redirect(url_for("login"))
		elif len(result) == 1:
			result = result[0]
			session["user"] = email
			return redirect(url_for("home"))
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
					q = "insert into tempusers(username,email,token,encodings) values('{}','{}','{}','{}')".format(username,email,"no",str(faceencodings.tolist()))
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

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


if __name__ == '__main__':
	app.run(debug=True,port=8000)