#!/usr/bin/env python
import os
import json
import requests
import sendgrid
import datetime
import models
import settings
from settings import *
from models import *
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = secret_key

sg = sendgrid.SendGridClient(SENDGRID_USERNAME, SENDGRID_PASSWORD)

@app.route('/')
@app.route('/index.html')
def index():
    if session.get('user_id'):
        data = Users.query.filter_by(id=session['user_id']).first().serialize
        data['client_id'] = client_id
        data['signed_in'] = True
        return render_template('index.html', data=data)
    else:
        data = {'signed_in': False,
                'client_id': client_id}
        return render_template('index.html', data=data)

@app.route('/move', methods=["POST"])
def move():
    pass

@app.route('/new', methods=["POST"])
def new():
    user_id = request.form['user_id']

    payload = {
        "access_token": access_token,
        "note": note,
        "amount": amount,
        "user_id": user_id
    }

    url = "https://api.venmo.com/v1/payments"
    response = requests.post(url, payload)
    data = response.json()
    if 'error' in data:
        return jsonify(data)
    else:
        user = Users.query.filter_by(id=session['user_id']).first()
        user.balance = user.balance + amount
        depo = Updates(session['user_id'], "Deposit")
        depo.balance = user.balance
        depo.stock_percentage = user.stock_percentage

        depo.stock_change = amount * user.stock_percentage/100.0
        depo.bond_change = amount * user.bond_percentage/100.0

        db.session.add(depo)
        db.session.add(user)
        db.session.commit()

        text(user.venmo_metadata['display_name'] + " has just deposited " + str(amount))

        return jsonify({
            'message': "Successfully deposited $" + str(amount) + "!",
            'balance': user.balance,
            'type': 'Deposit',
            'stock_balance': "%.2f" % (user.balance * user.stock_percentage/100.0),
            'bond_balance': "%.2f" % (user.balance * user.bond_percentage/100.0),
            'stock_change': "%.2f" % depo.stock_change,
            'bond_change': "%.2f" % depo.bond_change,
            'timestamp': datetime.now().strftime("%B %d %Y %I:%M%p")
        })


@app.route('/deposit', methods=["POST"])
def deposit():
    access_token = session['access_token']
    note = "ShrubFund deposit at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = request.form['user_id']
    amount = float(request.form['amount'])

    payload = {
        "access_token": access_token,
        "note": note,
        "amount": amount,
        "user_id": user_id
    }

    url = "https://api.venmo.com/v1/payments"
    response = requests.post(url, payload)
    data = response.json()
    if 'error' in data:
        return jsonify(data)
    else:
        user = Users.query.filter_by(id=session['user_id']).first()
        user.balance = user.balance + amount
        depo = Updates(session['user_id'], "Deposit")
        depo.balance = user.balance
        depo.stock_percentage = user.stock_percentage

        depo.stock_change = amount * user.stock_percentage/100.0
        depo.bond_change = amount * user.bond_percentage/100.0

        db.session.add(depo)
        db.session.add(user)
        db.session.commit()

        text(user.venmo_metadata['display_name'] + " has just deposited " + str(amount))

        return jsonify({
            'message': "Successfully deposited $" + str(amount) + "!",
            'balance': user.balance,
            'type': 'Deposit',
            'stock_balance': "%.2f" % (user.balance * user.stock_percentage/100.0),
            'bond_balance': "%.2f" % (user.balance * user.bond_percentage/100.0),
            'stock_change': "%.2f" % depo.stock_change,
            'bond_change': "%.2f" % depo.bond_change,
            'timestamp': datetime.now().strftime("%B %d %Y %I:%M%p")
        })

@app.route('/withdraw', methods=["POST"])
def withdraw():
    access_token = SHRUBFUND_TOKEN
    note = "ShrubFund withdrawal at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_id = session["user_id"]
    amount = float(request.form['amount'])

    user = Users.query.filter_by(id=session['user_id']).first()
    if amount > user.balance:
        return jsonify({
            'error': {'message': "No u can't do that :("}
        })
    else:
        payload = {
            "access_token": access_token,
            "note": note,
            "amount": amount,
            "user_id": user_id
        }

        url = "https://api.venmo.com/v1/payments"
        response = requests.post(url, payload)
        data = response.json()
        if 'error' in data:
            return jsonify(data)
        else:
            user.balance = user.balance - amount
            draw = Updates(session['user_id'], "Withdraw")
            draw.balance = user.balance
            draw.stock_percentage = user.stock_percentage

            draw.stock_change = amount * -user.stock_percentage/100.0
            draw.bond_change = amount * -user.bond_percentage/100.0

            db.session.add(draw)
            db.session.add(user)
            db.session.commit()

            text(user.venmo_metadata['display_name'] + " has just withdrawn " + str(amount))

            return jsonify({
                'message': "Successfully withdrew $" + str(amount) + " to venmo account.",
                'balance': user.balance,
                'stock_balance': "%.2f" % ((user.balance * user.stock_percentage)/100.0),
                'bond_balance': "%.2f" % ((user.balance * user.bond_percentage)/100.0),
                'stock_change': "%.2f" % draw.stock_change,
                'bond_change': "%.2f" % draw.bond_change,
                'type': 'Withdraw',
                'timestamp': datetime.now().strftime("%B %d %Y %I:%M%p")
            })

@app.route('/get_payments', methods=["POST"])
def get_payments():
    updates = Updates.query.filter_by(user_id=session['user_id']).order_by(Updates.timestamp.desc())
    data = [u.serialize for u in updates]
    print data[0]
    return jsonify({"data": data})

@app.route('/auth')
def auth():
    AUTHORIZATION_CODE = request.args.get('code')
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": AUTHORIZATION_CODE
        }
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()

    _id = response_dict.get('user')['id']

    session['user_id'] = _id
    session['access_token'] = response_dict.get('access_token')

    user = Users.query.filter_by(id=_id).first()

    if user is None:
        user = Users(_id)

    user.venmo_metadata = response_dict.get('user')
    user.access_token = response_dict.get('access_token')
    user.email = response_dict.get('user')['email']
    db.session.add(user)
    db.session.commit()

    text(response_dict.get('user')['display_name'] + " is now using ShrubFund!")

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/settings')
def settings():
    if session.get('user_id'):
        data = Users.query.filter_by(id=session['user_id']).first().serialize
        return render_template('settings.html', data=data)
    else:
        data = {'signed_in': False}
        return render_template('index.html', data=data)

@app.route('/update_holdings', methods=['POST'])
def update_holdings():
    user = Users.query.filter_by(id=session["user_id"]).first()

    stock_change = (int(request.form['stock']) - user.stock_percentage)/100.0 * user.balance
    user.stock_percentage = request.form['stock']

    update = Updates(session["user_id"], "Portfolio Change")
    update.stock_percentage = request.form['stock']
    update.balance = user.balance

    update.stock_change = stock_change
    update.bond_change = -stock_change

    db.session.add(user)
    db.session.add(update)
    db.session.commit()
    return "Done"

# texts me phone if it is not a test environment
def text(txt):
    if 'VIRTUAL_ENV' not in os.environ:
        requests.post(BLOWERIO_URL+'/messages', data={
            'to': OWNER_NUMBER, 
            'message': txt
        })

if __name__ == "__main__":
	app.run(debug=True, port=4000)
