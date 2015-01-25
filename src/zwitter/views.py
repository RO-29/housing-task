import MySQLdb
import MySQLdb.cursors
import json
import time
import os
import hashlib
import urllib2
import requests
import pdb
import re
import datetime
from auth import *
from settings import *
from config import *
from models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf
from django.http import *
from django.shortcuts import render, redirect


#not using django default models to store values in databse, instead using mysql default lib for python for our db operarions
#returns the mysql constructor Object
def DB_Obj():
    db_obj = MySQLdb.connect(HOST,USERNAME,PASSWORD,DATABASE)
    return db_obj
#####################################################################

#Secret key for hashing user password, not that secure but Ok!
def salt():
        return 'zwitter_1234'

#Encode function for encoding User Password
def encode(password):
        return hashlib.md5(salt() + password).hexdigest()
#######################################################################




######################################################################
#Helper functions to query Databse
######################################################################


def get_tweet_count(uid):
    DB =DB_Obj()
    cursor = DB.cursor()
    query = 'Select count(*) from tweets WHERE uid_id= %s'% uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows[0] 

def get_followers_count(uid):
 
    DB =DB_Obj()
    cursor = DB.cursor()
    query = 'Select count(*) from followers WHERE uid_id= %s'%uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows[0] 

def get_following_count(uid):
     
    DB =DB_Obj()
    cursor = DB.cursor()
    query = 'Select count(*) from following WHERE uid_id= %s'%uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows[0] 

def get_following(uid):
     
    DB =DB_Obj()
    cursor = DB.cursor()
    query = 'Select * from following WHERE uid_id= %s'%uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows

def get_followers(uid):
     
    DB =DB_Obj()
    cursor = DB.cursor()
    query = 'Select * from followers WHERE uid_id= %s'%uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows 

def get_handle(uid):
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "SELECT  * FROM users WHERE uid='%s'" %uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows

def get_uid(handle):
     
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "SELECT * FROM users WHERE handle='%s'" %handle
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows[0][0]

def get_user(uid):
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "Select * from users WHERE uid= '%s'"%uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows

def follows_u(request,uid):
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "SELECT * FROM followers WHERE follower_id='%s' AND uid_id='%s'" %(uid,request.session['uid'])
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    if rows: 
        return True
    else:
        return False

def u_follow(request,uid):
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "SELECT * FROM following WHERE following_id='%s' AND uid_id='%s'" %(uid,request.session['uid'])
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    if rows: 
        return True
    else:
        return False

def get_tweets(uid):
     
    DB =DB_Obj()
    cursor = DB.cursor()
    query = "SELECT * FROM tweets WHERE uid_id='%s'" %uid
    cursor.execute(query)
    rows = cursor.fetchall()
    DB.commit()
    DB.close()
    return rows

##########################################################
#End Of helper functions
##########################################################



#Index page , Serves as starting path for our app
#We check if user is logged in or not ,decorator defined in auth.py

@auth_check
def index(request):
    return render(request,'timeline.html')
#######################################################################


#Gets tweets for logged in user timeline from his/her followers tweets

@csrf_exempt
def get_tweets_timeline(request):
 response={}
 tweets=[]
 total_followers = get_followers(request.session['uid'])

 for follower in total_followers:
      tweets+=get_tweets(follower[1])

 tweets = sorted(tweets, key=lambda p: p[1], reverse=True)
 i=0
 for tweet in tweets:
  resp = {}
  user_info = get_handle(tweet[3])[0]
  timestamp = str(tweet[1].time())+"  "+str(tweet[1].date())
  name = user_info[1]+" "+user_info[2]
  resp['msg'] = tweet[2]
  resp['time']=timestamp
  resp['name']=name 
  resp['handle']= user_info[4]
  response[i]=resp
  i+=1
 return HttpResponse(json.dumps(response), content_type="application/json") 

#######################################################################

#tweets and profile info of user which is not the logged in user
@csrf_exempt
def other_user(request):
   DB = DB_Obj()
   cursor = DB.cursor() 
   response={} 
   tweets={}
   handle = request.POST.get('user')
   uid = get_uid(handle)

   tweets_all = get_tweets(uid)
   tweets_all = sorted(tweets_all, key=lambda p: p[1], reverse=True)

   i=0
   for row in tweets_all:
	  tweet = {}
	  timestamp = str(row[1].time())+"  "+str(row[1].date())
	  name = get_user(uid)[0][1]+" "+get_user(uid)[0][2]
	  tweet['msg'] = row[2]
	  tweet['time']=timestamp
	  tweet['name']=name
	  response[i]=tweet
	  i+=1
   DB.commit()
   DB.close()

   user = get_user(uid)[0]
   #pdb.set_trace()
   following_count = get_following_count(uid) 
   followers_count = get_followers_count(uid)
   if uid==request.session['uid']:
      current_user=True
   else:
      current_user=False
   response['userDetails']={'name':user[1]+" "+user[2],'about':user[6],'followers':followers_count,'following':following_count,'count':get_tweet_count(uid),'handle':handle,"u_fl":u_follow(request,uid),"fl_u":follows_u(request,uid),'cr':current_user}
   return HttpResponse(json.dumps(response), content_type="application/json")  

