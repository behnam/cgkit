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

## \file idmanager.py
## \brief Contains the IDManager class.

# Exceptions...
class IDNotAllocated(Exception):
    """Exception class."""
    pass

# IDManager
class IDManager:
    """This class manages IDs.

    This class is used to generate IDs for GUI elements such as menu items.
    You can call allocID() to get an unused ID and later on freeID() to
    make the ID available again.
    """
    def __init__(self, startid=1):
        """Constructor.

        \param startid (\c int) The starting value for the IDs (default: 1)
        """
        # Each interval is given by its start and its end (=last item+1)
        self._intervals = [[startid,None]]
        self._startid = startid

    def __call__(self):
        return self.allocID()

    # allocID
    def allocID(self):
        """Request an ID.

        \return An unused ID (\c int).
        """
        id = self._intervals[0][0]
        self._intervals[0][0]+=1
        # Is the interval eaten up? then remove it
        if self._intervals[0][0]==self._intervals[0][1]:
            del self._intervals[0]
        return id

    # freeID
    def freeID(self, id):
        """Releases an ID.

        \param id (\c int) A previously allocated ID
        """
        if id<self._startid:
            raise IDNotAllocated, "ID %d hasn't been allocated."%id
        
        idx = 0
        for istart,iend in self._intervals:
            if id<istart:
                break
            # Check if id is in the current interval (=attempt to free an ID
            # which wasn't allocated)
            if iend==None:
                iend = id+1
            if id>=istart and id<iend:
                raise IDNotAllocated, "ID %d hasn't been allocated."%id
            idx+=1

        # Is the freed id id directly before the interval
        if id==self._intervals[idx][0]-1:
            self._intervals[idx][0]-=1
            # Check if the interval can be merged with the previous interval
            if idx!=0 and self._intervals[idx-1][1]==self._intervals[idx][0]:
                self._intervals[idx-1][1]=self._intervals[idx][1]
                del self._intervals[idx]

        # Is the freed id directly behind the previous interval? then enlarge
        elif idx!=0 and id==self._intervals[idx-1][1]:
            self._intervals[idx-1][1]+=1
            # Check if the enlarged interval can be merged with its successor
            if self._intervals[idx-1][1]==self._intervals[idx][0]:
                self._intervals[idx-1][1]=self._intervals[idx][1]
                del self._intervals[idx]
        else:
            # Create a new interval with one element
            self._intervals.insert(idx,[id,id+1])



######################################################################
if __name__=="__main__":
    im = IDManager(5)
    print im.allocID()
    print im.allocID()
    print im.allocID()
    print im._intervals
    im.freeID(4)
    im.freeID(5)
    im.freeID(6)
    print im._intervals
    print im.allocID()
    print im._intervals
    print im.allocID()
    print im.allocID()
    
