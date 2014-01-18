flask-template
==============

Template for starting project with Flask using peewee as ORM



Why?
=====

Because I always start with just one file and end up with the models, the admin, the views and everything else in the same file, which makes it difficult to separate things after



Components
===========

Rest API thanks to flask-peewee

Admin interface thanks to flask-peewee

User class used for authentication and used by the Admin interface

Different configs so you can use Sqlite on local development but have the production config stored. With one line you can change database and debug status

Everything separated, models on models, views on vies, admin views on admin, api configuration on api

A base template with bootstrap, jquery and font awesome already loaded, a message div for flashing error/success messages with flash() and display them with bootstrap alert colors + jquery slideDown/Up

A main.css already linked from the base template so you can start cssing


Pull requests?
===============

Not sure if I would accept any as this is meant to be used by me, so I will add stuff that probably I find useful, but if you got any question, request or whatever jsut contact me.