#######################################################################


#gets Current user tweets and return response conataining formatted data
@csrf_exempt
def get_tweets_me(request):
 DB =DB_Obj()
 response={} 
 tweets={}
 cursor = DB.cursor()
 query = 'Select * from tweets WHERE uid_id= %s'%request.session['uid']
 cursor.execute(query)
 rows = cursor.fetchall()
 rows = sorted(rows, key=lambda p: p[1], reverse=True)
 i=0
 for row in rows:
  tweet = {}
  timestamp = str(row[1].time())+"  "+str(row[1].date())
  name = request.session['name']
  tweet['msg'] = row[2]
  tweet['time']=timestamp
  tweet['name']=name
  response[i]=tweet
  i+=1
 DB.commit()
 DB.close()
 response['userDetails']={'name':request.session['name'],'about':request.session['about'],'followers':request.session['followers'],'following':request.session['following'],'count':request.session['tweet_count'],'handle':request.session['handle']}
 return HttpResponse(json.dumps(response), content_type="application/json")  

#######################################################################


#Renders profile page of current user
@auth_check
def profile(request):
 return render(request,'profile.html')

#######################################################################

#Anonumous function, used for testing
def test(request):
 response={}
 return HttpResponse(json.dumps(response), content_type="application/json") 

#######################################################################

@csrf_exempt
def list_(request): 
   response={}
   get = request.GET.get('get')
   handle = request.GET.get('handle')
   uid = get_uid(handle)
   if get=='followers':
    res = get_followers(uid)
   else:
    res = get_following(uid)
   i=0
   for ab in res:
       user = get_user(ab[1])
       for row in user: 
        users={}
        users['name']=row[1]+" "+row[2]
        users['handle']=row[4]
        response[i]=users
        i+=1 
   user = get_user(uid)[0]
   following_count = get_following_count(uid) 
   followers_count = get_followers_count(uid)
   
   if uid==request.session['uid']:
      current_user=True
   else:
      current_user=False
   response['userDetails']={'name':user[1]+" "+user[2],'about':user[6],'followers':followers_count,'following':following_count,'count':get_tweet_count(uid),'handle':handle,"u_fl":u_follow(request,uid),"fl_u":follows_u(request,uid),'cr':current_user}
   return HttpResponse(json.dumps(response), content_type="application/json") 

#######################################################################

@auth_check
def followers_render(request,handle):
  return render(request,'followers.html')

#######################################################################
@auth_check
def following_render(request,handle):
  return render(request,'following.html')
#######################################################################
@auth_check
def home(request):
    return render(request,'timeline.html')
#######################################################################
def check_login(request):
    if(request.session.get('logged',True)):
       print 'Already logged in'
       return True
    else:
      return False
####################################################################### 

#Login_signup form ,renders login and signup page if user is not logged in
def login_signup(request):
   if (check_login(request)==False):
    return render(request,'login.html')
   else:
    return HttpResponseRedirect('/')

@auth_check
def user_profile(request,handle):
    return render(request,'user_profile.html')



@csrf_exempt
@auth_check
def tweet_post(request):
 response={}
 #pdb.set_trace()
 if request.method=='POST':
    date = datetime.datetime.now()
    tweet = str(request.POST.get('tweet'))

    try:

         DB = DB_Obj() 
         cursor = DB.cursor()
         query = """INSERT INTO tweets (posted,tweet,uid_id) VALUES(%s,%s,%s)""" 
         params = (datetime.datetime.now().strftime(' %H:%M:%S %d-%m-%Y'),tweet,int(request.session['uid']))
         cursor.execute(query,params)
         DB.commit()
	 DB.close()
         #pdb.set_trace()
         response['result']="Success"
         response['message'] = 'Tweet posted!'

         return HttpResponse(json.dumps(response), content_type="application/json")
    
    except MySQLdb.Error, e:
                print str(e)
                response['result'] = 'failed'
		response['message']='Some Internal error,Try Again!'
                return HttpResponse(json.dumps(response), content_type="application/json")
 else:
  response['result']='failed'
  response['message']='Not a valid post request'
  return HttpResponse(json.dumps(response), content_type="application/json")  



