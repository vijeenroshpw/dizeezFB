
#! /bin/bash
# Scripters way of registerigng the achievements for app

curl --request DELETE --data "achievement=http://vijeenroshpw.pythonanywhere.com/achieves/1&access_token={{ access_token }}" https://graph.facebook.com/{{ app_id }}/achievements 

curl -d "achievement=http://vijeenroshpw.pythonanywhere.com/achieves/1&access_token={{ access_token }}" https://graph.facebook.com/{{ app_id }}/achievements




