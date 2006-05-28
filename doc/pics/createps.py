#!/usr/bin/env python
# Create the Postscript files from the image files

import os, os.path, glob

# Convert all jpg images into compressed ps images
imgfiles = glob.glob("*.jpg")
for imgfile in imgfiles:
    psfile = os.path.splitext(imgfile)[0]+".ps"
    cmd = "jpeg2ps %s >%s"%(imgfile, psfile)
    print cmd
    os.system(cmd)
