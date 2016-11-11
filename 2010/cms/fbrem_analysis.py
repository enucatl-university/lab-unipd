#!/usr/bin/env python
#coding=utf-8

from __future__ import division, print_function
import sys
import style
from electron_dataset import ElectronDataset, DatasetComparison

style.ele_style.cd()

comparison = DatasetComparison(*sys.argv[1:])
comparison.draw()
print("Done.")
#raw_input()
