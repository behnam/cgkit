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
# $Id: glslangtokenize.py,v 1.1 2006/03/19 20:47:33 mbaas Exp $

"""OpenGL Shading Language Tokenizer."""

import re

WHITESPACE = 0
NAME       = 1
NUMBER     = 2
STRING     = 3
NEWLINE    = 4
OPERATOR   = 5
CHARACTER  = 6
TYPE       = 7
QUALIFIER  = 8

# tokenize
def tokenize(readline, tokeater):
    """Reads a Shading Language input stream and creates tokens.

    The first parameter, readline, must be a callable object which
    provides the same interface as the readline() method of built-in
    file objects. Each call to the function should return one line of
    input as a string.

    The second parameter, tokeneater, must also be a callable object.
    It is called with six parameters: the token type, the token
    string, a tuple (srow, scol) specifying the row and column where
    the token begins in the source, a tuple (erow, ecol) giving the
    ending position of the token, the line on which the token was
    found and the filename of the current file.

    By default the filename argument is an empty string. It will only
    be the actual filename if you provide a preprocessed file stream
    as input (so you should first run cpp on any shader). The
    tokenizer actually expects preprocessed data as it doesn't handle
    comments.
    """

    types = ["void", "bool", "float", "int", "bvec2", "bvec3", "bvec4",
             "ivec2", "ivec3", "ivec4", "vec2", "vec3", "vec4",
             "mat2", "mat3", "mat4", "struct",
             "sampler1D", "sampler2D", "sampler3D", "samplerCube",
             "sampler1DShadow", "sampler2DShadow"]
    
    qualifiers = ["const", "attribute", "uniform", "varying", "in", "out", "inout"]
                      
    regs =  ( (WHITESPACE, re.compile(r"[ \t]+")),
              (NAME,       re.compile(r"[A-Za-z_][A-Za-z_0-9]*")),
              (NUMBER,     re.compile(r"[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?")),
              (STRING,     re.compile(r"\"[^\"]*\"")),
              (OPERATOR,   re.compile(r"\(|\)|\[|\]|\+\+|\-\-|\+|-|!|\.|~|\*|/|\^|%|&|\||<<|>>|<|>|<=|>=|==|!=|&&|\|\||\^\^|\?:|=|\+=|-=|\*=|/=|%=|<<=|>>=|&=|\^=|\|=")),
              (NEWLINE,    re.compile(r"\n"))
            )

    linenr   = 0
    filename = ""
    while 1:
        # Read next line
        line = readline()
        # No more lines? then finish
        if line=="":
            break

        linenr+=1
        # Base for starting column...
        scolbase = 0

        # Process preprocessor lines...
        if line[0]=="#":
            try:
                f = line.strip().split(" ")
                linenr = int(f[1])-1
                filename = f[2][1:-1]
            except:
                pass
            continue

        s = line

        # Create tokens...
        while s!="":
            unmatched=1
            # Check all regular expressions...
            for r in regs:
                m=r[1].match(s)
                # Does it match? then the token is found
                if m!=None:
                    scol = m.start()
                    ecol = m.end()
                    tok = s[scol:ecol]
                    s   = s[ecol:]
                    typ = r[0]
                    if typ==NAME:
                        if tok in types:
                            typ = TYPE
                        elif tok in qualifiers:
                            typ = QUALIFIER
                    tokeater(typ, tok, (linenr, scolbase+scol), (linenr, scolbase+ecol), line, filename)
                    scolbase += ecol
                    unmatched=0
                    continue

            # No match? then report a single character...
            if unmatched:
                tok = s[0]
                tokeater(CHARACTER, tok, (linenr, scolbase), (linenr, scolbase+1), line, filename)
                s = s[1:]
                scolbase += 1
            
            

def _tokeater(type, s, start, end, line, filename):
    if type==WHITESPACE or type==NEWLINE:
        return
    types = { 0:"WHITESPACE", 1:"NAME", 2:"NUMBER", 3:"STRING", 4:"NEWLINE",
              5:"OPERATOR", 6:"CHARACTER", 7:"TYPE", 8:"QUALIFIER" }
    print "%s: %-10s: %-20s %s %s"%(filename, types[type], s, start, end)

######################################################################

if __name__=="__main__":

    f=open("test.shader")
    tokenize(f.readline, _tokeater)
    
