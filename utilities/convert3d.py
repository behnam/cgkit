#!/usr/bin/env python
######################################################################
# 3D file converter
######################################################################

import sys, optparse
from cgkit.all import *

# Parse options
parser = optparse.OptionParser("usage: %prog [options] inputfiles outputfile")
options, args = parser.parse_args()

# Check if there are enough arguments (at least one input file and an
# output file)
if len(args)<2:
    parser.print_help()
    sys.exit(1)

srcs = args[:-1]
dst = args[-1]
# Read the input files...
for src in srcs:
    print 'Loading "%s"...'%src
    load(src)

# Save the scene
print 'Saving "%s"...'%dst
save(dst)

