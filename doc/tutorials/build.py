# Build tutorials

import sys, os, os.path, stat

# isNewer
def isNewer(file1, file2):
    """Check if file1 is newer than file2.

    Returns True if file1 is newer than file2 or if file2 doesn't exist.
    file1 must be an existing file.
    """
    if not os.path.exists(file2):
        return True
    return os.stat(file1)[stat.ST_MTIME]>os.stat(file2)[stat.ST_MTIME]

# build
def build(name, stylesheet="../default.css"):
    """Build a tutorial by converting RST into HTML."""
    n,ext = os.path.splitext(name)
    dest = n+".html"
    if isNewer(name, dest):
        cmd = "rst2html %s %s --stylesheet=%s"%(name, dest, stylesheet)
        print cmd
        os.system(cmd)

######################################################################

# Change to the directory where the script is located
# (so that the following commands uses the correct paths)
os.chdir(os.path.dirname(sys.argv[0]))

#build("index.txt", stylesheet="default.css")
build("first_steps/first_steps.txt")
build("materials/materials.txt")
build("animation/animation.txt")
build("renderman/renderman.txt")
build("custom_vars/custom_vars.txt")
build("ogre/ogre.txt")
build("baking/baking.txt")
build("code_examples/demo1.txt")
build("code_examples/demo2.txt")
build("code_examples/demo3.txt")
build("code_examples/shownormals.txt")
build("code_examples/spacedevicedemo.txt")
