========================
# WEEBLY TRIAL PROJECT #
========================

Welcome to my source code!

This project is made with <a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask</a> and MongoDB. It is hosted on Heroku and includes a few logging and notification plugins as well. The dependencies listed in README.md include all pip dependencies installed on my computer (generated with pip freeze > requirements.txt) and not all are used in this project.

The content is stored in a nested array in the pages collection, and users are stored in the sessions collection. I've only stored the access_token (from google or fb), the user_id, and the generated weebly_token, which is a random selection of characters from the user's access_token.

TO TEST: <br>
source venv/bin/activate <br>
pip install -r requirements.txt <br>
foreman start web <br>

# BUGS AND TODO #

[x] Ajax executing twice on keydown<br>
[x] Facebook Login<br>
[x] Edit buttons overlapping with text<br>
[x] Add API Key requirement to REST Api<br>
[x] Fix get all pages json<br>
[x] Handle ObjectId format error<br>
[x] Better API return values and JSON success functions<br>
[x] Reuse code and endpoints for Facebook and Google Logins<br>

[ ] Stop the aggressive login without changing the token<br>
[ ] Bind content deletions and make content updatable<br>
[ ] Figure out a better way to store content and write API docs<br>
[ ] Make active tab do ajax call to display the active page rather than default<br>

# API ENDPOINTS #

| Endpoint | Description |
| ---- | --------------- |
| GET /api/pages | Get all pages |
| GET /api/page/:id | Get a specific page |
| POST /api/pages | Create a new page |
| PUT /api/page/:id | Update a specific page |
| DELETE /api/page/:id | Delete a specific page |
