import oauth2 as oauth
import urlparse
import requests

URL = 'http://www.goodreads.com'
REQUEST_TOKEN_URL = '%s/oauth/request_token' % URL
AUTHORIZE_URL = '%s/oauth/authorize' % URL
aCCESS_TOKEN_URL = '%s/oauth/access_token' % URL

APPLICATION_KEY = 'tS4AZr3qhInGYME1VeuQGg'
APPLICATION_SECRET = 'v2nHmXYiJBUo53OySrIOsUuYKgN7PsM4deYv7M8'

consumer = oauth.Consumer(key=APPLICATION_KEY,
                          secret=APPLICATION_SECRET)

client = oauth.Client(consumer)

response, content = client.request(REQUEST_TOKEN_URL, 'GET')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

# This is the user token.
request_token = dict(urlparse.parse_qsl(content))

# The token request URL hands back a URL that the user has to accept.
authorize_link = '%s?oauth_token=%s' % (AUTHORIZE_URL,
                                        request_token['oauth_token'])
print authorize_link
accepted = 'n'
while accepted.lower() == 'n':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
    accepted = raw_input('Have you authorized me? (y/n) ')

token = oauth.Token(request_token['oauth_token'],
                    request_token['oauth_token_secret'])

client = oauth.Client(consumer, token)
response, content = client.request(ACCESS_TOKEN_URL, 'POST')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urlparse.parse_qsl(content))

# this is the token you should save for future uses
token = oauth.Token(access_token['oauth_token'],
                    access_token['oauth_token_secret'])