@csrf_exempt
def login_process(request):
  
    #Response we will return
    response={}
    #pdb.set_trace()

    #POST request, all except post are ignored
    if request.method == 'POST':

        #the fields we are checking against our stored values in our database for user table 
        #All the basic validation like correct email,non empty, length etc are already checked for in pur client side login form  
        #We are also using django default decorator @csrf_exempt to prevent any kind of malformed input 
        handle    = request.POST.get('loginhandle')
        password    = request.POST.get('loginpassword')
        #pdb.set_trace()    
  
        #NSA watchout!
        password = encode(password)  
        try:
                #pdb.set_trace()

		DB = DB_Obj()
                cursor = DB.cursor()
                #we check for valid handle and password combo
		query = "SELECT * FROM users WHERE handle='%s' AND password='%s'" %(handle,password)
 		cursor.execute(query)
		rows = cursor.fetchone()
                
                if rows:
                   request.session['uid']=int(rows[0])
                   request.session['name']= str(rows[1])+" "+str(rows[2])
                   request.session['email'] = str(rows[3])
                   request.session['handle']= str(rows[4])
                   request.session['about']= str(rows[6])
                   request.session['logged'] = True
                   request.session['followers']= get_followers_count(request.session['uid'])
                   request.session['following']= get_following_count(request.session['uid'])
                   request.session['tweet_count']= get_tweet_count(request.session['uid'])
                   response['result'] = 'Success'
                   response['message']='Auth Done!,redirecting'
                else:
                  response['result'] = 'failed'
                  response['message']="error':'Invalid Handle & Password combination'"
                
		DB.commit()
		DB.close()
                return HttpResponse(json.dumps(response), content_type="application/json")
        #User is smart, But we will not let him get IN!!!
        except MySQLdb.Error, e:
                print str(e)
                response['result'] = 'failed'
		response['message']='Some Internal error,Try Again!'
                return HttpResponse(json.dumps(response), content_type="application/json")
    else:
      response['result']='failed'
      response['message']='Not a valid post request'
      return HttpResponse(json.dumps(response), content_type="application/json")     


def logout(request):

    request.session.flush()
    request.session['logged'] = False
    return HttpResponseRedirect('/login')
         

#Signup form processed after data is recieved from signup form
@csrf_exempt
def process_signup(request):
    #Response we will return
    response={}
    #pdb.set_trace()

    #POST request, all except post are ignored
    if request.method == 'POST':

        #the fields we are storing in our database for user table 
        #All the basic validation like correct email,non empty, length etc are already checked for in pur client side signup form  
        #We are also using django default decorator @csrf_exempt to prevent any kind of malformed input 
        email    = request.POST.get('email')
        fname    = request.POST.get('fname')
        lname    = request.POST.get('lname')
        password    = request.POST.get('password')
        handle   = request.POST.get('handle')
        about      = request.POST.get('about')
        #pdb.set_trace()    
  
        #NSA watchout!
        password = encode(password)  
     
        #checking if handle and email don't already exist, if yes we retun failed message else user is registered
        try:
                #pdb.set_trace()

		DB = DB_Obj()
                cursor = DB.cursor()
		query = "SELECT * FROM users WHERE handle='%s' " % (handle)
		query2 = "SELECT * FROM users WHERE email='%s' " % (email)
 		cursor.execute(query)
		rows = cursor.fetchall()
		#pdb.set_trace()
		if rows:
		   response['result'] = 'failed'
                   #pdb.set_trace() 
		   response['message'] = 'Handle already exists'
		   return HttpResponse(json.dumps(response), content_type="application/json")

                cursor.execute(query2)
		rows2 = cursor.fetchall()
		if rows2:
		   response['result'] = 'failed'
		   response['message'] = 'Email already exists'
  		   return HttpResponse(json.dumps(response), content_type="application/json")

                #if handle and email are not registered,We commit to our db
		insert = "INSERT INTO users (email,fname,lname,password,handle,about) VALUES (%s, %s, %s, %s, %s,%s)"
		params = (str(email),str(fname),str(lname),str(password),str(handle),str(about))
		cursor.execute(insert, params)
		DB.commit()
		DB.close()
		response['result'] = 'Success'
		response['message']='Create new user Success' 
		return HttpResponse(json.dumps(response), content_type="application/json")

        #User is smart, But we will not let him get IN!!!
        except MySQLdb.Error, e:
                print str(e)
                response['result'] = 'failed'
		response['message']='Some Internal error,Try Again!'
                return HttpResponse(json.dumps(response), content_type="application/json")
            

    else:
      response['result']='failed'
      response['message']='Not a valid post request'
      return HttpResponse(json.dumps(response), content_type="application/json") 
   
    
