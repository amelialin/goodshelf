import oauth2 as oauth
import urlparse
import requests
import urllib
requests.packages.urllib3.disable_warnings()

# adds book to user's to-read shelf, given the book's ISBN

def add_book_by_isbn(isbn):
    url = 'http://www.goodreads.com'
    request_token_url = '%s/oauth/request_token' % url
    authorize_url = '%s/oauth/authorize' % url
    access_token_url = '%s/oauth/access_token' % url

    # these come from the Goodreads API developer account
    APP_KEY = 'tS4AZr3qhInGYME1VeuQGg'
    APP_SECRET = 'v2nHmXYiJBUo53OySrIOsUuYKgN7PsM4deYv7M8'
    # these come from running goodreads-oauth.py
    USER_TOKEN = 'jOQ9CNoSqoRpzwgAc9pjA'
    USER_SECRET = 'VKhP4N0YMVxLETi8lKew636vchBirQa6YTD9upct18'

    consumer = oauth.Consumer(key=APP_KEY,
                              secret=APP_SECRET)

    token = oauth.Token(USER_TOKEN, USER_SECRET)

    # transform isbn to book_id
    query = url + '/book/isbn_to_id/' + str(isbn) + '?key=' + APP_KEY
    print query

    book_id = requests.get(
            query).json()

    client = oauth.Client(consumer, token)
    body = urllib.urlencode({'name': 'to-read', 'book_id': book_id})
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
                                       'POST', body, headers)
    # check that the new resource has been created
    if response['status'] != '201':
        raise Exception('Cannot create resource: %s' % response['status'])
    else:
        print 'Book added!'

if __name__ == "__main__":
    from sys import argv
    script, isbn = argv
    print add_book_by_isbn(isbn)