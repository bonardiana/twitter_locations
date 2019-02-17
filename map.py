import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

inputs = ['screen_name', 'location', 'description', 'url',
          'followers_count', 'friends_count', 'favourites_count',
          'created_at', 'verified', 'statuses_count', 'status']

while True:
    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) > 1):
        break
while True:
    print("Choose information you want to get about users friends.")
    info = input(inputs)
    if info in inputs:
        break
url = twurl.augment(TWITTER_URL,
                    {'screen_name': acct, 'count': '200'})
print('Retrieving', url)
connection = urllib.request.urlopen(url, context=ctx)
data = connection.read().decode()

js = json.loads(data)
with open('data.json', 'w') as outfile:
    json.dump(js, outfile)
print(json.dumps(js, indent=2))

headers = dict(connection.getheaders())
print('Remaining', headers['x-rate-limit-remaining'])

for u in js['users']:
    print(u['screen_name'])
    if 'status' not in u:
        print('   * No status found')
        continue
    s = u['status']['text']
    print('  ', s[:50])
print(len(js['users']))
