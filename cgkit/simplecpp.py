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
# $Id: simplecpp.py,v 1.2 2006/01/27 22:11:09 mbaas Exp $

import types, os.path

# PreProcessor
class PreProcessor:
    """A simple 'preprocessor'.

    This class implements a subset of the functionality of the C preprocessor.

    So far, only comments are stripped (strings are properly processed, i.e.
    comment characters inside strings are ignored).
    """

    def __init__(self):
        # Flag that specifies if the starting position of the next line is
        # already inside a comment (i.e. if there was a '/*' without a '*/'
        self.inside_comment = False

    def __call__(self, source, errstream=None):
        """Preprocess a file or a file-like object.

        source may either be the name of a file or a file-like object.
        """
        if isinstance(source, types.StringTypes):
            filename = source
            # Read the input file
            f = open(filename)
            s = f.read()
            f.close()
        else:
            s = source.read()
            filename = getattr(source, "name", "<?>")

        # Filter
        s = self.filter(s)
        # Return the filtered text
        res = '# 1 "%s"\n%s'%(os.path.basename(filename), s)
        return res

    # filter
    def filter(self, s):
        """Filter a string (which may contain multiple lines).

        s may either be a string or a file-like object.
        """
        # If s is no string it must be a file-like object
        if not isinstance(s, types.StringTypes):
            s = s.read()
            
        reslist = map(lambda x: self.filterLine(x), s.split("\n"))
        return "\n".join(reslist)
       
    # filterLine
    def filterLine(self, s):
        """Filter one single line.
        """

        # Replace string contents with dots...
        s2 = s
        offset = 0
        while 1:
            # Search the beginning of a string
            n1 = s.find('"', offset)
            if n1==-1:
                break
            # Search the end of the string (ignore quoted apostrophes)...
            start = n1+1
            n2 = None
            while 1:
                n2 = s.find('"', start)
                if n2==-1:
                    break
                elif s[n2-1]!='\\':
                    break
                else:
                    start = n2+1
            if n2==-1:
                n2 = len(s2)
            le = n2-n1-1
            # Replace the string contents with dots
            s2 = s2[:n1+1] + le*"." + s2[n2:]
            offset += n2+1

        return self._filterLine(s,s2)
            
    def _filterLine(self, s1, s2):
        """Helper for the filterLine() method.
        """
        if self.inside_comment:
            n = s2.find("*/")
            if n==-1:
                return ""
            n+=2
            self.inside_comment = False
            return n*" " + self._filterLine(s1[n:], s2[n:])
        
        else:            
            n1 = s2.find("//")
            n2 = s2.find("/*")
          
            # No comment? then return the entire line
            if n1==-1 and n2==-1:
                return s1
            # Only a '//'? Then return the line without that comment
            elif n1!=-1 and (n2==-1 or n2>n1):                
                return s1[:n1]
            # Only a '/*'?
            elif n2!=-1 and (n1==-1 or n1>n2):
                pre = s1[:n2]
                self.inside_comment = True
                return pre+"  "+self._filterLine(s1[n2+2:], s2[n2+2:])
            
