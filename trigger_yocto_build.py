#!/usr/bin/python
import os
import requests
from itsdangerous import TimestampSigner
import time
import json
import urllib


s = TimestampSigner(os.environ["KEY"])

user = s.sign(os.environ['GITHUB_USER'])
branch = s.sign(os.environ['BRANCH'])
machine = s.sign(os.environ['YOCTO_MACHINE'])
job = s.sign(os.environ["JOB"])

r = requests.post('http://home.distefa.no:9999/trigger', data={'job': job, 'machine':machine, 'branch': branch, 'user': user})
uid = r.json()["build"]

temp = ""
while True:
    try:
        time.sleep(10)
        r = requests.get("http://home.distefa.no:9999/log/" + uid)
        j = json.loads(r.text)

        if j != temp:
            print j
            temp = j
        else:
            print ".",

        if "log" in j and "done" in j["log"] and j["log"]["done"] == "success":
            print "done"
            break

    except Exception, e:
        print "error:", e
        pass

#urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
#urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
#urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
#urllib.urlretrieve ("http://www.example.com/songs/mp3.mp3", "mp3.mp3")
