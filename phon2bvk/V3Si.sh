#!/bin/sh

./harm2fcs.py
./fcs2bvkIn.py > V3Si.1
cat V3Si.? > V3Si
chmod 755 V3Si

