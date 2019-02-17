import urllib.request
import urllib.parse
import urllib.error
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import twurl
import json
import ssl


def js_load(acct):

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '200'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    headers = dict(connection.getheaders())
    return js


def _input():
    while True:
        print('')
        acct = input('Enter Twitter Account:')
        if (len(acct) > 1):
            return acct


def friends_locations(js):
    """
    Finds locations of users in js and creates dict key - location
    value - list of users screennames
    """
    friends = dict()
    for u in js['users']:
        if 'location' not in u or not u['location']:
            print('   * No location found')
        else:
            if u['location'] not in friends:
                friends[u['location']] = []
            friends[u['location']].append(u['screen_name'])
    return friends


def locations_to_coordinates(friends):
    """
    dct -> dct
    This functions transform dict with keys= location to the dict with
    keys =(latitude, longitude) and values = films made in that places
    """
    friends1 = dict()
    for loc in friends:
        l = loc.split(',')
        la = False
        lo = False
        try:
            geolocator = Nominatim(user_agent="hello_it_is_me")
            geocode = RateLimiter(geolocator.geocode, error_wait_seconds=2.0,
                                  max_retries=0, swallow_exceptions=False, return_value_on_exception=True)
            location = geolocator.geocode(l[0])
            la = location.latitude
            lo = location.longitude
            if (la, lo) not in friends1:
                friends1[(la, lo)] = ", ".join(friends[loc])
            else:
                friends1[(la, lo)] += ", " + ", ".join(friends[loc])
        except Exception as err:
            print(err, loc, friends[loc])
    return friends1


def to_map(friends):
    map = folium.Map(location=[0.0, 0.0], zoom_start=2)
    fg_fr = folium.FeatureGroup(name="My friends")
    for locations in friends:
        fg_fr.add_child(folium.CircleMarker(location=[
            locations[0], locations[1]], radius=10, popup=friends[locations], fill_opacity=1))
    map.add_child(fg_fr)
    map.save("My_Map.html")


if __name__ == "__main__":
    acc = _input()
    js = js_load(acc)
    with open('data.json', 'w') as outfile:
        json.dump(js, outfile)
    friends = friends_locations(js)
    to_map(locations_to_coordinates(friends))
