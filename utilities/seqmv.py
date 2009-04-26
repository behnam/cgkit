#!/usr/bin/env python
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

import sys
import os.path
import string
import optparse
import shutil
from cgkit import sequence
from cgkit.sequence import SeqString

def promptUser(question):
    """Print a question and ask for y/n.
    
    Returns True when the user entered 'y'.
    """
    while 1:
        print question,
        answer = raw_input()
        answer = answer.lower()
        if answer=="n":
            return False
        if answer=="y":
            return True
        print "Expected 'y' or 'n'"


def outputNameSpec(fileSequence, dstName, newSequenceValues, force):
    """
    newSequenceValues is a boolean indicating whether the main sequence number
    will receive new values or if the values from the input sequence are used.
    
    Returns None when the user didn't confirm the operation.
    """
    ranges = fileSequence.ranges()
    
    # The index of the number that varies most (i.e. the index of the sequence number)
    seqNumIdx = fileSequence.sequenceNumberIndex()
            
    # This is a list containing the number indices of the numbers that will
    # make it into the destination name. The final length of this list must
    # match the number of patterns in the destination name.
    numIdxs = []
    numPatterns = sequence.numSubstitutionPatterns(dstName)
    numValues = len(ranges)
    numVaryingValues = len(filter(lambda rng: len(rng)>1, ranges))
    # Is the destination name without any pattern at all? Then append '#' if
    # there is a unique sequence number
    if numPatterns==0:
        if numVaryingValues==1 or newSequenceValues:
            numIdxs = [seqNumIdx]
            if len(dstName)>0 and dstName[-1] in string.digits:
                print "The destination name ends in a number which would affect the output sequence number."
                if not force and not promptUser("Are you sure to continue?"):
                    return None
            dstName = dstName+"#"
        elif numVaryingValues!=0:
            raise ValueError('Invalid destination name: "%s". Cannot figure out how to number the destination files. There are %s varying numbers.'%(dstName, numVaryingValues))
    # Does the number of patterns match the number of values? Then everything is fine. 
    elif numPatterns==numValues:
        numIdxs = range(numValues)
    # Does the number of patterns match the number of varying values? Then everything
    # is fine as well. The single-valued numbers are just ignored (which means
    # they are treated like a string)
    elif numPatterns==numVaryingValues:
        for i,rng in enumerate(ranges):
            if len(rng)>1:
                numIdxs.append(i)
    # Only 1 pattern (even though the source names have more (or less))?
    # Only accept this when a destination range was specified (as this means
    # name clashes won't occur because every file gets a unique number)
    elif numPatterns==1 and newSequenceValues:
        numIdxs = [seqNumIdx]
    else:
        if numValues==numVaryingValues:
            expectedStr = "%s pattern"%numValues
            if numValues>1:
                expectedStr += "s"
            
        else:
            expectedStr = "%s or %s patterns"%(numVaryingValues, numValues)
        if numPatterns>numValues:
            raise ValueError('Invalid destination name: "%s". There are too many substitution patterns (expected %s).'%(dstName, expectedStr))
        else:
            raise ValueError('Invalid destination name: "%s". There are not enough substitution patterns (expected %s).'%(dstName, expectedStr))
            
    # Adjust the index that refers to the sequence number (as we might have removed some numbers from the list)
    for i,idx in enumerate(numIdxs):
        if idx==seqNumIdx:
            seqNumIdx = i
            break
    else:
        raise RuntimeError, "Bug: Couldn't find the new sequence number index."

    return dstName, numIdxs, seqNumIdx

def buildFileTable(fileSequence, srcRange, dstName, dstRangeIterator, force):
    """Build the file table. 
    
    fileSequence is a Sequence object that contains the (full) source sequence.
    srcRange is a Range object that determines which files from fileSequence
    should be considered.
    dstName is the name pattern of the output sequence. dstRangeIterator
    is an iterator that yields the main output numbers. It may also be None
    in which case the numbers from the source files are used.
    force is a boolean indicating whether the user may get prompted for
    confirmation or not.
    
    The return value is a list of tuples (srcName,dstName,uiSrcName,uiDstName)
    where srcName/dstName is the full real path of the source/destination file.
    The ui names are the ones that have been specified on the command line
    and this is what gets printed when the --test flag is used.
    None is returned if the user didn't confirm the operation.
    
    The number of items in the returned list depends on the source range
    and the destination range iterator. If the latter runs out of numbers,
    any remaining source files are ignored.
    """
    res = outputNameSpec(fileSequence, dstName, dstRangeIterator is not None, force)
    if res is None:
        return None
    dstName, numIdxs, seqNumIdx = res
                
    # Assign output names to the input names...
    fileTable = []
    for srcName in fileSequence:
        baseName = os.path.basename(str(srcName))
        baseName,ext = os.path.splitext(baseName)
        baseName = SeqString(baseName)
        allNums = baseName.getNums()
        # The file numbers that are used on the output pattern
        nums = map(lambda i: allNums[i], numIdxs)

        # Only queue this file when it is part of the source range
        if len(nums)==0 or srcRange.contains(nums[seqNumIdx]):
            # If a destination range was specified then replace the
            # main file number with the next number in the range, otherwise
            # the number from the input file is used
            if dstRangeIterator is not None and len(nums)>0:
                try:
                    nums[seqNumIdx] = dstRangeIterator.next()
                except StopIteration:
                    break
            # Create the file names and add them to the list
            uiSrc = str(srcName)
            uiDst = sequence.replaceNums(dstName, nums)
            if os.path.splitext(uiDst)[1]!=ext:
                uiDst += ext
            src = os.path.realpath(uiSrc)
            dst = os.path.realpath(uiDst)
            fileTable.append((src, dst, uiSrc, uiDst))
  
    return fileTable

