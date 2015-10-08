#!/usr/bin/env python

import json
import hmac
from hashlib import sha1,md5
import requests
import sys
import urllib
import unicodedata
import add_book_to_shelf
import web
import sqlite3

ACCESS_KEY="codex"
SECRET_KEY="fSySMaec6abmeu6Mv3B4TV21PzKl7jCZiVjtcxvy8lAVJGCjjUwwjE6VqnKsMx4b"
HOST = "apis.shelfie.com"

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

def strip_unicode(value):
    return unicodedata.normalize('NFKD', unicode(value)).encode('ascii','ignore')

def shelfie_check_status(shelfie_id, shelf_name="NONE", image_path="NONE"):
    """Checks status of a submitted shelfie, given the shelfie ID. If supplied a shelf_name, will also upload any identified books to the corresponding Goodreads shelf."""
    # login user to get userID
    userID = ""
    resp={}
    # print "-- Login user"
    try:
        resp = login_user("amelialin0@gmail.com")
        # print resp
    except:
        pass

    if resp.has_key("userID"):
        userID = resp["userID"]
    else:
        # print "-- Create user"    
        resp = create_user("amelialin0@gmail.com","Amelia","Lin")
        print resp
        if resp.has_key("userID"):
            userID = resp["userID"]

    # check shelfie status
    if userID == "":
        raise Exception('Missing user ID.')
    print "--  Shelfie status"   
    headers={"Content-Type": "application/json"}
    response = request_with_auth("GET", "/codex/shelfies/%s/status"%shelfie_id, "", headers)
    resp = json.loads(response.content)
    print resp
    print "Image path:", image_path

    # if no books have been processed yet
    if "books" not in resp:
        print "no books yet!"
        return 'pending'

    # print out overview of progress
    all_book_data = resp["booksMetadata"]
    # print all_book_data
    for book in all_book_data:
        # print book
        # print book['spineImage']
        if 'isbn' in book:
            print book['spineImage'], book['isbn'], book['title']
        elif ('title' in book) or ('authors' in book):
            search_string = ""
            if 'title' in book:
                search_string += book['title']
            if 'authors' in book:
                search_string += book['authors']
            print book['spineImage'], search_string
        else:
            print book['spineImage']
    print len(all_book_data), "books detected,", len(resp["books"]), "ISBNs identified,", len(all_book_data) - len(resp["books"]), "books unidentified ISBNs"

    # add isbns from processed books to goodreads
    if shelf_name != "NONE":
        conn = sqlite3.connect('goodshelf')
        cursor = conn.cursor()
        unidentified_books = []
        for book in all_book_data:
            spine_image = book['spineImage']
            print spine_image
            # submit detected ISBNs to Goodreads
            if 'isbn' in book:
                isbn = book['isbn']
                book_id = add_book_to_shelf.add_book_by_isbn(isbn, shelf_name)
                if book_id:
                    print "yeah book added!", book_id
                    cursor.execute("INSERT INTO shelfie_books(shelfie_id, isbn, gr_book_id, spine_image) values (?,?,?,?);", (shelfie_id, isbn, book_id, spine_image))
                else:
                    print "gotta add it manually :(", isbn, book['title'], book['authors']
                    cursor.execute("INSERT INTO shelfie_books(shelfie_id, isbn, spine_image) values (?,?,?);", (shelfie_id, isbn, spine_image))
            else:
                unidentified_books.append(spine_image)
            conn.commit()
        conn.close()

        # return spine images for unidentified books
        print "Unidentified books:"
        print unidentified_books

    return resp["status"]

if __name__ == "__main__" :
    from sys import argv
    if len(argv) == 4:
        script, shelfie_id, shelf_name, image_path = argv
        shelfie_check_status(shelfie_id, shelf_name, image_path)
    elif len(argv) ==3:
        script, shelfie_id, shelf_name = argv
        shelfie_check_status(shelfie_id, shelf_name)
    elif len(argv) == 2:
        script, shelfie_id = argv
        shelfie_check_status(shelfie_id)
    else:
        raise Exception('Use 1-3 arguments.')
