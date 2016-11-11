#!/usr/bin/python
#coding=utf-8

import os
import re

args = raw_input()
args = re.sub("[\D]", " ", args)

launch = "./forzato " + args
os.system(launch)
