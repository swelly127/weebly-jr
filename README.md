========================
# WEEBLY TRIAL PROJECT #
========================

Welcome to my source code!

This project is made with <a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask</a> and MongoDB. It is hosted on Heroku and includes a few logging and notification plugins as well.

The content is stored in a nested array in the pages collection, and users are stored in the sessions collection. I've only stored the access_token (from google or fb), the user_id, and the generated weebly_token, which is a random selection of characters from the user's access_token.

TO TEST:
source venv/bin/activate
pip install -r requirements.txt 
foreman start web
