# Modify HTTPBIN_URL variable below to point to your HTTPBIN server
# Modify the NUM_HITS variable to control how many API requests/responses are generated (100 by default)

# Run this script with: python3 test.py

import random
import uuid
import urllib.request
import requests
import hashlib
import base64
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# The URL for HTTPBIN, with trailing slash /
HTTPBIN_URL = 'http://10.10.196.11/'

# Number of API calls to make
NUM_HITS = 1000

# Open the dictionary file of words
f = open("dictwords", "r")
wordlist = f.read()
f.close()
words = wordlist.splitlines()
# If you want to only use words that look like names
#upper_words = [word for word in words if word[0].isupper()]
#name_words  = [word for word in upper_words if not word.isupper()]

def rand_string():
    return words[random.randint(0, len(words)-1)]

def rand_hi_number():
    return str(random.randint(10000, 99999))

def rand_lo_number():
    return str(random.randint(0, 5))

def rand_uuid():
    return str(uuid.uuid1())

#print("Random String:",rand_string())
#print("Random Number:",rand_hi_number())
#print("Random ID:",rand_uuid())

endpoints = ['get','status/200','status/300','status/400','status/500','headers','ip','user-agent','cache','etag','response-headers','brotli','deflate','deny','encoding/utf8','gzip','html','json','robots.txt','xml','base64','bytes/5','links/5/0','range','stream/3','uuid','cookies','image','image/jpeg','image/png','image/svg','image/webp','anything']

def rand_endpoint():
    return endpoints[random.randint(0, len(endpoints)-1)]

def test_apis():
    for n in range(NUM_HITS):
        new_endpoint = rand_endpoint()
        if new_endpoint == 'get':
            new_endpoint = 'get?random_num=' +rand_hi_number()
        elif new_endpoint == 'cache':
            new_endpoint = 'cache/'+rand_lo_number()
        elif new_endpoint == 'etag':
            new_endpoint = 'etag/'+rand_uuid()
        elif new_endpoint == 'response-headers':
            new_endpoint = 'response-headers?random_string='+rand_string()
        elif new_endpoint == 'base64':
            new_endpoint = 'base64/'+base64.b64encode(rand_string().encode('ascii')).decode('ascii')
        elif new_endpoint == 'range':
            new_endpoint = 'range/'+rand_lo_number()
        else:
            if new_endpoint == 'anything':
                new_endpoint = 'anything/random_md5/'+hashlib.md5(rand_string().encode()).hexdigest()
        new_endpoint = HTTPBIN_URL+new_endpoint
        print("[" + str(n) + "] Trying:",new_endpoint)
        r = requests.get(new_endpoint, auth=('user', 'pass'),verify=False)
        print("Status:",r.status_code)
        #print()

if __name__ ==  "__main__":
    start = time.time()
    test_apis()
    end = time.time()
    print(end-start)
