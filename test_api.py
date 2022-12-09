from api_caller import APICaller
import time



apiURL = 'http://10.10.196.11/'
requestCount = 100

# Open the dictionary file of words
f = open("dictwords", "r")
wordlist = f.read()
f.close()
words = wordlist.splitlines()
# If you want to only use words that look like names
#upper_words = [word for word in words if word[0].isupper()]
#name_words  = [word for word in upper_words if not word.isupper()]

endpoints = ['get','status/200','status/300','status/400','status/500','headers','ip','user-agent','cache','etag','response-headers','brotli','deflate','deny','encoding/utf8','gzip','html','json','robots.txt','xml','base64','bytes/5','links/5/0','range','stream/3','uuid','cookies','image','image/jpeg','image/png','image/svg','image/webp','anything']

apiCaller = APICaller(words, apiURL, endpoints, requestCount, 'user', 'pass')

if __name__ ==  "__main__":
    start = time.time()
    apiCaller.run()
    end = time.time()
    print(end-start)
