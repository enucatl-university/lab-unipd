#!/bin/bash

for file in *.py
do
    python $file $1
done
