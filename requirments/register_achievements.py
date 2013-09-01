import urllib,urllib2

url = 'https://graph.facebook.com/159866620823022/achievements'
payload = urllib.urlencode({'access_token':'Access Token GOES  Here',
                            'achievement':'http://vijeenroshpw.pythonanywhere.com/achievements/ach1.html' })
request = urllib2.Request(url,payload)
response = urllib2.urlopen(request)
print response.read()


