#!/usr/bin/env python
import os
import pymongo
import requests
import sendgrid
from flask import Flask, flash, redirect, render_template, request, url_for
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'sushi4ever'

os.environ["BLOWERIO_URL"]="https://fd37f239-0c12-460c-a976-9b93892b075b:RKYMWFlMeDlMXFr-Rl9BAg@api.blower.io/"
os.environ["SENDGRID_USERNAME"]="app27692256@heroku.com"
os.environ["SENDGRID_PASSWORD"]="e0linoa9"
os.environ["MONGOLAB_URI"]="mongodb://heroku_app27692256:t7tuhrdvgemhhghb15jig0tvcq@ds037827.mongolab.com:37827/heroku_app27692256"
os.environ["MONGOLAB_DB"]="heroku_app27692256"

client = MongoClient(os.environ["MONGOLAB_URI"])
sg = sendgrid.SendGridClient(os.environ['SENDGRID_USERNAME'], os.environ['SENDGRID_PASSWORD'])

def text_notify(email):
		requests.post(os.environ['BLOWERIO_URL']+'/messages', data={
			'to': '+14154907810', 
			'message': email + " has signed up for beta!"
		})

def email_notify(email):
		message = sendgrid.Mail(to='jessicashu127@gmail.com', 
								text="Congrats! Welcome them to ShrubFund.",
								subject=email + " has signed up for beta!", 
								from_email='ShrubFund')
		print sg.send(message) # returns status, msg

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		email = request.form['email']
		if len(email) > 1:
			client.heroku_app27692256.beta_emails.remove({"email": email}) 
			client.heroku_app27692256.beta_emails.save({"email": email, "date": datetime.now().strftime("%B %d, %Y %I:%m %p")})
			email_notify(email)
			text_notify(email)
		if email.find("@") < email.rfind(".") and email.rfind != -1:
			return render_template('index.html', msg="thanks")
		else:
			flash('Please enter a valid email')
			return redirect('/home#signup')
	else:
		return render_template('index.html')

@app.route('/faq')
def faq():
	return render_template('faq.html')

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
	if request.method == 'POST':
		email = request.form['email']
		if len(email) > 1:
			client.heroku_app27692256.beta_emails.save({"email": email, "date": datetime.now().strftime("%B %d, %Y %I:%m %p")})
			notify(email)
		if email.find("@") < email.rfind(".") and email.rfind != -1:
			flash("Thanks. We'll be in touch shortly.")
			return redirect('/portfolio#signup')
		else:
			flash('Please enter a valid email')
			return redirect('/portfolio#signup')
	else:
		return render_template('portfolio.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/legal')
def legal():
	return render_template('legal.html')

@app.route('/privacy')
def privacy():
	return render_template('privacy.html')

if __name__ == "__main__":
	app.run(debug=True, port=4000)
