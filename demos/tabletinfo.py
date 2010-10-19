# Print tablet infos.
# Just run this directly (without the viewer tool).

import cgkit.wintab
from cgkit.wintab import *

# axisInfoStr
def axisInfoStr(axis):
    """Return a string containing info about an axis.
    """
    units = { TU_NONE : "None",
              TU_INCHES : "inch",
              TU_CENTIMETERS : "cm",
              TU_CIRCLE : "circle" }
    if axis is None:
        return "no info available"
    
    axmin, axmax, unit, resolution = axis
    if unit==TU_NONE:
        return "%d - %d (no units)"%(axmin, axmax)
    else:
        resolution = float(resolution)/0x10000
        unitstr = units.get(unit,"bla")
        return "%d - %d (%s units = 1 %s)"%(axmin, axmax, resolution, unitstr)

# hexStr
def hexStr(v):
    if v is None:
        return "None"
    else:
        return hex(v)

# hardwareCapStr
def hardwareCapStr(cap):
    if cap is None:
        return "None"

    cl = []
    if cap & HWC_INTEGRATED:
        cl += ["Integrated"]
    if cap & HWC_TOUCH:
        cl += ["Touch"]
    if cap & HWC_HARDPROX:
        cl += ["Hardprox"]
    if cap & HWC_PHYSID_CURSORS:
        cl += ["PhysID-Cursors"]

    if cl==[]:
        return "<none>"
    else:
        return ", ".join(cl)

# packetDataStr
def packetDataStr(data):
    if data is None:
        return "None"

    cl = []
    if data & PK_CONTEXT:
        cl += ["Ctx"]
    if data & PK_STATUS:
        cl += ["Sta"]
    if data & PK_TIME:
        cl += ["Time"]
    if data & PK_CHANGED:
        cl += ["Chg"]
    if data & PK_SERIAL_NUMBER:
        cl += ["Srl"]
    if data & PK_CURSOR:
        cl += ["Csr"]
    if data & PK_BUTTONS:
        cl += ["Btn"]
    if data & PK_X:
        cl += ["X"]
    if data & PK_Y:
        cl += ["Y"]
    if data & PK_Z:
        cl += ["Z"]
    if data & PK_NORMAL_PRESSURE:
        cl += ["NP"]
    if data & PK_TANGENT_PRESSURE:
        cl += ["TP"]
    if data & PK_ORIENTATION:
        cl += ["Ort"]
    if data & PK_ROTATION:
        cl += ["Rot"]

    if cl==[]:
        return "<none>"
    else:
        return ", ".join(cl)


# cursorCapabilitiesStr
def cursorCapabilitiesStr(cap):
    if cap is None:
        return "None"
    
    cl = []
    if cap & CRC_MULTIMODE:
        cl += ["Multimode"]
    if cap & CRC_AGGREGATE:
        cl += ["Aggregate"]
    if cap & CRC_INVERT:
        cl += ["Invert"]
    if cl==[]:
        return "<none>"
    else:
        return ", ".join(cl)

######################################################################

# Interface info
info = cgkit.wintab.info(WTI_INTERFACE)
ndevices = info["NDEVICES"]
ncursors = info["NCURSORS"]
ncontexts = info["NCONTEXTS"]
nextensions = info["NEXTENSIONS"]
specversion = info["SPECVERSION"]
implversion = info["IMPLVERSION"]
print 'Hardware identification string   : "%s"'%info["WINTABID"]
print "Specification version number     : %d.%d"%(specversion>>8, specversion&0xff)
print "Implementation version number    : %d.%d"%(implversion>>8, implversion&0xff)
print "Number of devices supported      :",ndevices
print "Number of cursor types supported :",ncursors
print "Number of contexts supported     :",ncontexts
print "Context options supported        :",hexStr(info["CTXOPTIONS"])
print "Size of the save information     :",info["CTXSAVESIZE"]
print "Number of extension data items   :",nextensions
print "Number of manager handles supp.  :",info["NMANAGERS"]

