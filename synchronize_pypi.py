#!/usr/bin/python2.7
# pip install pip2pi
from __future__ import division


import os
import requests
import threading


url = "https://pypi.python.org/pypi/%s/json"


def get_releases(package_name):
    data = requests.get(url % (package_name)).json()
    releases= data.get("releases")
    for k,v in releases.items():
        if v:
            os.system("pip2tgz ../web/ %s==%s" % (package_name, k))


class ReleasesThread (threading.Thread):

    def __init__(self, threadID, name, results):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.fs = results

    def run(self):
        get_releases_all(self.threadID, len(self.fs))
        print "starting -> %s, %s" % (self.threadID, self.name)


if __name__ == "__main__":

    total_thread = 3
    filename = open("requirements.txt", "rw")
    filename_list = filename.readlines()
    filename_list = [x.strip("\n") for x in filename_list if x.strip("\n")]

    def get_releases_all(tid, length):
        mod = length % total_thread
        if not (mod == 0):
            length = length + mod
            page_count = (length // total_thread) + 1
        else:
            page_count = length // total_thread

        start = page_count * (tid-1)
        end = page_count * tid

        for i in filename_list[start:end]:
            try:
                get_releases(i)
            except:
                continue

    for i in range(1, total_thread + 1):
        a = ReleasesThread(i, "Process request!", filename_list)
        a.start()
        os.system("dir2pi ../web/ ")

