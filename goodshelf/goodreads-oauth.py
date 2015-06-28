import oauth2 as oauth
import urlparse
import requests

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
authorize_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url

KEY = 'tS4AZr3qhInGYME1VeuQGg'
SECRET = 'v2nHmXYiJBUo53OySrIOsUuYKgN7PsM4deYv7M8'

consumer = oauth.Consumer(key=KEY,
                          secret=SECRET)

client = oauth.Client(consumer)

response, content = client.request(request_token_url, 'GET')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

request_token = dict(urlparse.parse_qsl(content))

authorize_link = '%s?oauth_token=%s' % (authorize_url,
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
response, content = client.request(access_token_url, 'POST')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urlparse.parse_qsl(content))

# this is the token you should save for future uses
token = oauth.Token(access_token['oauth_token'],
                    access_token['oauth_token_secret'])

print access_token