# Devices
for i in range(ndevices):
    print ""
    print 30*"-","Device",i,30*"-"
    info = cgkit.wintab.info(WTI_DEVICES+i)
    print 'Device name                 : "%s"'%info["NAME"]
    print "Hardware/driver capabil.    :",hardwareCapStr(info["HARDWARE"])
    print "Number of supported cursors :",info["NCSRTYPES"]
    print "First cursor                :",info["FIRSTCSR"]
    print "Maximum packet report rate  :",info["PKTRATE"],"Hz"
    print "Available packet data       :",packetDataStr(info["PKTDATA"])
    print "Relative only items         :",packetDataStr(info["PKTMODE"])
    print "Cursor dependent data       :",packetDataStr(info["CSRDATA"])
    print "Margin (x/y/z)              :",info["XMARGIN"],"/",info["YMARGIN"], "/",info["ZMARGIN"]
    print "X range                     :",axisInfoStr(info["X"])
    print "Y range                     :",axisInfoStr(info["Y"])
    print "Z range                     :",axisInfoStr(info["Z"])
    print "Normal pressure range       :",axisInfoStr(info["NPRESSURE"])
    print "Tangent pressure range      :",axisInfoStr(info["TPRESSURE"])
    res = info["ORIENTATION"]
    if res==None:
        az,al,t = None,None,None
    else:
        az,al,t = res
    print "Orientation azimuth range   :",axisInfoStr(az)
    print "Orientation altitude range  :",axisInfoStr(al)
    print "Orientation twist range     :",axisInfoStr(t)
    res = info["ROTATION"]
    if res==None:
        p,r,y = None,None,None
    else:
        p,r,y = res
    print "Rotation pitch range        :",axisInfoStr(p)
    print "Rotation roll range         :",axisInfoStr(r)
    print "Rotation yaw range          :",axisInfoStr(y)
    print 'Plug and Play ID            : "%s"'%info["PNPID"]

# Cursors
for i in range(ncursors):
    print ""
    print 30*"-","Cursor",i,30*"-"
    info = cgkit.wintab.info(WTI_CURSORS+i)
    print 'Cursor name                 : "%s"'%info["NAME"]
    print "Active                      :",info["ACTIVE"]
    print "Available packet data       :",packetDataStr(info["PKTDATA"])
    print "Number of buttons           :",info["BUTTONS"]
    print "Number of button bits       :",info["BUTTONBITS"]
    print "Button names                :",info["BTNNAMES"]
    print "Button map                  :",info["BUTTONMAP"]
    print "Button action codes         :",info["SYSBTNMAP"]
    print "Normal pressure button      :",info["NPBUTTON"]
    print "Button marks for normal pr. :",info["NPBTNMARKS"]
#    print "Normal response curve       :",info["NPRESPONSE"]
    print "Tangential pressure button  :",info["TPBUTTON"]
    print "Button marks for tangent pr.:",info["TPBTNMARKS"]
#    print "Tangential response curve   :",info["TPRESPONSE"]
    print "Physical cursor identifier  :",info["PHYSID"]
    print "Cursor mode number          :",info["MODE"]
    print "Minimum packet data         :",info["MINPKTDATA"]
    print "Minimum number of buttons   :",info["MINBUTTONS"]
    print "Cursor capabilities         :",cursorCapabilitiesStr(info["CAPABILITIES"])

# Extensions
for i in range(nextensions):
    print ""
    print 30*"-","Extension",i,30*"-"
    info = cgkit.wintab.info(WTI_EXTENSIONS+i)
    print 'Extension name              : "%s"'%info["NAME"]
    print "Identifier                  :",info["TAG"]
    print "Mask                        :",hexStr(info["MASK"])
    print "Size (abs, rel)             :",info["SIZE"]
    print "Axis descriptions           :",info["AXES"]
    print "Default data                :",info["DEFAULT"]
    print "Default context data        :",info["DEFCONTEXT"]
    print "Default system context data :",info["DEFSYSCTX"]
    print "Cursor specific data        :",info["CURSORS"]

