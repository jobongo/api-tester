from queue import Queue
import requests
from threading import Thread
import time
import random
import hashlib
import base64
#import urllib.request
import uuid
import argparse

argParser = argparse.ArgumentParser(description="API Testing Tool to generate randomized API calls to httpbin server.")
argParser.add_argument("-c", "--request_count", help="Number of API requests to send", default=1, type=int)
argParser.add_argument("-d", "--api_url", help="Specify the URL.", default="http://10.10.196.11/")
argParser.add_argument("-t", "--thread_count", help="Number of threads to run simultaneously.", default=10, type=int)
args = argParser.parse_args()

numOfRequests = args.request_count
numOfThreads = args.thread_count
apiURL = args.api_url

if list(apiURL)[-1] != '/':
    apiURL = apiURL + '/'

f = open("dictwords", "r")
wordlist = f.read()
f.close()
words = wordlist.splitlines()

endpoints = [
    'get',
    'status/200',
    'status/300',
    'status/400',
    'status/500',
    'headers',
    'ip',
    'user-agent',
    'cache',
    'etag',
    'response-headers',
    'brotli',
    'deflate',
    'deny',
    'encoding/utf8',
    'gzip',
    'html',
    'json',
    'robots.txt',
    'xml',
    'base64',
    'bytes/5',
    'links/5/0',
    'range',
    'stream/3',
    'uuid',
    'cookies',
    'image',
    'image/jpeg',
    'image/png',
    'image/svg',
    'image/webp',
    'anything',
    'echo'
    ]

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.count = 0
        self.tasks = tasks
        self.daemon = True
        self.start()
        

    def run(self):       
        while True:
            func, args, kargs = self.tasks.get()
            
            try:
                func(*args, **kargs)
                
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    """ Create a pool of threads."""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()

class APIGenerator():
    def __init__(self, num_requests, api_url, endpoints, **data):
        self.num_requests = num_requests
        self.apiURL = api_url
        self.endpoints = endpoints
        
    
    def generateResources(self, endpoint):
        if endpoint == 'get':
            resource = 'get?random_num=' + str(random.randint(10000, 99999))
        elif endpoint == 'cache': 
            resource = 'cache/' + str(random.randint(0, 1000))
        elif endpoint == 'etag':
            resource = 'etag/' + str(uuid.uuid1())
        elif endpoint == 'response-headers':
            resource = 'response-headers?random_string=' + words[random.randint(0, len(words)-1)]
        elif endpoint == 'base64':
            resource = 'base64/' + base64.b64encode(words[random.randint(0, len(words)-1)].encode('ascii')).decode('ascii')
        elif endpoint == 'range':
            resource = 'range/' + str(random.randint(0, 5))
        elif endpoint == 'anything':
            resource = 'anything/random_md5/' + hashlib.md5(words[random.randint(0, len(words)-1)].encode()).hexdigest()
        elif endpoint == 'anything':
            resource = 'anything/'
        else:
            resource = endpoint
        return resource
            
    def rand_endpoint(self):
        return self.endpoints[random.randint(0, len(self.endpoints)-1)]

    def generateURLs(self):
        urls = []
        for n in range(self.num_requests):
            endpoint = self.rand_endpoint()
            endpoint_data = self.generateResources(endpoint)
            new_endpoint = f"{self.apiURL}{endpoint_data}"
            urls.append(new_endpoint)
        return urls

def get(url):
    r = session.get(url)
    print(f"{r} {url}")

def post(url):
    r = session.post(url, data={"email": "user@test.com"})
    print(f"{r} {url}")
    print(r.text)

if __name__ == '__main__':
    apiGenerator = APIGenerator(numOfRequests, apiURL, endpoints)
    urls = apiGenerator.generateURLs()
    #urls = ["http://10.10.196.11/anything?freeform=test"]

    pool = ThreadPool(numOfThreads)
    results = {}
    session = requests.session()

    now = time.time()

    pool.map(get, urls)

    #pool.map(post, urls)
    pool.wait_completion()
    time_taken = time.time() - now

    print(time_taken)
