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
# $Id: rmshader.py,v 1.9 2006/05/26 21:33:29 mbaas Exp $

import string
import os.path
import re
import glob as _glob
import copy

class SeqString:
    """Sequence string class.

    Sequence strings treat numbers inside a strings as integer numbers
    and not as strings. This can be used to sort numerically (e.g.
    'anim01' is smaller than 'anim0002').

    A sequence string is initialized by passing a regular string to
    the constructor or by calling setString().
    The main task of a SeqString is comparing two strings which can
    be done with the normal comparison operators. Example:

    >>> a = SeqString('a08')
    >>> b = SeqString('a2')
    >>> a<b
    False
    >>> a>b
    True
    """
    
    def __init__(self, s=None):
        """Constructor.

        The sequence string is initialized with s which can be a regular 
        string, another SeqString or anything else that can be turned into
        a string using str(s). s can also be None which is equivalent
        to an empty string.
        """
        # This is an alternating sequence of text and number values
        # (always beginning with a text (which might be empty)).
        # The value part is a tuple (value,numdigits) where value
        # is an integer and numdigits the number of digits the
        # value was made of.
        # Example: 'anim1_0001.png' -> ['anim', (1,1), '_', (1,4), '.png']
        self._value = []
        
        self.setString(s)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Convert the sequence string into a normal string.

        The number of digits is maintained. The result is the original
        string.
        """
        
        res=""
        for i, vn in enumerate(self._value):
            if i%2==0:
                res += vn
            else:
                val,ndigits = vn
                a = '%'+"0%dd"%ndigits
                res += a%val
        return res   

    def __cmp__(self, other):
        """Comparison operator.

        The text parts are treated as strings, the number parts as numbers
        (e.g. 'a08' is greater than 'a2').
        """

        if other is None:
            return 1
        
        # Check the 'structure' of the strings first.
        # The numeric comparison is only done when the strings have the same
        # text/num patterns.
        res = self.match_cmp(other)
        if res!=0:
            return res

        # Compare the individual components of the values side by side
        for i, (a,b) in enumerate(zip(self._value, other._value)):
            if i%2==1:
                # Get the numbers
                a = a[0]
                b = b[0]

            if a<b:
                return -1
            if a>b:
                return 1

        # If we are here everything has been equal so far, but maybe
        # one string has one component more in _value
        return cmp(len(self._value), len(other._value))
        
    def setString(self, s):
        """Initialize the sequence string with a string.

        s can either be a regular string, another sequence string (to create
        a copy) or anything else that can be turned into a string using str(s).
        s can also be None which is equivalent to passing an empty string.
        Internally, the string is split into its text components and
        number components.
        """
        if s is None:
            s = ""
            
        s = str(s)
        textbuf = ""
        numtup = (0,0)
        res = []
        # State
        z = 0

        for c in s:
            # State: Collect text
            if (z==0):
                # Is this the beginning of a number?
                if (c in string.digits):
                    res.append(textbuf)
                    numtup  = (0,1)
                    textbuf = c
                    z = 1
                # Store text in buffer
                else:
                    textbuf += c
            # State: Collect number
            else:
                # Another digit?
                if (c in string.digits):
                    numtup = (0,numtup[1]+1)
                    textbuf += c
                # No more digits
                else:
                    numtup = (int(textbuf),numtup[1])
                    res.append(numtup)
                    textbuf = c
                    z = 0

        # Add last value
        if (z==0):
             res.append(textbuf)
        else:
             numtup = (int(textbuf),numtup[1])
             res.append(numtup)

        self._value = res

    def match(self, template, numPos=None):
        """Check if one sequence string is equal to another except for one or all numbers.

        Returns True if the text parts of self and template are equal,
        i.e. both strings belong to the same sequence.
        
        numPos is the index of the number that is allowed to vary. For example,
        if numPos is -1, the last number in a string may be different for two
        strings to be in the same sequence. If numPos is None, all numbers
        may vary.
        """

        # The lengths of the value lists must be equal
        if len(self._value)!=len(template._value):
            return False
        
        if numPos is not None:
            if numPos<0:
                numPos = self.numCount()+numPos
            numPos = 2*numPos + 1
        
        for i, (va,vb) in enumerate(zip(self._value, template._value)):
            # Only compare the text parts and ignore the numbers
            if i%2==0:
                if va!=vb:
                    return False
            elif numPos is not None and i!=numPos and va[0]!=vb[0]:
                return False
            
        return True

    def match_cmp(self, template):
        """Comparison function to build groups.

        This is the same as match() but with a different return value
        so that this method can be used as comparison function for sort().
        
        0: self==template, <0: self<template, >0: self>template
        """

        a = self.groupRepr()
        b = template.groupRepr()
        return cmp(a,b)

    def groupRepr(self, numChar="*"):
        """Return a template string where the numbers are replaced by the given character.
        """
        
        res=""
        for i,v in enumerate(self._value):
            if i%2==0:
                res += v
            else:
                res += numChar
        return res   

    def numCount(self):
        """Return the number of number occurrences in the string.

        Example: 'anim01.tif'    -> 1
                 'anim1_018.tif' -> 2
                 'anim'          -> 0
        """
        return int(len(self._value)/2)

    def getNum(self, idx):
        """Return a particular number inside the string.

        idx is the index of the number (0-based) which may also be
        negative. The return value is an integer containing the number
        at that position. 
        Raises an IndexError exception when idx is out of range.
        """

        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        return self._value[idx*2+1][0]

    def getNumStr(self, idx):
        """Return a particular number as a string just as it appears in the original string.

        idx is the index of the number (0-based) which may also be
        negative. The return value is a string that contains the number
        as it appears in the string (including padding).
        Raises an IndexError exception when idx is out of range.
        """

        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        val,ndigits = self._value[idx*2+1]
        a = '%'+"0%dd"%ndigits
        return a%val
    
    def getNums(self):
        """Return all numbers.
        
        Returns a list of all numbers in the order as they appear in the string. 
        """
        res=[]
        for i in range(self.numCount()):
            res.append(self.getNum(i))

        return res

    def setNum(self, idx, value):
        """Set a new number.

        idx is the index of the number (may be negative) and value
        is the new integer value.
        Raises an IndexError exception when idx is out of range.
        """
        
        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        value = int(value)
        width = self._value[idx*2+1][1]
        self._value[idx*2+1] = (value,width)

    def getNumWidth(self, idx):
        """Return the number of digits of a particular number.

        idx is the index of the number (may be negative).
        Raises an IndexError exception when idx is out of range.
        """
        
        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        return self._value[idx*2+1][1]

    def setNumWidth(self, idx, width):
        """Set the number of digits of a number.

        idx is the index of the number (may be negative) and width
        the new number of digits.
        Raises an IndexError exception when idx is out of range.
        """
        
        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        width = int(width)
        val = self._value[idx*2+1][0]
        self._value[idx*2+1] = (val,width)

    def getNumWidths(self):
        """Return the number of digits of all numbers.
        
        Returns a list of width values.
        """
        res=[]
        for i in range(self.numCount()):
            res.append(self.getNumWidth(i))

        return res

    def setNumWidths(self, widths):
        """Set the number of digits for all numbers.
        
        widths must be a list of integers. The number of values may not
        exceed the number count in the string, otherwise an IndexError
        exception is thrown.
        """
        for i in range(len(widths)):
            self.setNumWidth(i,widths[i])
            
    def deleteNum(self, idx):
        """Delete a number inside the string.

        idx is the index of the number (0-based) which may also be
        negative.
        Raises an IndexError exception when idx is out of range.
        """
        self.replaceNum(idx, "")

    def replaceNum(self, idx, txt):
        """Replace a number by a string.

        idx is the index of the number (0-based) which may also be
        negative. txt is a string that will replace the number.
        Raises an IndexError exception when idx is out of range.
        """
        
        if idx<0:
            idx = self.numCount()+idx
        if idx<0 or idx>=self.numCount():
            raise IndexError, "index out of range"

        # Insert the text
        self._value[idx*2] += str(txt)
        # Concatenate the adjacent texts
        if len(self._value)>idx*2+2:
            self._value[idx*2] += self._value[idx*2+2]
        # Remove the number
        del self._value[idx*2+1:idx*2+3]


class Sequence:
    """A list of names that all belong to the same sequence.
    
    The class can be used like a list (using len(), index operator or iteration).
    """
    
    def __init__(self):
        """Constructor.
        """
        # A list of file names (stored as SeqString objects)
        self._names = []
    
    def __str__(self):
        placeholder,ranges = self.sequenceName()
        if len(ranges)==0:
            return placeholder
        else:
            return "%s (%s)"%(placeholder, "; ".join(ranges))
    
    def __len__(self):
        return len(self._names)
    
    def __getitem__(self, key):
        """Return an element as a SeqString.
        """
        return self._names[key]
    
    def match(self, name, numPos=None):
        """Check if a name matches the names in this sequence.
        
        If the sequence doesn't contain any name at all yet, then any name
        will match.
        """
        if len(self._names)==0:
            return True
        else:
            return self._names[0].match(name, numPos)

    def append(self, name):
        """Add a file name to the group.
        
        name can be a SeqString object or a regular string.
        The name is added unconditionally, so it's the callers responsibility
        to make sure the file really belongs to this sequence.
        """
        if not isinstance(name, SeqString):
            name = SeqString(name)

        self._names.append(name)
        
    def sequenceNumberIndex(self):
        """Return the index of the sequence number.
        
        Returns the index of the number that has the most variation among its
        values. If two numbers have the same amount of values, the last
        number is used.
        Returns None if there is no number at all.
        """
        ranges = self.ranges()
        
        # This will be the index of the number that varies most (i.e. the index of the sequence number)
        seqNumIdx = None
        maxValues = -1
        for i,rng in enumerate(ranges):
            lr = len(rng)
            if lr>=maxValues:
                maxValues = lr
                seqNumIdx = i
        
        return seqNumIdx
        
    def ranges(self):
        """Return a list of all the number ranges in the sequence.
        
        The return value is a list of Range objects. There are as many
        ranges as there are separate numbers in the names. The ranges
        are given in the same order as the corresponding number appears in
        the names.
        """
        name,rangeStrs = self._nameAndRangeStrs()
        return map(lambda x: Range(x), rangeStrs)

    def sequenceName(self):
        """Return a sequence placeholder and range strings.
        
        Returns a tuple (placeholder, ranges) where placeholder is the
        name of a member of the sequence where all numbers have been replaced
        by '#' (=0-padded number with 4 digits) or one or more '@' (=padded
        number with as many digits as there are '@' characters. Just a single
        '@' represents an unpadded number). If the sequence contains inconsistent
        padding, the number is replaced by '*'.
        The number is not replaced at all if there is only one single value
        among all file names anyway.
        ranges is a list of strings where each string describes the range
        of values of the corresponding number in the placeholder string.
        
        The returned information is meant to be displayed to the user as
        information about the sequence. It is not possible to reconstruct
        all original file names (unless the placeholder contains no more than
        one substitution).
        """
        name,rangeStrs = self._nameAndRangeStrs(ignoreSingleValues=True)
        return name,rangeStrs
        
        
    def _nameAndRangeStrs(self, ignoreSingleValues=False):
        """Helper method for sequenceName() and ranges().
        
        Returns a tuple (placeholder, ranges). See sequenceName().
        if ignoreSingleValues is True, any number in the sequence names
        whose range only consists of a single value will not be replaced
        by # or @ and will not appear in the "ranges" list.
        """
        if len(self._names)==0:
            return "", []
        
        # How many numbers do we have in the string?
        n = self._names[0].numCount()
        if n==0:
            return str(self._names[0]), []
        
        # The minimum width of every number
        minWidths = self._names[0].getNumWidths()
        # The maximum width of every number
        maxWidths = list(minWidths)
        # A flag indicating whether the number is unpadded or not
        unpadded = len(minWidths)*[True]
        # A list of values
        values = []
        for i in range(n):
            values.append([])
                
        # Collect all required values from the names
        for name in self._names:
            for i in range(name.numCount()):
                v = name.getNum(i)
                w = name.getNumWidth(i)
                
                # Update the minimum width
                minWidths[i] = min(w, minWidths[i])
                # Update the maximum width
                maxWidths[i] = max(w, maxWidths[i])
                # Update the unpadded flag
                if len(str(v))<w:
                    unpadded[i] = False
                # Update the value list (don't append if the last value is the same as v)
                if len(values[i])==0 or values[i][-1]!=v:
                    values[i].append(v)
                    
        # Compute the sequence name that has the numbers replaced by placeholders
        res = copy.deepcopy(self._names[0])
        rangeStrs = []
        for i in range(len(minWidths)):
            # If there is only one single value anyway then just leave the number
            if ignoreSingleValues and len(values[i])==1:
                # The index is 0 because previous number have already been replaced by strings
                s = res.getNumStr(0)
            else:
                rangeStrs.append(compactRange(values[i]))
                if unpadded[i]:
                    s = "@"
                else:
                    if minWidths[i]==maxWidths[i]:
                        n = minWidths[i]
                        if n==4:
                            s = "#"
                        else:
                            s = n*"@"
                    else:
                        s = "*"
            # The number index is always 0 because we are replacing the numbers
            # one by one (which reduces the numcount)
            res.replaceNum(0, s)
            
        return str(res), rangeStrs

class Sequences:
    """A collection of sequences.
    """
    
    def __init__(self, names=[], assumeFiles=False):
        """Constructor.
        
        names is a list of strings that will be grouped into sequences.
        """
        # A list of FileSequence objects
        self._sequences = []
        
        # Create the sequences
        self.setFiles(names, assumeFiles=assumeFiles)

    def __str__(self):
        return "<Sequences: %d sequences>"%len(self._sequences)

    def __len__(self):
        return len(self._sequences)

    def __getitem__(self, key):
        """Return the Sequence object with the given index.
        """
        return self._sequences[key]

    # clear
    def clear(self):
        """Remove all sequences.
        """
        self._sequences = []

    # setFiles
    def setFiles(self, names, numPos=None, assumeFiles=False):
        """Initialize the sequences given a flat list of names.
        
        names is a list of objects (usually strings) that are turned into
        SeqString objects and grouped into sequences.
        if assumeFiles is True, the input strings are assumed to be file
        names. In this case, it will be ensured that files from different
        directories are put into different sequences and any number occurring
        in the directory part is "frozen" (turned into a string).
        """

        self.clear()

        # Convert the names into SeqString objects and sort them (numerically)...
        # The order of the result is already so that members of the same
        # sequence are together, we just don't know yet where a sequence ends
        # and the next one begins.
        seqnames = map(SeqString, names)
        seqnames.sort()
        
        # Build sequences...
        currentSeq = Sequence()
        currentPath = None
        for name in seqnames:
            # Are we dealing with file names? Then freeze directory numbers...
            if assumeFiles:
                path,n = os.path.split(str(name))
                pathseq = SeqString(path)
                # n: The number count in the path (these numbers have to be frozen)
                n = pathseq.numCount()
                for i in range(n):
                    name.replaceNum(i, name.getNumStr(i))
                
            sequenceSplit = False
            
            # Check if the current name has a different structure or different
            # text parts as the names in the current sequence. If so, we
            # have to begin a new sequence            
            if not currentSeq.match(name, numPos):
                sequenceSplit = True
                
            # If we are dealing with file names, then make sure files in
            # different directories are put into separate sequences (even
            # when the names have the same structure).
            if assumeFiles:
                # path has been set above where the directory numbers were frozen
                if currentPath is not None and path!=currentPath:
                    sequenceSplit = True
                    currentPath = path
                                        
            # Do we have to begin a new sequence?
            if sequenceSplit:
                self._sequences.append(currentSeq)
                currentSeq = Sequence()
                
            # Add the current name to the current sequence
            currentSeq.append(name)

        # Also store the last sequence generated (if it isn't empty)
        if len(currentSeq)>0:
            self._sequences.append(currentSeq)


class Range:
    """Range class.
    
    This class represents a sequence of integer values (frame numbers).
    The sequence is composed of a number of sub-ranges which have a begin,
    an optional end and a step number.
    """
    
    def __init__(self, rangeStr=None):
        """Constructor.
        """
        # The individual sub-ranges.
        # This is a list of tuples (begin,end,step) where each value is an integer.
        # begin is the first value of the range, end the last value or None
        # for an infinite sub-range. step is the difference between subsequent
        # values.
        # The following conditions must always be met by all items:
        # - end>=begin (if end is not None)
        # - (end-begin)%step == 0
        self._ranges = []
        
        # Set the initial range
        self.setRange(rangeStr) 
            
    def __str__(self):
        """Return a string describing the range.
        """
        rangeStrs = []
        for begin,end,step in self._ranges:
            if begin==end:
                rangeStrs.append(str(begin))
            else:
                if step==1:
                    stepStr = ""
                else:
                    stepStr = "x%s"%step
                    
                if end is None:
                    endStr = ""
                else:
                    endStr = str(end)
                    
                rangeStrs.append("%s-%s%s"%(begin,endStr,stepStr))
                                
        return ",".join(rangeStrs)
    
    __repr__ = __str__
            
    def __len__(self):
        """Return the number of values in the sequence.
        
        A ValueError exception is thrown if the sequence is infinite.
        """
        res = 0
        for begin,end,step in self._ranges:
            if end is None:
                raise ValueError("Cannot return length of infinite range")
            res += int((end-begin)/step)+1
        return res
            
            
    def __iter__(self):
        """Iterate over all individual values in the range.
        
        The values are reported in increasing order. No value is reported twice.
        Note that the sequence will be infinite if isInfinite() returns True.
        """
        # Copy the _ranges list and convert the tuples to lists.
        # The "begin" value will be increased during the iteration.
        currentValues = map(lambda x: list(x), self._ranges)
        
        # Advance all sub-ranges in parallel and always yield the minimum
        # value. The ensures that the iteration is done in order and no value
        # is reported twice.
        while len(currentValues)>0:
            # The next value is the minimum "begin" value...
            nextVal = min(map(lambda x: x[0], currentValues))
            # Report the value
            yield nextVal

            # Now increase all "begin" values that are equal to the current value
            for i in range(len(currentValues)):
                current,end,step = currentValues[i]
                if current==nextVal:
                    current += step
                    if end is not None and current>end:
                        # Replace the tuple with None (so that it gets removed later on)
                        currentValues[i] = None
                    else:
                        # Set the new step value
                        currentValues[i][0] = current
                    
            # Remove the deleted items (the ones that are None)
            currentValues = filter(lambda x: x is not None, currentValues)
                
    def isInfinite(self):
        """Check if the range is infinite.
        """
        for begin,end,step in self._ranges:
            if end is None:
                return True
            
        return False        
                
    def contains(self, val):
        """Check if a value is inside the range.
        
        val is an integer that is checked against the range. The method
        returns True when the value is part of the range.
        """
        for begin,end,step in self._ranges:
            if val>=begin and (end is None or val<=end) and (val-begin)%step==0:
                return True
        return False

    def setRange(self, rangeStr):
        """Initialize the range object with a new range string.
        
        The range string may contain individual numbers or ranges separated by
        comma. The individual ranges are specified by a begin, an end (inclusive)
        and an optional step number.
        This is the opposite function to compactRange().
        
        Examples:
        
        "1,5,10" -> [1,5,10]
        "1-5" -> [1,2,3,4,5]
        "2-8x2" -> [2,4,6,8]
        "1-3,10-13" -> [1,2,3,10,11,12,13] 
        """
        
        if rangeStr is None:
            rangeStr = ""

        reRange = re.compile(r"([0-9]+)(?:-([0-9]*)(?:x([0-9]+))?)?$")

        self._ranges = []
        for rs in rangeStr.split(","):
            rs = rs.strip()
            if rs=="":
                continue
            # Matches a single number, a range without step and a range with step
            m = reRange.match(rs)
            if m is not None:
                begin = int(m.group(1))
                end = m.group(2)
                step = m.group(3)
                if step is None:
                    step = 1
                else:
                    step = int(step)
                if end is None:
                    end = begin
                else:
                    if end=="":
                        end = None
                    else:
                        end = int(end)
                        # Adjust the end so that it is actually part of the
                        # sequence (i.e. 1-10x2 -> 1-9x2)
                        end -= (end-begin)%step
                if end is None or end>=begin:
                    self._ranges.append((begin,end,step))
            else:
                raise ValueError("Invalid range string: %s"%rs)

        self._ranges.sort()
        
        
def compactRange(values):
    """Build the range string that lists all values in the given list in a compacted form.
    
    values is a list of integers (may contain duplicate values and doesn't have
    to be sorted). The return value is a string that lists all values (sorted)
    in a compacted form (using the same syntax that Shake accepts as time values).
    The returned range string can be passed to a Range object to create the
    expanded integer sequence again.
    
    Example: [1,2,3,4,5,6]    -> "1-6"
             [2,4,6,8]        -> "2-8x2"
             [1,2,3,10,11,12] -> "1-3,10-12"
    """
    if len(values)==0:
        return ""
    
    values.sort()
    
    # Set the initial value of the range list. The list contains
    # lists [start,end,step].
    v = values[0]
    rangeList = [[v,v,None]]
    
    # Build the range list
    for v in values[1:]:
        r = rangeList[-1]
        begin,end,step = r
        if v!=end:
            if begin==end:
                step = v-begin
                r[2] = step
            if end+step==v:
                r[1] = v
            else:
                rangeList.append([v,v,None])
                
    # Go through all individual ranges and check if ranges that only contain
    # two values can be changed so that the end value is put into the
    # subsequent range (e.g. 1-100x99,101 -> 1,100-101)
    for i in range(len(rangeList)-1):
        begin,end,step = rangeList[i]
        # Is this a range containing 2 values? Then check if it's advantageous
        # second value can be moved into the subsequent range
        if begin!=end and (end-begin)/step==1:
            begin2,end2,step2 = rangeList[i+1]
            # The second range only contains 1 value? Then only move
            # when the new step is smaller than the old step in the first range
            if begin2==end2:
                step2 = begin2-end
                if step2<step:
                    begin2 = end
                    rangeList[i+1][0] = begin2
                    rangeList[i+1][2] = step2
                    rangeList[i][1] = begin
            # The second range contains several values, so check if actually
            # can add the end value from the previous range
            else:
                if begin2-step2==end:
                    begin2 = end
                    rangeList[i+1][0] = begin2
                    rangeList[i][1] = begin
                   
    # Collapse the range list into strings (such as "1-99,110,200-220x2", etc)
    rs = []
    for r in rangeList:
        begin,end,step = r
        if begin==end:
            rs.append(str(begin))
        else:
            # Step is 1? Then leave it out
            if step==1:
                rs.append("%s-%s"%(begin,end))
            # This sub-range only consists of two values (and step is not 1)? Then list individually
            elif (end-begin)/step==1:
                rs.append("%s,%s"%(begin,end))
            # Full sub-range, including step
            else:
                rs.append("%s-%sx%s"%(begin,end,step))
                
    return ",".join(rs)

def glob(name):
    """Create file sequences.
    
    name is a file pattern that will get a '*' appended. The pattern is then
    passed to the regular glob() function to obtain a list of files which
    are then grouped into sequences.
    Returns a Sequences objects that contains all file sequences found.
    """
    globpattern = name
    if not globpattern.endswith("*"):
        globpattern += "*"
        
    # Replace number substitution pattern by wildcards (this might result
    # in files being reported that are actually not valid because they either
    # contain strings instead of numbers or the padding is not as specified)
    globpattern = globpattern.replace("#", "????")
    while 1:
        m = re.search(r"@+", globpattern)
        if m is None:
            break
        globpattern = "%s%s%s"%(globpattern[:m.start()], "?*", globpattern[m.end():])
        
    # Create a regular expression to filter the glob result
    regexp = []
    s = name
    while 1:
        m = re.search(r"\*|#|@+", s)
        if m is None:
            regexp.append(re.escape(s))
            break
        p = m.group()
        regexp.append(re.escape(s[:m.start()]))
        if p=="*":
            regexp.append(".*")
        elif p=="#":
            regexp.append("[0-9][0-9][0-9][0-9]")
        else:
            r = len(p)*"[0-9]"
            r = "(%s|[1-9][0-9]{%s,})"%(r,len(p))
            regexp.append(r)
        s = s[m.end():]

    regexp = "".join(regexp)
    
    # Get a list of potential file names    
    fileNames = _glob.glob(globpattern)
    
    # Remove all directories
    fileNames = filter(lambda n: not os.path.isdir(n), fileNames)
    
    # Remove files that don't match the regular expression
    reg = re.compile(regexp)
    fileNames = filter(lambda n: reg.match(n) is not None, fileNames)
    
    # Remove files that don't have any number in their name (without ext)
    fileNames = filter(lambda n: SeqString(os.path.splitext(n)[0]).numCount()>0, fileNames)
    
    return Sequences(fileNames, assumeFiles=True)
    
def numSubstitutionPatterns(pattern):
    """Return the number of substitution patterns inside a string.
    
    Returns the number of occurrences of a single '#' or a sequence of '@'
    character.
    """
    rexp = re.compile(r"#|@+")
    res = 0
    while 1:
        m = rexp.search(pattern)
        if m is None:
            break
        res += 1
        pattern = pattern[m.end():]
    return res
    
def replaceNums(pattern, nums):
    """Replace number patterns inside a string.
    
    pattern is a string that contains '#' or '@' characters. A single '#'
    represents a padded number with 4 digits whereas a sequence of '@'
    characters represents a number of that width. If a number is larger than
    the specified width, the final width will be larger as well (i.e. the
    number is not clipped).
    nums is a list of integers. For each number in the list, the pattern
    string must contain exactly one number substitution pattern.
    """
    if len(nums)==1:
        patternMsg = "pattern"
    else:
        patternMsg = "patterns"
        
    s = pattern
    for num in nums:
        n1 = s.find("#")
        n2 = s.find("@")
        if n1!=-1 and (n2==-1 or n1<n2):
            s = "%s%04d%s"%(s[:n1], num, s[n1+1:])
        elif n2!=-1 and (n1==-1 or n2<n1):
            n = 1
            while n2+n<len(s) and s[n2+n]=="@":
                n += 1
            sdef = "%%s%%0%dd%%s"%n
            s = sdef%(s[:n2], num, s[n2+n:])
        else:
            raise ValueError("No matching number substitution pattern found: %s (expected %s %s)"%(pattern, len(nums), patternMsg))
            
    if s.find("#")!=-1 or s.find("@")!=-1:
        raise ValueError("Too many number substitution patterns: %s (only expected %s %s)"%(pattern,len(nums), patternMsg))
        
    return s

