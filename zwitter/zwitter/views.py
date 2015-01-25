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
from datetime import datetime

from models import *

from django.http import * #(HttpResponse, HttpResponseRedirect)
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.context_processors import csrf

from auth import *
from settings import *
from local_settings import *

def DB_Obj():
    db_obj = MySQLdb.connect(MYSQL_HOST,MYSQL_USERNAME,MYSQL_PASSWORD,MYSQL_DATABASE)
    return db_obj

def salt():
        return 'zwitter_1234'

def encode(password):
        return hashlib.md5(salt() + password).hexdigest()

def index(request):
    return render(request,'user.html')


@csrf_exempt
def process_signup(request):
    response={}
    response['message'] = ''
    #pdb.set_trace()
    if request.method == 'POST':

        email    = request.POST.get('email')
        fname    = request.POST.get('fname')
        lname    = request.POST.get('lname')
        password    = request.POST.get('password')
        handle   = request.POST.get('handle')
        about      = request.POST.get('about')
        #pdb.set_trace()      
        #NSA watchout!
        password = encode(password)  
     
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

		insert = "INSERT INTO users (email,fname,lname,password,handle,about) VALUES (%s, %s, %s, %s, %s,%s)"
		params = (str(email),str(fname),str(lname),str(password),str(handle),str(about))
		cursor.execute(insert, params)
		DB.commit()
		DB.close()
		response['result'] = 'Success'
		response['message']='Create new user Success' 
		return HttpResponse(json.dumps(response), content_type="application/json")
        except MySQLdb.Error, e:
                print str(e)
            

    else:
      response['result']='failed'
      response['message']='Not a valid post request'
      return HttpResponse(json.dumps(response), content_type="application/json") 
   
    if response.has_key('result') and response['result']=='failed':
       response['message']='Not a valid post request last'
       return HttpResponse(json.dumps(response), content_type="application/json")
    #pdb.set_trace()  
