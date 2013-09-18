import urllib,urllib2

url = 'https://graph.facebook.com/{{ app_id }}/achievements'
payload = urllib.urlencode({'access_token':'Access Token GOES  Here',
                            'achievement':'http://vijeenroshpw.pythonanywhere.com/achieves/1' })
request = urllib2.Request(url,payload)
response = urllib2.urlopen(request)
print response.read()


