# Tablet test

import sys, os, os.path
import pygame
from pygame.locals import *

import cgkit.wintab
from cgkit.wintab.constants import *

ctx = cgkit.wintab.Context()

ctx.name = "TestApp"
ctx.options |= CXO_MESSAGES | CXO_CSRMESSAGES

print ('Name     : "%s"'%ctx.name)
print ("Options  : %s"%ctx.options)
print ("Status   : %s"%ctx.status)
print ("Locks    : %s"%ctx.locks)
print ("MsgBase  : %s"%ctx.msgbase)
print ("Device   : %s"%ctx.device)
print ("PktRate  : %s"%ctx.pktrate)
print ("PktData  : %s"%ctx.pktdata)
print ("PktMode  : %s"%ctx.pktmode)
print ("MoveMask : %s"%ctx.movemask)
print ("BtnDnMask: %s"%ctx.btndnmask)
print ("BtnUpMask: %s"%ctx.btnupmask)
print ("InOrgX   : %s"%ctx.inorgx)
print ("InOrgY   : %s"%ctx.inorgy)
print ("InOrgZ   : %s"%ctx.inorgz)
print ("InExtX   : %s"%ctx.inextx)
print ("InExtY   : %s"%ctx.inexty)
print ("InExtZ   : %s"%ctx.inextz)
print ("OutOrgX  : %s"%ctx.outorgx)
print ("OutOrgY  : %s"%ctx.outorgy)
print ("OutOrgZ  : %s"%ctx.outorgz)
print ("OutExtX  : %s"%ctx.outextx)
print ("OutExtY  : %s"%ctx.outexty)
print ("OutExtZ  : %s"%ctx.outextz)
print ("SensX    : %s"%ctx.sensx)
print ("SensY    : %s"%ctx.sensy)
print ("SensZ    : %s"%ctx.sensz)
print ("SysMode  : %s"%ctx.sysmode)
print ("SysOrgX  : %s"%ctx.sysorgx)
print ("SysOrgY  : %s"%ctx.sysorgy)
print ("SysExtX  : %s"%ctx.sysextx)
print ("SysExtY  : %s"%ctx.sysexty)
print ("SysSensX : %s"%ctx.syssensx)
print ("SysSensY : %s"%ctx.syssensy)

######################################################################

def main():
    global ctx
    
    # Initialize pygame
    passed, failed = pygame.init()

    pygame.display.set_caption("Wintab test")
    srf = pygame.display.set_mode((320,240))

    info = pygame.display.get_wm_info()
    hwnd = info["window"]
    print ("HWND: %s"%hwnd)

    ctx.pktdata = PK_X | PK_Y | PK_CURSOR | PK_BUTTONS | PK_NORMAL_PRESSURE | PK_STATUS #| PK_ORIENTATION

    ctx.pktrate = 20
    ctx.open(hwnd, True)

    print ("Queue size: %s"%ctx.queuesize)
#    print ctx.save()

    pygame.event.set_allowed(SYSWMEVENT)
#    pygame.event.set_blocked(MOUSEMOTION)

    clk = pygame.time.Clock()
    running = True
    while running:
        
        events = pygame.event.get()
        if len(events)>0:
#            print len(events), "events",events
            for e in events:
                if e.type==SYSWMEVENT and e.msg>=ctx.msgbase:
                    if e.msg==ctx.id_packet:
                        p = ctx.packet(e.wparam)
#                        print p
#                        print p.x, p.y, p.z
                    elif e.msg==ctx.id_csrchange:
                        print "Cursor change"
                    elif e.msg==ctx.id_ctxopen:
                        print "Context opened - Status flags:",hex(e.lparam)
                    elif e.msg==ctx.id_ctxclose:
                        print "Context closed - Status flags:",hex(e.lparam)
                    elif e.msg==ctx.id_ctxupdate:
                        print "Context updated - Status flags:",hex(e.lparam)
                    elif e.msg==ctx.id_ctxoverlap:
                        print "Context overlap - Status flags:",hex(e.lparam)
                    elif e.msg==ctx.id_proximity:
                        print "Proximity event - lParam:",hex(e.lparam)
                    elif e.msg==ctx.id_infochange:
                        print "Info change event - lParam:",hex(e.lparam)
                    else:
                        print "EVT - ID:%d  wParam:%d lParam:%d"%(e.msg,e.wparam,e.lparam)

#        pkts = ctx.packetsGet(10)
#        if len(pkts)>0:
#            print len(pkts),"packets"
#            for p in pkts:
#                print " ",p
                
        for e in events:
            if e.type==QUIT:
                running = False
            if e.type==KEYDOWN:
                if e.unicode=="c":
                    print "Config:",
                    print ctx.config()

        clk.tick(30)

main()
