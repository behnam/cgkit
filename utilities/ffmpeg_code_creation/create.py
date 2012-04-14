#!/usr/bin/env python
# ffmpeg wrapper generation.
# Uses ctypeslib (h2xml.py, xml2py.py): http://pypi.python.org/pypi/ctypeslib/

import sys, os, os.path, re, glob, subprocess, shutil, ctypes

license = """# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the License); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the GPL), or
# the GNU Lesser General Public License Version 2.1 or later (the LGPL),
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
"""

class DefinesCollector:
    """Turn #defines into enum.

    This class reads all ffmpeg headers, extracts the #defined symbol names
    and turns some selected symbols into enums so they can be processed by
    the subsequent wrapping tools (so that gccxml sees and maintains them).
    """

    def __init__(self, out, log):
        """Constructor.
        
        out is a file object that will receive the generated header file.
        log is a stream where log information is written.
        """
        self.out = out
        self.log = log

    def createHeader(self, includePath):
        """Create the header containing the enums.
        
        includePath is the main include path where the ffmpeg headers are.
        """
        defineNames = self.readAllDefinitions(includePath)
    
        self.createEnum(defineNames, "AVERROR_.*")
        self.createEnum(defineNames, "LIBAVCODEC_VERSION_.*")
        self.createEnum(defineNames, "LIBAVFORMAT_VERSION_.*")
        self.createEnum(defineNames, "LIBAVUTIL_VERSION_.*")
        self.createEnum(defineNames, "LIBAVFILTER_VERSION_.*")
        self.createEnum(defineNames, "LIBSWSCALE_VERSION_.*")
        
        # libavcodec/avcodec.h
        self.createEnum(defineNames, "CODEC_FLAG_.*")
        self.createEnum(defineNames, "CODEC_TYPE_.*")
        self.createEnum(defineNames, "AV_TIME_BASE$")
        
        # libavformat/avio.h
        self.createEnum(defineNames, "URL_[WR].*")
        
        # libavformat/avformat.h")
        self.createEnum(defineNames, "MAX_STREAMS")
        self.createEnum(defineNames, "AVSEEK_FLAG_.*")
        self.createEnum(defineNames, "AVFMT_.*")
        
        # libswscale/swscale.h
        self.createEnum(defineNames, "SWS_.*", exclude=["SWS_MAX_REDUCE_CUTOFF"])

    def findDefinitions(self, headerName):
        """Return the names of all #defines in the given header file.
        
        Returns a list of names.
        """
        names = set()
        for line in open(headerName, "rt"):
            line = line.strip()
            if line.startswith("#define"):
                f = line.split()
                names.add(f[1])
        
        return list(names)

    def readAllDefinitions(self, includePath):
        """Read the symbol names from all ffmpeg headers.
        
        This calls findDefinitions() on all ffmpeg headers and collects the symbol
        names. See findDefinitions() for more info.
        includePath is the main include path where the ffmpeg headers are.
        Returns a list of names. 
        
        Example: If the headers contained the following lines:
        
           #define spam 12
           #define eggs 19
           
        then the returned list would be: ["spam", "eggs"]
        """
        headers = glob.glob(os.path.join(includePath, "libavcodec", "*.h"))
        headers.extend(glob.glob(os.path.join(includePath, "libavformat", "*.h")))
        headers.extend(glob.glob(os.path.join(includePath, "libavfilter", "*.h")))
        headers.extend(glob.glob(os.path.join(includePath, "libswscale", "*.h")))
        headers.extend(glob.glob(os.path.join(includePath, "libavutil", "*.h")))
        headers.extend(glob.glob(os.path.join(includePath, "libavdevice", "*.h")))
        
        self.log.write("Extracting #defines from %s ffmpeg headers...\n"%len(headers))
        
        defNames = []
        for header in headers:
            self.log.write("    %s..."%header)
            defs = self.findDefinitions(header)
            self.log.write("\t%s #defines\n"%len(defs))
            defNames.extend(defs)
        
        return defNames
    
    def createEnum(self, names, pattern, exclude=None):
        """Create an enum from a list of names.
        
        names is a list of symbol names that should be the values of the enum.
        For every name, the enum will create an entry like this:
        
        enum {
            ...
            _WRAP_<name> = <name>,
            ...
        }
        
        <name> is supposed to be a name that is #defined somewhere in a header.
        When the enum is then processed by the preprocessor, the symbol
        names on the right side will be replaced by their actual value.
        
        pattern is a regular expression that defines which values to pick from
        the names list. exclude may be a list of names that should not be considered,
        even when they match the pattern.
        """
        if exclude is None:
            exclude = []
        self.out.write("// %s\n"%pattern)
        self.out.write("enum {\n")
        for name in names:
            if re.match(pattern, name) and name not in exclude:
                self.out.write("  _WRAP_%s = %s,\n"%(name, name))
        self.out.write("};\n\n")


