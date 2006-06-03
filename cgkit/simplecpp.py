# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2004
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
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
            
