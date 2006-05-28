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
# $Id: toolbars.py,v 1.1.1.1 2004/12/12 14:31:41 mbaas Exp $

import os.path, string
import wx
import panelicons

# ToolBarPalette
class ToolBarPalette(object):
    """Toolbar palette.

    This class manages a wx.Notebook that contains an arbitrary number
    of ToolBars.

    \see ToolBar
    """
    def __init__(self, parent, IDmanager):
        
        self._wx = wx.Notebook(parent, -1, style=wx.CLIP_CHILDREN)
        self.sizer = wx.NotebookSizer(self._wx)

        self._toolbars = []

        self._id_manager = IDmanager

        self.addToolBar("Main")
        self.addToolBar("Test")

        

    def __iter__(self):
        return iter(self._toolbars)

    def __getattr__(self, name):
        return self.findToolBar(name)

        
    def addToolBar(self, title):
        tb = ToolBar(self, title, self._id_manager)
        self._wx.AddPage(tb._panel, title)

        self._toolbars.append(tb)
        
#        tb.add("Open.png", None)
#        tb.add("Close", None)


    # findToolBar
    def findToolBar(self, name):
        """Returns the toolbar with the given name.

        \param name (\c str) Toolbar name
        \return Toolbar (\c ToolBar) or None.
        """
        for tb in self._toolbars:
            if tb.name==name:
                return tb
        return None



        
    ######################################################################
    ## protected:

    # "wx" property...
    
    def _getWx(self):
        """Return the encapsulated wx widget.

        This method is used for retrieving the \a wx property.

        \return wxPython object.
        """
        return self._wx

    wx = property(_getWx, None, None, "Encapsulated wx widget")
        

# ToolBar
class ToolBar:
    """Encapuslates a wx ToolBar.

    \see ToolBarPalette
    """
    
    def __init__(self, parent, name, IDmanager):
        """Constructor.
        
        \param parent (\c ToolBarPalette) Parent tool bar palette 
        """
        self._panel = wx.Panel(parent.wx, -1)
        self._wx = wx.ToolBar(self._panel, -1)
        self._wx.SetName(name)
        self._wx.SetToolBitmapSize(wx.Size(32,32))

        self._sizer = wx.BoxSizer(wx.VERTICAL)
        # Add 8 pixels at the bottom (why is it too small without?!?)
        self._sizer.Add(self._wx, 0, wx.EXPAND | wx.BOTTOM, 8)
        self._panel.SetAutoLayout(True)
        self._panel.SetSizer(self._sizer)

        self._id_manager = IDmanager
        # Lookup table
        self._tool_id_lut = {}

    def __str__(self):
        return "<ToolBar '%s'>"%self._wx.GetName()

    def add(self, bitmapdef, command=None):
        """Add a new tool.
        """

        bitmap = self._def2bitmap(bitmapdef)
        id = self._id_manager.allocID()
        self._wx.AddSimpleTool(id, bitmap, "Short", "A help string.")

        self._tool_id_lut[id] = command
        wx.EVT_MENU(self._wx, id, self._onToolSelection)
        
        self._wx.Realize()


    ######################################################################
    ## protected:

    def _onToolSelection(self, event):
        id = event.GetId()
        if id not in self._tool_id_lut:
            return

        cmd = self._tool_id_lut[id]
        if cmd!=None:
            cmd()

    def _def2bitmap(self, bitmapdef):
        """Convert a bitmap definition into a bitmap.

        \return wx Bitmap
        """
        # Is bitmapdef already a bitmap?
        if isinstance(bitmapdef, wx.BitmapPtr):
            return bitmapdef

        if self._isFilename(bitmapdef):
            bmp = wx.Bitmap(bitmapdef)
            if bmp.Ok():
                return bmp
            else:
                bitmapdef = os.path.basename(bitmapdef)

        bmp = wx.EmptyBitmap(32,32)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)

        dc.SetPen(wx.BLACK_PEN)
        dc.SetBackground(wx.GREY_BRUSH)
        font = wx.Font(5, wx.SWISS, wx.NORMAL, wx.NORMAL)
        dc.SetFont(font)
        dc.Clear()
        w,h = dc.GetTextExtent(bitmapdef)
        x = (32-w)/2
        y = 32-h-3
        dc.DrawText(bitmapdef,x,y)
        return bmp

    def _isFilename(self, name):
        """Check if a string contains a filename.

        The check is done on the suffix. If there is one that has
        3 or 4 ascii characters then the function returns True.
        """
        n,ext = os.path.splitext(name)
        if ext=="" or len(ext)<4 or len(ext)>5:
            return False
        for c in ext[1:]:
            if c not in string.ascii_letters:
                return False
        return True


    # "wx" property...
    
    def _getWx(self):
        """Return the encapsulated wx widget.

        This method is used for retrieving the \a wx property.

        \return wxPython object.
        """
        return self._wx

    wx = property(_getWx, None, None, "Encapsulated wx widget")

    # "name" property...
    
    def _getName(self):
        """Return the node name.

        This method is used for retrieving the \a name property.

        \return Name (\c str)
        """
        return self._wx.GetName()
        
    name = property(_getName, None, None, "Name")
        

