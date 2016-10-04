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

r = requests.post('http://146.185.179.202:9999/trigger', data={'job': job, 'machine':machine, 'branch': branch, 'user': user})
uid = r.json()["build"]
print "Build: %s started" % uid

start_time = time.time()
max_time = time.time() * (30 * 60)
temp = ""

while time.time() < max_time:
    try:
        time.sleep(2)
        r = requests.get("http://146.185.179.202:9999/log/" + uid)
        j = json.loads(r.text)

        if j != temp:
            print "\n", str(j)
            temp = j
        else:
            print ".",

        if "log" in j and type(j["log"]) is dict and "completed" in j["log"] and j["log"]["completed"]:
            print "done"
            break

    except Exception, e:
        print "error:", e
        pass


machine = os.environ['YOCTO_MACHINE']

try:
    os.mkdir(machine)
except:
    pass

if machine == "beaglebone":
    print "Downloading beaglebone output files"
    urllib.urlretrieve ("https://s3-eu-west-1.amazonaws.com/mender-temp/%s/beaglebone/core-image-base-beaglebone.ext4" % (uid), "beaglebone/core-image-base-beaglebone.ext4")
    urllib.urlretrieve ("https://s3-eu-west-1.amazonaws.com/mender-temp/%s/beaglebone/core-image-base-beaglebone.sdimg" % (uid), "beaglebone/core-image-base-beaglebone.sdimg")
elif machine == "vexpress-qemu":
    print "Downloading vexpress-qemu output files"
    urllib.urlretrieve ("https://s3-eu-west-1.amazonaws.com/mender-temp/%s/vexpress-qemu/core-image-full-cmdline-vexpress-qemu.ext4" % (uid), "vexpress-qemu/core-image-full-cmdline-vexpress-qemu.ext4")
    urllib.urlretrieve ("https://s3-eu-west-1.amazonaws.com/mender-temp/%s/vexpress-qemu/core-image-full-cmdline-vexpress-qemu.sdimg" % (uid), "vexpress-qemu/core-image-full-cmdline-vexpress-qemu.sdimg")
