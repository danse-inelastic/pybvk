#!/bin/sh

./harm2fcs.py
./fcs2bvkIn.py > V3Si.body
cat V3Si.head V3Si.body V3Si.tail > V3Si
chmod 755 V3Si

