# <a href="http://weebly-junior.herokuapp.com">WEEBLY TRIAL PROJECT</a>#
========================

<b>Welcome to my source code! </b>

This project is made with <a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask</a> and MongoDB. It is hosted on Heroku and includes a few logging and notification plugins as well. The dependencies listed in README.md include all pip dependencies installed on my computer (generated with pip freeze > requirements.txt) and not all are used in this project.

The content is stored in a nested array in the pages collection, and users are stored in the sessions collection. I've only stored the access_token (from google or fb), the user_id, and the generated weebly_token, which is a random selection of characters from the user's access_token.

<b>TO TEST LOCALLY: </b><br>
source venv/bin/activate <br>
pip install -r requirements.txt <br>
foreman start web <br>

Api token for testing: <b>IJ6MXxAmiq </b> <br>
You only need a token if you are not logged in.<br>
Sample page ID for testing: <b>544a0774882819000754b501 </b><br>

# BUGS AND TODO #

[x] Ajax executing twice on keydown<br>
[x] Facebook Login<br>
[x] Edit buttons overlapping with text<br>
[x] Add API Key requirement to REST Api<br>
[x] Fix get all pages json<br>
[x] Handle ObjectId format error<br>
[x] Better API return values and JSON success functions<br>
[x] Reuse code and endpoints for Facebook and Google Logins<br>

[ ] Stop the aggressive login (logins without user clicking anything) without changing the token (Bug)<br>
[ ] Bind content deletions and make content updatable (FE Level 3) <br>
[ ] Figure out a better/scalable way to store content (BE Level 3)<br>
[ ] Make active tab do ajax call to display the active page rather than default (FE Level 3)<br>

# API ENDPOINTS #

| Endpoint | Description | Arguments |
| ---- | --------------- | ----- |
| GET /api/pages | Get all pages | api_token |
| GET /api/page/:id | Get a specific page | api_token |
| POST /api/pages | Create a new page | api_token, name (string), element (nested array)|
| PUT /api/page/:id | Update a specific page | api_token, name (string), element (nested array)|
| DELETE /api/page/:id | Delete a specific page | api_token |
| GET /api/me | JSON representation of logged in user's data | api_token |
| GET /logout | Logout | delete (boolean, revokes token if true) |
