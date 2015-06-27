#!/usr/bin/env python

import json
import hmac
from hashlib import sha1,md5
import requests
import sys
import urllib
import unicodedata

ACCESS_KEY="codex"
SECRET_KEY="fSySMaec6abmeu6Mv3B4TV21PzKl7jCZiVjtcxvy8lAVJGCjjUwwjE6VqnKsMx4b"
HOST = "apis.shelfie.com"

def strip_unicode(value):
    return unicodedata.normalize('NFKD', unicode(value)).encode('ascii','ignore')

def hmac_auth(secret, value):
  return hmac.new(secret,value,sha1).digest().encode("base64")

def crt_date():
  from wsgiref.handlers import format_date_time
  from datetime import datetime
  from time import mktime

  now = datetime.now()
  stamp = mktime(now.timetuple())
  return format_date_time(stamp)

def request_with_auth(method, url, body, headers):
  md5sum = md5(body).hexdigest()
  content_type = headers["Content-Type"]
  date = crt_date()
  headers["Date"] = date
  headers["Content-MD5"] = md5sum

  auth_value = "%s\n%s\n%s\n%s\n%s"%(method, md5sum, content_type, date, url)
  auth = "hmac %s:%s"%(ACCESS_KEY, hmac_auth(SECRET_KEY, auth_value).strip())
  headers["Authorization"] = auth

  resp = requests.request(method, 'http://'+HOST+url, headers = headers, data = body)
  resp.raise_for_status()
  return resp.content

  

def login_user(email):
  headers={"Content-Type": "application/json"}
  response = request_with_auth("GET", "/codex/login?email="+urllib.quote_plus(email), "", headers)
  return json.loads(response)


def create_user(email, firstName, lastName):
  request = { "email": email, "firstName": firstName, "lastName": lastName}  
  json_request = json.dumps(request)
  headers={"Content-Type": "application/json"}
  response = request_with_auth("POST", "/codex/users", json_request, headers)
  return json.loads(response)


def submit_shelfie(userID, image_path):
  f = open(image_path,"rb")
  body = f.read()
  f.close()
  headers={}
  headers["Content-Type"] = "image/jpeg"
  headers["Content-Length"] = len(body)
  response = request_with_auth("POST", "/codex/users/%s/shelfies"%userID, body, headers)
  return json.loads(response)
  

def shelfie_status(shelfieID):
  headers={"Content-Type": "application/json"}
  response = request_with_auth("GET", "/codex/shelfies/%s/status"%shelfieID, "", headers)
  return json.loads(response)
  

def user_books(userID):
  headers={"Content-Type": "application/json"}
  response = request_with_auth("GET", "/codex/users/%s/books"%userID, "", headers)
  return json.loads(response)

def book_cover(isbn):
  headers={"Content-Type": "application/json"}
  response = request_with_auth("GET", "/codex/books/%s/cover"%isbn, "", headers)
  return response


def save_cover(body, name):
  f = open(name, "wb")
  f.write(body)
  f.close()

if __name__ == "__main__" :
  userID = ""
  print "-- Login user"
  resp = login_user("marius.muja@shelfie.com")
  print resp
  if resp.has_key("userID"):
    userID = resp["userID"]
  else:
    print "-- Create user"    
    resp = create_user("marius.muja@shelfie.com","Marius","Muja")
    print resp
    if resp.has_key("userID"):
      userID = resp["userID"]


  if len(sys.argv)>1 and userID!="":
    print "--  Submit shelfie"    
    resp = submit_shelfie(userID,sys.argv[1])
    print resp


  print "--  Shelfie status"    
  resp = shelfie_status("GfajZqW8aSB")
  print resp

  print "--  User status"    
  resp = user_books("1KHjGYFtfaF")
  print resp


  print "-- Book cover"
  resp = book_cover("9780061944895")
  save_cover(resp, "9780061944895.jpg")
  print "done"

