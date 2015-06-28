import oauth2 as oauth
import urlparse
import requests
import urllib
requests.packages.urllib3.disable_warnings()

def check_for_shelf(shelf_name):
    """Checks to see if shelf exists, if it doesn't, creates it"""

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
    USER_ID = '7308319'

    consumer = oauth.Consumer(key=APP_KEY,
                              secret=APP_SECRET)

    token = oauth.Token(USER_TOKEN, USER_SECRET)

    client = oauth.Client(consumer, token)
    
    # check for existing shelf
    # query = url + '/shelf/list.xml'   
    # # https://www.goodreads.com/shelf/list.xml?key=tS4AZr3qhInGYME1VeuQGg 
    # user_shelves = requests.get(query, params={'key': APP_KEY, 'user_id': USER_ID}).content
    # print user_shelves
    # return False

    # add new shelf
    body = urllib.urlencode({'user_shelf[name]': 'test_shelf'})
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request('%s/user_shelves.xml' % url, 'POST', body, headers)
    
    # check that the new resource has been created
    if response['status'] == '409':
        print shelf_name, "shelf already exists"
        return True
    if response['status'] != '201':
        raise Exception('Cannot create resource: %s' % response['status'])
    else:
        return True

if __name__ == "__main__":
    from sys import argv
    script, shelf_name = argv
    print check_for_shelf(shelf_name)