from flask import Flask, flash, redirect, render_template, session, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
import db
import tokens
load_dotenv()
import os


app = Flask(__name__)
mail= Mail(app)
app.secret_key = os.getenv('SECRET_KEY')

db_connection = db.db_connect()

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

# =============================================================================================================