import oauth2 as oauth
import urlparse
import requests
import urllib
requests.packages.urllib3.disable_warnings()

def add_book_by_isbn(isbn):
    """Adds book to user's to-read shelf, given the book's ISBN as a string"""

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
    query = url + '/book/isbn_to_id/' + isbn    
    book_id = requests.get(query, params={'key': APP_KEY}).content
    if book_id == ' ':
        return False
    client = oauth.Client(consumer, token)
    body = urllib.urlencode({'name': 'to-read', 'book_id': book_id})
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request('%s/shelf/add_to_shelf.xml' % url, 'POST', body, headers)
    
    # check that the new resource has been created
    if response['status'] != '201':
        raise Exception('Cannot create resource: %s' % response['status'])
    else:
        return book_id

# def add_books_to_gr(isbns):
#     for isbn in isbn_list:
#         add_book_by_isbn(isbn)

#     # add isbns from processed books to goodreads
#     isbns = map(strip_unicode, resp["books"])
#     print len(isbns)
#     conn = sqlite3.connect('goodshelf')
#     cursor = conn.cursor()
#     for isbn in isbns:
#         book_id = add_book_to_shelf.add_book_by_isbn(isbn)
#         if book_id:
#             print "yeah book added!", book_id
#             cursor.execute("INSERT INTO shelfie_books(shelfie_id, isbn, gr_book_id) values (?,?,?);", (shelfie_id, isbn, book_id))
#         else:
#             print "gotta add it manually :(", isbn
#             cursor.execute("INSERT INTO shelfie_books(shelfie_id, isbn) values (?,?);", (shelfie_id, isbn))
#         conn.commit()
#     conn.close()

if __name__ == "__main__":
    from sys import argv
    script, isbn = argv
    print add_book_by_isbn(isbn)