def xml2py(xmlFile, regExp=None):
    """Run xml2py.py and return the resulting lines.
    
    regExp is the value for the -r option.
    """
    cmd = 'xml2py.py "%s"'%(xmlFile)
    if regExp is not None:
        cmd += ' -r "%s"'%(regExp)
    print ("> %s"%cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    lines = proc.stdout.readlines()
    return lines

def xml2decls(xmlFile, prefix):
    """Helper function for createCppDefs.
    
    Extracts all #defines matching the given prefix from the xml file.
    IN the xml file, the #defines must appear as enums whose values have
    a prefix "_WRAP_<prefix>".
    Returns a string containing the lines. A line looks like this:
    
      LIBAVCODEC_VERSION_MAJOR = 52
    """
    decls = []
    lines = xml2py(xmlFile, "_WRAP_"+prefix+".*")
    for line in lines:
        if line.startswith("_WRAP_"):
            decls.append(line[6:])
    
    if len(decls)==0:
        print ("Warning: No declarations for prefix '%s' found."%prefix)
    
    return "".join(sorted(decls))

def createCppDefs(fileName, xmlFile):
    """Create the cppdefs.py file that contains all #defined values.
    """
    f = open(fileName, "wt")
    f.write(license)
    
    # Write the version info...
    f.write("\n# Versions this module is based on\n")
    for prefix in ["LIBAVCODEC_VERSION_", "LIBAVFORMAT_VERSION_", "LIBAVUTIL_VERSION_",
                   "LIBAVFILTER_VERSION_", "LIBSWSCALE_VERSION_"]:
        decls = xml2decls(xmlFile, prefix)
        f.write(decls+"\n")

    # A few special values
    f.write("AV_NOPTS_VALUE = 0x8000000000000000\n\n")
    for prefix in ["AV_", "MAX_"]:
        decls = xml2decls(xmlFile, prefix)
        f.write(decls+"\n")

    for comment,prefix in [("Error codes", "AVERR"),
                           ("CodecType enum values", "CODEC_TYPE_"),
                           ("Codec flags", "CODEC_FLAG_"),
                           ('Flags for the "flags" field in AVOutputFormat/AVInputFormat', "AVFMT_"),
                           ("Flags for url_fopen()", "URL_"),
                           ("av_seek_frame() flags", "AVSEEK_FLAG_"),
                           ("swscale flags", "SWS_")]:    
        f.write("# %s\n"%comment)
        decls = xml2decls(xmlFile, prefix)
        f.write(decls+"\n")

    f.close()

def create(includePath, generatedDir, cppdefsName, declsName, log):
    """Create all declarations.
    """
    if not os.path.exists(generatedDir):
        os.mkdir(generatedDir)

    # Generate the defs.h header file containing the converted #defines...
    # Values that were defined using #define wouldn't get parsed by gccml, so
    # we temporarily convert them into enums that have a prefix "_WRAP_" prepended.
    # The enums will appear in the xml file and from there we can create the values
    # again.
    defsName = os.path.join(generatedDir, "defs.h")
    print ("### Creating %s..."%defsName)
    f = open(defsName, "wt")
    dc = DefinesCollector(out=f, log=log)
    dc.createHeader(includePath)
    f.close()
    
    # Generate the ffmpeg.xml file containing all C declarations...
    ffmpegXmlName = os.path.join(generatedDir, "ffmpeg.xml") 
    print ("### Creating %s..."%ffmpegXmlName)
    cmd = "h2xml.py -I%s -o %s `pwd`/mainheader.h"%(includePath, ffmpegXmlName)
    print ("> %s"%cmd)
    os.system(cmd)
    
    # Generate the cppdefs.py file containing the #define values...
    print ("### Creating %s..."%cppdefsName)
    createCppDefs(cppdefsName, ffmpegXmlName)
    
    # Generate the decls file containing the ffmpeg struct definitions...
    print ("### Creating %s..."%declsName) 
    f = open(declsName, "wt")
    f.write(license)
    if sys.version_info[0]==2:
        f.write("\nfrom cppdefs import *\n")
    else:
        f.write("\nfrom .cppdefs import *\n")
    f.close()
    cmd = "xml2py.py %s -s AVFormatContext -s AVPicture -s SwsContext >> %s"%(ffmpegXmlName, declsName)
    print ("> %s"%cmd)
    os.system(cmd)

def logStats(generatedDir, log):
    """Log the byte size of the generated structs in decls.
    """
    sys.path.append(generatedDir)
    log.write('\nModule "decls" struct contents and sizes:\n')
    import decls
    for name in sorted(dir(decls)):
        obj = getattr(decls, name)
        try:
            isStruct = issubclass(obj, ctypes.Structure)
            size = ctypes.sizeof(obj)
        except:
            isStruct = False
            size = 0
        if isStruct:
            log.write("  sizeof(%s) = %s\n"%(name, size))

############################################################################

includePath = "/opt/local/include"
generatedDir = "generated"

cppdefsName = os.path.join(generatedDir, "cppdefs.py")
declsName = os.path.join(generatedDir, "decls.py")

if len(sys.argv)==2 and sys.argv[1]=="copy":
    # Copy
    targetDir = os.path.join("..", "..", "cgkit", "ffmpeg")
    print ("Copy %s -> %s"%(cppdefsName, targetDir))
    shutil.copy(cppdefsName, targetDir)
    print ("Copy %s -> %s"%(declsName, targetDir))
    shutil.copy(declsName, targetDir)
else:
    # Create    
    log = open(os.path.join(generatedDir, "log.txt"), "wt")
    create(includePath=includePath, generatedDir=generatedDir, cppdefsName=cppdefsName, declsName=declsName, log=log)
    logStats(generatedDir, log)
    log.close()
