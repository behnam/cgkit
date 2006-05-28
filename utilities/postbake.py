#!/usr/bin/env python
###########################################################################
# cgkit - Python Computer Graphics Kit
# Copyright (C) 2004 Matthias Baas (baas@ira.uka.de)
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# cgkit homepage: http://cgkit.sourceforge.net
###########################################################################

import sys, optparse, Image

# shift
def shift(img, dx, dy):
    """Return an image shifted by dx,dy pixels.
    """
    w,h = img.size
    if dx<0:
        x1 = -dx
        x2 = w
        xd = 0
    else:
        x1 = 0
        x2 = w-dx
        xd = dx
        
    if dy<0:
        y1 = -dy
        y2 = h
        yd = 0
    else:
        y1 = 0
        y2 = h-dy
        yd = dy
    clp = img.crop((x1,y1,x2,y2))
    res = Image.new(img.mode, img.size)
    res.paste(clp, (xd,yd))
    return res

# composite
def composite(img1, img2):
    """Composite two images.

    img2 is on top of img1.
    """
    r,g,b,a = img2.split()
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")
    res = Image.composite(img2, img1, a)
    return res

    
######################################################################

usage = "usage: %prog [options] inputimage outputimage"
optparser = optparse.OptionParser(usage)
opts, args = optparser.parse_args()

if len(args)<2:
    optparser.print_help()
    sys.exit()

print 'Reading "%s"...'%args[0]
img = Image.open(args[0])

if img.mode!="RGBA":
    print 'Invalid image mode %s (must be RGBA)'%img.mode
    sys.exit(1)

r = 1
bg = Image.new("RGB", img.size)
bg = composite(bg, shift(img, -r, -r))
bg = composite(bg, shift(img, r,-r))
bg = composite(bg, shift(img, -r,r))
bg = composite(bg, shift(img, r,r))

outimg = composite(bg, img)
print 'Writing "%s"...'%args[1]
outimg.save(args[1])
