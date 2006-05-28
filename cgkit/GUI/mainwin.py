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
# $Id: mainwin.py,v 1.2 2006/01/27 07:52:40 mbaas Exp $

import wx
import window
#from cgkit import getApp
from menu import *
from panels import Panels, LayoutNode, PanelNode, PanelWidget, HORIZONTAL, VERTICAL
from toolbars import ToolBarPalette

# MainWin
class MainWindow(window.Window):
    def __init__(self):
        window.Window.__init__(self)

        # Create menu
        file = Menu("&File", name="file", items=
                    [("&New"),
                     ("&Open..."),
                     ("&Save"),
                     ("Save &as...", None),
                     ("&Close"),
                     MenuItem("---",name="sep1"),
                     ("&Exit", None)
                     ])

        self.menu = Menu(items=[file])


        # ToolBar palette
        self.toolbars = ToolBarPalette(self.wx, self._menu_id_manager)

        # Create panels
        self.panels = Panels(self.wx)
        self.panels.layout = PanelNode(name="Dummy")


        self.mainlayout = wx.BoxSizer(wx.VERTICAL)
        self.mainlayout.AddSizer(self.toolbars.sizer, 0, wx.EXPAND, 0)
        self.mainlayout.Add(self.panels.wx, 1, wx.EXPAND, 0)
        self.wx.SetSizer(self.mainlayout)


#        views = LayoutNode(splittertype=VERTICAL, name="splitter1")

#        self.btn = wx.Button(parent, -1, "Button", wx.Point(0,0))
#        front = PanelNode(name="front", activatable=True,
#                          widget=PanelWidget(wx=self.btn))

#        dict = globals()
#        dict["app"]=getApp()
#        self.shell = wx.py.shell.Shell(parent, -1, locals=dict)
#        shell = PanelNode(name="shell", widget=PanelWidget(wx=self.shell))
        
#        views.setChildren((front, shell))
#        self.panels.layout = views
#        front.makeCurrent()

#        self.panels.updateLayout()

        if "mainwin.geometry" in getApp().prefs:
            x,y,w,h = getApp().prefs["mainwin.geometry"]
            print "set",x,y,w,h
            self.SetDimensions(x,y,w,h)
            if getApp().prefs["mainwin.maximized"]:
                self.Maximize(True)
           
        wx.EVT_SIZE(self, self.onResize)
        wx.EVT_MOVE(self, self.onMove)
        return

    def onMove(self, event):
        app = getApp()
        if "mainwin.geometry" in app.prefs:
            x,y,w,h = app.prefs["mainwin.geometry"]
        else:
            w,h = self.GetSizeTuple()
        x,y = self.GetPosition()
        if not self.IsMaximized():
            app.prefs["mainwin.geometry"] = [x,y,w,h]

    def onResize(self, event):
        app = getApp()
        if "mainwin.geometry" in app.prefs:
            x,y,w,h = app.prefs["mainwin.geometry"]
        else:
            x,y = self.GetPositionTuple()
        w,h = self.GetSize()
        if self.IsMaximized():
            app.prefs["mainwin.maximized"] = True
        else:
            app.prefs["mainwin.maximized"] = False
            app.prefs["mainwin.geometry"] = [x,y,w,h]
        event.Skip()

