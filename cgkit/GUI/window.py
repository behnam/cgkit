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

import wx
import idmanager
import keys

class Window(object):
    """Frame class.

    Attributes:

    - wx
    - keys
    - menu
    """


    def __init__(self,
                 parent = None,
                 id = -1,
                 title = 'Title',
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style = wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN):
        """Create a Frame instance.
        """

        # Create the actual window (a wx Frame)
        self._wx = wx.Frame(parent, id, title, pos, size, style)

        self._keys = keys.Keys()
        self._keys.attach(self)

        # Set up the wx main menu bar
        self._menu_id_manager = idmanager.IDManager(10)
        menubar = wx.MenuBar()
        self._wx.SetMenuBar(menubar)
        self._menu = None

        self.CreateStatusBar()

        wx.EVT_LEFT_DOWN(self, self.onLeftDown)
        wx.EVT_LEFT_UP(self, self.onLeftUp)
        wx.EVT_MIDDLE_DOWN(self, self.onMiddleDown)
        wx.EVT_MIDDLE_UP(self, self.onMiddleUp)
        wx.EVT_RIGHT_DOWN(self, self.onRightDown)
        wx.EVT_RIGHT_UP(self, self.onRightUp)

    def popupMenu(self, menu, pos):
        """Open a menu as a popup menu at the given position.

        \param menu (\c Menu)  Menu tree
        \param pos (\c 2-sequence) Position of the popup menu
        """
        menu._attach(self._menu_id_manager, self, None)
        x,y = pos
        self.PopupMenuXY(menu.wx, x, y)
        menu._detach()

    def onLeftDown(self, event):
        event.Skip()

    def onLeftUp(self, event):
        event.Skip()

    def onMiddleDown(self, event):
        event.Skip()

    def onMiddleUp(self, event):
        event.Skip()

    def onRightDown(self, event):
        event.Skip()

    def onRightUp(self, event):
        event.Skip()


    ######################################################################
    ## protected:

    def __getattr__(self, name):
        """Forward attribute requests to the wxFrame object."""
        
        val = getattr(self._wx, name, None)
        if val==None:
            raise AttributeError, "'Window' object has no attribute '%s'."%name
        else:
            return val

        
    # "wx" property...
    
    def _getWx(self):
        """Return the corresponding wxFrame object.

        This method is used for retrieving the \a wx property.

        \return Frame (\c wxFrame).
        """
        return self._wx

    wx = property(_getWx, None, None, "wxFrame object")


    # "keys" property...
    
    def _getKeys(self):
        """Return the key manager.

        This method is used for retrieving the \a keys property.

        \return Key manager (\c Keys).
        """
        return self._keys

    keys = property(_getKeys, None, None, "Key manager")


    # "menu" property...
    
    def _getMenu(self):
        """Return the menu tree.

        This method is used for retrieving the \a menu property.

        \return Root menu node (\c MenuNode).
        """
        return self._menu

    def _setMenu(self, menu):
        """Set a menu.

        This method is used for setting the \a menu property.
        """

        if self._menu!=None:
            self._menu._detach()

        self._menu = menu
        self._menu._attach(self._menu_id_manager, self, self._wx.GetMenuBar())


    menu = property(_getMenu, _setMenu, None, "Menu tree")


