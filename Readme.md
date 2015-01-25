
Housing_task
============


RUNNING
====================================
>Mysql Databse settings--> src/zwitter/config.py (Change according to your databse settings, else mysql commands will fail due to auth error)

>sudo pip install -r requirements.txt

>python manage.py migrate

>python mange.py runserver

**Note If Databse tabels don't show up or python manage.py migrate fails, import schema.sql in your databse


Problem_statement
=================
>TWITTER­CLONE

You are required to develop a basic twitter­clone using Django/python (ONLY) with the database being
either MySQL or any other relational database. This app will enable users to login to their accounts and
do some basic Twitter like operations. Try using Twitter for understanding the flow.

The required functionalities are mandatory:

PRE­LOGIN

1) The Person should be able to signup for a very basic profile if he/she doesn’t have an existing
profile. Some basic profile details should be a prerequisite for signup.

2) The person should be able to sign­in with his credentials if he/she has an existing account.

3) All other functionalities of this App should only be accessible post­login.
POST­LOGIN

1) View a basic timeline consisting of the latest tweets only from the people being followed by the
currently logged­in user.

2) Ability to compose and post a tweet(post) of limited characters.

3) View the Profiles of other users which opens a view that displays all the tweets posted by that user,
view the basic profile details of that user and the ability to follow/unfollow the user.

4) The person should be able to view his/her profile as well which shows all the tweets posted by
themselves.

5) View the list of all people being followed.

6) View the list of all people that are the current user’s followers.

