#!/usr/bin/env python

import json
import hmac
from hashlib import sha1,md5
import requests
import sys
import urllib

ACCESS_KEY="codex"
SECRET_KEY="fSySMaec6abmeu6Mv3B4TV21PzKl7jCZiVjtcxvy8lAVJGCjjUwwjE6VqnKsMx4b"
HOST = "apis.shelfie.com"
LOGIN_USER_EMAIL = "amelialin0@gmail.com"
LOGIN_USER_FIRST = "Amelia"
LOGIN_USER_LAST = "Lin"

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
    #resp.raise_for_status()
    return resp

def login_user(email):
    headers={"Content-Type": "application/json"}
    response = request_with_auth("GET", "/codex/login?email="+urllib.quote_plus(email), "", headers)
    return json.loads(response.content)

def create_user(email, firstName, lastName):
    request = { "email": email, "firstName": firstName, "lastName": lastName}  
    json_request = json.dumps(request)
    headers={"Content-Type": "application/json"}
    response = request_with_auth("POST", "/codex/users", json_request, headers)
    return json.loads(response.content)  

def shelfie_status(shelfieID):
    headers={"Content-Type": "application/json"}
    response = request_with_auth("GET", "/codex/shelfies/%s/status"%shelfieID, "", headers)
    return json.loads(response.content)

def submit_shelfie(image_path, shelf_name):
    userID = ""
    resp={}

    # login user
    # print "-- Login user"
    try:
        resp = login_user(LOGIN_USER_EMAIL)
        # print resp
    except:
         pass

    # get user id
    if resp.has_key("userID"):
        userID = resp["userID"]
    else:
        print "-- Create user"    
        resp = create_user(LOGIN_USER_EMAIL, LOGIN_USER_FIRST, LOGIN_USER_LAST)
        print resp
        if resp.has_key("userID"):
          userID = resp["userID"]

    # submit shelfie
    if userID == "":
        raise Exception('Missing user ID.')
    print "--  Submit shelfie"    

    f = open(image_path,"rb")
    body = f.read()
    f.close()
    headers={}
    headers["Content-Type"] = "image/jpeg"
    headers["Content-Length"] = len(body)
    response = request_with_auth("POST", "/codex/users/%s/shelfies"%userID, body, headers)
    resp = json.loads(response.content)
    print resp
    shelfieID = resp['shelfieID']

    print "--  Shelfie status"    
    resp = shelfie_status(shelfieID)
    print resp

    return shelfieID, shelf_name, image_path

if __name__ == "__main__" :
    from sys import argv
    if len(argv) < 2:
        raise Exception('Too few arguments.')
    script, image_path, shelf_name = argv
    print submit_shelfie(image_path, shelf_name)