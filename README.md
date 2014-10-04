POKER
=====

Most of this code is copied from another website I made using Flask (http://flask.pocoo.org/docs/0.10/tutorial/) and Postgres and hosted with Heroku, so no need to understand the code right now.

This was the most lightweight way I could think of to do this, all the technologies used have a very low learning curve.

Everything other than "models.py" almost everything is copied from the previous website right now. I can explain everything at our next meeting, but for now I think we should work on defining the classes we need:

So far I've defined Card, Deck, Game, and Player but I'm not completely sure if that is the best way to do it. This is a very rough draft, feel free to overwrite anything at this point.

We should also discuss how to model things in the database, which shouldn't take too long (I just want to implement a login and keep track of players and how many coins they have) — I can implement the db layer on my own time if needed.

Since this is an AI project the majority of our focus will be on the logic of our player (how it responds to different situations, what type of information it should store, etc.) and the UI probably doesn't need to be perfect. I plan on working on this for fun after the class is over so for right now we only need to make it good enough to not fail 4701 haha.

If you guys want to get started on the pokerbot (in models.py) that'd be great. I'm gonna figure out how to setup the site for now. 

— Jessica
