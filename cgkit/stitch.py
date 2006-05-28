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
# $Id: stitch.py,v 1.3 2005/10/16 12:29:04 mbaas Exp $

"""Image stitching module.

This file can also be used as a command line tool.
"""

import sys, os, os.path, glob, optparse
import _Image as Image

# isTile
def isTile(name):
    """Check if a filename is the name of a tile.
    """
    try:
        splitTileName(name)
    except ValueError:
        return False
    return True

# splitTileName
def splitTileName(name):
    """Split the components of a tile name.

    The return value is a tuple (basename, extension, coords) where
    coords is a tuple (x1,x2,y1,y2).
    A ValueError exception is thrown if name is not a valid tile name.
    """
    coords = []
    n,ext = os.path.splitext(name)
    for i in range(4):
        j = n.rfind("_")
        if j==-1:
            raise ValueError, "no tile name"
        try:
            coords = [float(n[j+1:])]+coords
        except:
            raise ValueError, "no tile name (invalid coordinate)"
        n = n[:j]

    return n,ext,tuple(coords)

# outputSpecs
def outputSpecs(tiles):
    """Return the final image resolution and the pixel positions of the tiles.

    Returns a tuple (width, height, xposs, yposs) where xposs/yposs are
    dictionaries that store the x and y positions of the tiles. The key
    is the x1 (resp. y1) value and the value is the position.
    """
    xsplits = {}
    ysplits = {}

    xres = 0
    yres = 0
    # Sum up the width (height) of each tile with a new x1 (y1) value...
    for tilename, coords, img in tiles:
        x = coords[0]
        y = coords[2]
        w,h = img.size
        if x in xsplits:
            if w!=xsplits[x]:
                raise ValueError, "%s: Inconsistent tile resolution, expected a width of %d but got %d"%(tilename, xsplits[x], w)
        else:
            xsplits[x] = w
            xres += w
        if y in ysplits:
            if h!=ysplits[y]:
                raise ValueError, "%s: Inconsistent tile resolution, expected a height of %d but got %d"%(tilename, ysplits[y], h)
        else:
            ysplits[y] = h
            yres += h

    # Create a dict with the x pixel positions of the tiles...
    xv = xsplits.keys()
    xv.sort()
    xposs = {}
    xpos = 0
    for x in xv:
        xposs[x] = xpos
        xpos += xsplits[x]

    # Create a dict with the y pixel positions of the tiles...
    yv = ysplits.keys()
    yv.sort()
    yposs = {}
    ypos = 0
    for y in yv:
        yposs[y] = ypos
        ypos += ysplits[y]

    return xres, yres, xposs, yposs

# stitch
def stitch(filename, removetiles=False, infostream=None):
    """Stitch several image tiles together.
    
    filename is the base name of the image that determines the file names
    of the tiles. filename is also the name of the output image.
    If removetiles is True, the individual image files will be deleted
    after the image has been stitched.
    If infostream is set to a file like object it is used to output
    status information about the stitching process.

    The name of an image tile must contain the crop information that was
    used to create the image. For example, the name of a tile for an
    image "out.tif" could look like this: "out_0.0_0.5_0.75_1.0.tif".
    The four values are the x1,x2,y1,y2 values of the crop window. Those
    values together with the resolution of the tile determine the resolution
    of the entire image. The position of the tile within that image is
    given by x1,y1.
    """
    
    inname,inext = os.path.splitext(filename)
    tilenames = glob.glob("%s*%s"%(inname,inext))

    # A list of tuples (tilename, coords, img)
    tiles = []
    mode = None
    # Filter tiles and fill the tiles list...
    for tilename in tilenames:
        # No tile at all?
        if not isTile(tilename):
            continue
        
        name,ext,coords = splitTileName(tilename)
        
        # A tile of another image?
        if name!=inname or ext!=inext:
            continue

        # Open the tile image...
        img = Image.open(tilename)

        # Set required mode
        if mode==None:
            mode = img.mode
        if img.mode!=mode:
            raise ValueError, "%s: Mode mismatch, %s instead of %s"%(tilename, img.mode, mode)

        tiles.append((tilename, coords, img))

    # No tiles? then exit
    if len(tiles)==0:
        if infostream!=None:
            print >>infostream, 'No image tiles found for image "%s"'%filename
        return


    # Create the output image...
    width, height, xposs, yposs = outputSpecs(tiles)
    mode = tiles[0][2].mode
    if infostream!=None:
        print >>infostream, "Final resolution: %dx%d, mode: %s"%(width, height, mode)
    outimg = Image.new(mode, (width, height))

    # Paste the tiles into the output image...
    for tilename, coords, img in tiles:
        x = xposs[coords[0]]
        y = yposs[coords[2]]
        outimg.paste(img, (x, y))

    # Delete the reference to the image
    img = None

    # Save the output image
    if infostream!=None:
        print >>infostream, "Stitched %d tiles"%len(tiles)
        print >>infostream, 'Saving "%s"...'%filename
    outimg.save(filename)

    # Remove tiles (if desired)
    if removetiles:
        if infostream!=None:
            print >>infostream, "Removing tiles..."
        # Get the tile names and delete the tiles list
        # so that the images are no longer referenced
        # (otherwise they couldn't be deleted)
        tilenames = map(lambda x: x[0], tiles)
        tiles = None
        for tilename in tilenames:
            os.remove(tilename)


######################################################################

def main():
    """Main function for the stitch command line tool.
    """
    
    usage = "usage: %prog [options] basenames"
    parser = optparse.OptionParser(usage)
    parser.add_option("-r", "--remove-tiles",
                      action="store_true", default=False,
                      help="Remove the tiles after stitching")

    opts, args = parser.parse_args()

    if len(args)==0:
        parser.print_help()
        sys.exit(0)
        
    for filename in args:
        stitch(filename, removetiles=opts.remove_tiles, infostream=sys.stdout)

######################################################################
        
if __name__=="__main__":
    try:
        main()
    except ValueError, e:
        print e