def checkCollisions(fileTable, srcFiles):
    """Check if moving/renaming the files would lead to collisions.
    
    fileTable is a list of tuples where the first two items are the
    srcName and the dstName. There may be additional items per tuple which
    are just ignored.
    srcFiles is the list of initial files as they exist on disk (the strings
    must match the srcName strings in fileTable).
    """
    fileDict = {}
    # Initialise the file dict with the source files
    for name in srcFiles:
        fileDict[name] = 1
        
    # Simulate the rename operations and check if there is a collision
    for item in fileTable:
        srcName = item[0]
        dstName = item[1]
        del fileDict[srcName]
        if fileDict.has_key(dstName):
            return True
        fileDict[dstName] = 1
        
    return False

def resolveCollisions(fileTable, srcFiles):
    """Modify the file table, so that moving files doesn't resolve in collisions.
    
    Collisions are only checked among the file in the table, it is not checked
    that a move operation would overwrite a file on disk.
    Returns the new file table (the old table might have been modified!).
    
    srcFiles is the list of initial files as they exist on disk (the strings
    must match the srcName strings in fileTable).
    
    Raises an exception if collisions cannot be resolved (this can happen
    when the sequence contains file like img1.tif and img01.tif which might
    both get mapped to the same output file name).
    """
    # Check if renaming in the current order would result in a collision.
    if checkCollisions(fileTable, srcFiles):
        # Try the reverse order instead
        fileTable.reverse()
                
        # If this still collides, then use a temporary name
        if checkCollisions(fileTable, srcFiles):
            fileTable.reverse()
            tab1 = []
            tab2 = []
            for item in fileTable:
                srcName = item[0]
                dstName = item[1]
                uiSrcName = item[2]
                uiDstName = item[3]
                
                p,n = os.path.split(dstName)
                tmpName = os.path.join(p, "__tmp__"+n)
                p,n = os.path.split(uiDstName)
                uiTmpName = os.path.join(p, "__tmp__"+n)
                
                tab1.append((srcName,tmpName,uiSrcName,uiTmpName))
                tab2.append((tmpName,dstName,uiTmpName,uiDstName))
            fileTable = tab1+tab2
            
            if checkCollisions(fileTable, srcFiles):
                raise ValueError("Cannot resolve collisions because of inconsistent sequence numbering. A file from the input sequence would overwrite another file from the same sequence.")

    return fileTable

def main():
    parser = optparse.OptionParser(usage="%prog [options] src dst")
    parser.add_option("-s", "--source-frames", default="0-", metavar="FRAMES", help="Specify a subset of the source frames")
    parser.add_option("-d", "--destination-frames", default=None, metavar="FRAMES", help="Specify the destination numbers")
    parser.add_option("-f", "--force", action="store_true", default=False, help="Never query the user for confirmation")
    parser.add_option("-t", "--test", action="store_true", default=False, help="Only print what would be done, but don't move anything")
    opts,args = parser.parse_args()

    if len(args)!=2:
        parser.print_usage()
        return

    # The source frame numbers
    srcRange = sequence.Range(opts.source_frames)
    
    # The destination frame numbers
    dstRangeIterator = None
    if opts.destination_frames is not None:
        dstRangeIterator = iter(sequence.Range(opts.destination_frames))

    srcSeq = args[0]
    dstArg = args[1]        
    
    # Determine the source sequences
    fseqs = sequence.glob(srcSeq)
    
    # Build the file table
    fileTable = []
    for fseq in fseqs:
        if os.path.isdir(dstArg):
            dstName = os.path.join(dstArg, os.path.basename(fseq.sequenceName()[0]))
        else:
            dstName = dstArg
        ftab = buildFileTable(fseq, srcRange, dstName, dstRangeIterator, force=opts.force)
        if ftab is None:
            return
        fileTable.extend(ftab)

        # Print the final source and destination sequence (just for user info)
        if ftab!=[]:
            srcSeq = sequence.Sequences(map(lambda x: x[2], ftab))[0]
            dstSeq = sequence.Sequences(map(lambda x: x[3], ftab))[0]
            print "Move: %s -> %s"%(srcSeq, dstSeq)
            
    # Resolve collisions
    srcFiles = map(lambda t: t[0], fileTable)
    fileTable = resolveCollisions(fileTable, srcFiles)
                
    # Check if a rename would overwrite an existing file that is not from the
    # input sequence...
    if not opts.force:
        srcDict = {}
        for srcName in srcFiles:
            srcDict[srcName] = 1
        dstFiles = map(lambda t: t[1], fileTable)
        overwrites = []
        for dstName in dstFiles:
            if dstName not in srcDict and os.path.exists(dstName):
                overwrites.append(dstName)
                
        if len(overwrites)>0:
            if not promptUser("Overwrite %s files?"%len(overwrites)):
                return
            
    # Move the files
    for item in fileTable:
        srcName = item[0]
        dstName = item[1]
        # Are the source and destination names the same? then skip this one
        if srcName==dstName:
            continue
        
        if opts.test:
            uiSrcName = item[2]
            uiDstName = item[3]
            print uiSrcName,"->",uiDstName
        else:
            shutil.move(srcName, dstName)

##########################################################################
try:
    main()
except SystemExit:
    pass
except KeyboardInterrupt:
    print >>sys.stderr, "\nUser abort"
except:
    print >>sys.stderr, "ERROR:",sys.exc_info()[1]
    raise
    sys.exit(1)
