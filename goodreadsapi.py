import requests
requests.packages.urllib3.disable_warnings()


def genderize(name):
    return requests.get(
        'https://api.genderize.io/', 
        params={'apikey': '8d7d83a04bb749681ea4e8531f8492d4', 
                'name': name}).json()['gender']

# goodreads
r = requests.get(
        'https://www.goodreads.com/search.xml?key=tS4AZr3qhInGYME1VeuQGg&q=Ender%27s+Game') 
        # params={'apikey': '8d7d83a04bb749681ea4e8531f8492d4', 
                # 'name': name})

print r.content
# key: tS4AZr3qhInGYME1VeuQGg
# secret: v2nHmXYiJBUo53OySrIOsUuYKgN7PsM4deYv7M8

# https://www.goodreads.com/search.xml?key=YOUR_KEY&q=Ender%27s+Game