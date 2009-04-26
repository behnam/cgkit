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
import optparse
import os
import os.path
from cgkit import sequence


def main():
    parser = optparse.OptionParser(usage="%prog [options] sequences")
    opts,args = parser.parse_args()

    if len(args)<1:
        parser.print_usage()
        return
 
    for pattern in args:
        fseqs = sequence.glob(pattern)
        if len(fseqs)==0:
            print >>sys.stderr, '%s: No sequence "%s" found.'%(os.path.basename(sys.argv[0]), pattern)
            
        for fseq in fseqs:
            print "Deleting %s"%fseq
            for fileName in fseq:
                os.remove(str(fileName))
            
    return 0
    
##########################################################################

ret = main()
sys.exit(ret)

