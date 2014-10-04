POKER
=====

Most of the code here is copied from another website I made using <a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask</a> and Postgres. It is hosted with Heroku and includes a few logging and notification plugins as well. The technologies used are lightweight and have very low learning curves, but we don't need everyone to understand the web code since our project will be graded on the AI logic of the PokerBot, which can be worked on independently of the site. 

Models.py contains all of the AI logic and can be worked on independently. So far I've defined Card, Deck, Game, and Player but I'm not completely sure if that is the best approach. This is a very rough draft, so feel free to overwrite anything.

We should also discuss how to model things in the database, which shouldn't take too long. I'd like to implement a login and keep track of players, how many coins they have, and past games. The databases will need to be directly linked to the models.

Since this is an AI project the UI doesn't need to be perfect. I plan on continuing this project after the class is over but for right now we just need to make it work well enough not to fail 4701.

If you guys want to get started feel free to start looking through the code in models.py — I'm gonna figure out how to setup the rest of the site for now. I'm currently putting the final touches on our <a href="http://pokerbot.co">landing page</a>.

Let me know if you have any questions!

Jessica
