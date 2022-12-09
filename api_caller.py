import random
import uuid
import urllib.request
import requests
import hashlib
import base64
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Open the dictionary file of words
f = open("dictwords", "r")
wordlist = f.read()
f.close()
words = wordlist.splitlines()
# If you want to only use words that look like names
#upper_words = [word for word in words if word[0].isupper()]
#name_words  = [word for word in upper_words if not word.isupper()]


class APICaller():

    def __init__(self, data, url, endpoints, requestCount, username, password):
        self.URL = url
        self.endpoints = endpoints
        self.requestCount = requestCount
        self.endpoints = endpoints
        self.user = username
        self.password = password

    def rand_string(self):
        return words[random.randint(0, len(words)-1)]

    def rand_low_number(self):
        return str(random.randint(0, 1000))

    def rand_hi_number(self):
        return str(random.randint(10000, 99999))

    def rand_lo_number(self):
        return str(random.randint(0, 5))

    def rand_uuid(self):
            return str(uuid.uuid1())

    def rand_endpoint(self):
        return self.endpoints[random.randint(0, len(self.endpoints)-1)]

    def run(self):
        for n in range(self.requestCount):
            new_endpoint = self.rand_endpoint()
            if new_endpoint == 'get':
                new_endpoint = 'get?random_num=' + self.rand_hi_number()
            elif new_endpoint == 'cache':
                new_endpoint = 'cache/' + self.rand_low_number()
            elif new_endpoint == 'etag':
                new_endpoint = 'etag/' + self.rand_uuid()
            elif new_endpoint == 'response-headers':
                new_endpoint = 'response-headers?random_string=' + self.rand_string()
            elif new_endpoint == 'base64':
                new_endpoint = 'base64/' + base64.b64encode(self.rand_string().encode('ascii')).decode('ascii')
            elif new_endpoint == 'range':
                new_endpoint = 'range/' + self.rand_low_number()
            elif new_endpoint == 'anything':
                new_endpoint = 'anything/random_md5/' + hashlib.md5(self.rand_string().encode()).hexdigest()

            new_endpoint = self.URL + new_endpoint
            print("[" + str(n) + "] Trying:",new_endpoint)

            r = requests.get(new_endpoint, auth=(self.user, self.password),verify=False)

            print("Status:",r.status_code)
            print()