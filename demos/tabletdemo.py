# Tablet demo
# This has to be run using the viewer tool.

from cgkit.wintab.constants import *

TargetCamera(
    pos = (1, -1, 2),
    target = (1,0.7,0)
)

pen = CCylinder(
    name = "Pen",
    radius = 0.03,
    length = 0.8,
    pivot = (0,0,-0.4),
    material = GLMaterial( diffuse = (0.3,0.3,0.7) )
)

Plane(
    name = "Tablet",
    lx = 2,
    ly = 1.5,
    pos = (1, 0.75, -0.01),
    material = GLMaterial( diffuse = (1.0, 0.97, 0.9) )
)

def onTablet(e):
    f = 0.0001
    p = vec3(f*e.x, f*e.y, 0.05)
    pen.pos = p

    if e.pktdata & PK_ORIENTATION:
        az = e.orient_azimuth/10.0
        alt = e.orient_altitude/10.0
        R1 = mat3().rotation(radians(90-alt), vec3(-1,0,0))
        R2 = mat3().rotation(radians(az), vec3(0,0,-1))
        pen.rot = R2*R1

    if e.buttons!=0:
        p.z = 0
        drawMarker(p, size=0.03*e.normalpressure/1024.0, color=(0,0,0))

def onKey(e):
    if e.key==" ":
        drawClear()

eventmanager.connect(TABLET, onTablet)
eventmanager.connect(KEY_PRESS, onKey)
