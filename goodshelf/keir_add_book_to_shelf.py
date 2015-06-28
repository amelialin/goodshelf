import oauth2 as oauth
import urlparse
import requests
import urllib
requests.packages.urllib3.disable_warnings()


# As an example, let's add a book to one of the user's shelves
#

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url

APP_KEY = 'tS4AZr3qhInGYME1VeuQGg'
APP_SECRET = 'v2nHmXYiJBUo53OySrIOsUuYKgN7PsM4deYv7M8'

USER_TOKEN = 'x79lRrC2zmxHV5hBK76iQ'
USER_SECRET = 'hoSG1QShKfdRDRleu2aid41KXamvQBPZbgIMBZQ'

consumer = oauth.Consumer(key=APP_KEY,
                          secret=APP_SECRET)

token = oauth.Token(USER_TOKEN, USER_SECRET)

# transform isbn to book_id
isbn = '9781449314323'
query = url + '/book/isbn_to_id/'
r = requests.get(
        'https://www.goodreads.com/book/isbn_to_id/9781449314323?key=tS4AZr3qhInGYME1VeuQGg').json()

# print r

book_id = 41821

client = oauth.Client(consumer, token)
# the book is: "Generation A" by Douglas Coupland
body = urllib.urlencode({'name': 'to-read', 'book_id': book_id})
headers = {'content-type': 'application/x-www-form-urlencoded'}
response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
                                   'POST', body, headers)
# check that the new resource has been created
if response['status'] != '201':
    raise Exception('Cannot create resource: %s' % response['status'])
else:
    print 'Book added!'