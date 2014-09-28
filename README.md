POKER 4701 PROJECT
===================

Most of this code is copied from another website I made using <a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask</a> and Postgres. It is hosted with Heroku and includes a few loggings and notification plugins as well. Most of the technologies used are lightweight and have very low learning curves, but we don't need everyone to understand all of the web code yet since our project will probably be graded on the AI logic of the agent, which can be worked on independently of the site logic. 

Models.py contains all of the AI logic and works independently of the other files. So far I've defined Card, Deck, Game, and Player but I'm not completely sure if that is the best way to do it. This is a very rough draft, so feel free to overwrite anything at this point.

We should also discuss how to model things in the database, which shouldn't take too long (I just want to implement a login and keep track of players and how many coins they have) — I could also implement the db layer on my own time if we run out of time.

Since this is an AI project the UI doesn't need to be perfect. I plan on working on this for fun after the class is over so for right now we only need to make it good enough to not fail 4701.

If you guys want to get started feel free to start looking through the code in models.py — I'm gonna figure out how to setup the rest of the site for now. I'm currently putting the final touches on our <a href="http://pokerbot.co">landing page</a>.

Let me know if you have any questions!

Jessica
