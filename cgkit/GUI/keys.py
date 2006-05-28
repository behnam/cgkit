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

## \file keys.py
## Contains the Keys class.

import wx
import string

# Exceptions:
class InvalidKeyDescription(Exception):
    """Exception class."""
    pass

class KeyNotBound(Exception):
    """Exception class."""
    pass

# Keys
class Keys(object):
    """This class manages key strokes.

    Key bindings correspond to special key attributes. The attribute
    name is the name of the key and the value is a callable object
    that takes no arguments.

    Example:

    \code
    >>> keys = Keys()

    # Bind functions to keys...
    >>> keys.ctrl_c = onExit
    keys.shift_ctrl_tab = onFoo

    # Remove a key binding
    >>> del keys.ctrl_c
    
    \endcode
    """

    def __init__(self):

        # Command dictionary. The keys are the tuples that contain the
        # modifier flags and the key code. The value is a callable object.
        self._commands = {}
        
        # A dictionary that translates wx key codes into a string description
        # The dictionary is built from the WXK_xyz constants
        self._wxkeystrs = {}
        wxkeys = filter(lambda x: x[0:4]=="WXK_", dir(wx))
        for k in wxkeys:
            code = getattr(wx, k)
            self._wxkeystrs[code] = k[4:].capitalize()

        # The Window object that uses this key manager
        self._window = None


    def attach(self, window):
        self._window = window
        wx.EVT_KEY_DOWN(window, self._onKeyDown)
#        wx.EVT_KEY_UP(window, self._onKeyUp)
#        wx.EVT_CHAR(window, self._onChar)

    def detach(self):
        pass

    def findCommandKeys(self, func):
        """Search the key table for a command and return all associated keys.

        \param func (\c callable) The bound function
        \return A list of readable key strings.
        """

        res = []
        # Compare all commands...
        for key in self._commands.iterkeys():
            cmd = self._commands[key]
            if func==cmd:
                res.append(self._cmdkey2text(key))

        return res

    ######################################################################
    ## protected:

#    def __setitem__(self, name, value):
#        print "setitem"
#        key = self._str2cmdkey(name)
#        print "Setting",key,"to",value
#        self._commands[key] = value        

    def _onKeyDown(self, event):
        """Handle a KeyDown event.

        Note: This event handler is \b not called if the corresponding
        description text is present in the menu. In that case, the menu
        handles the events itself (a wx feature). But it seems this only
        works with English modifier names.
        """
        print "KeyDown",
        print "KeyCode:",event.GetKeyCode(),"RawKeyCode:",event.GetRawKeyCode()

        # Create the key tuple
        key = self._event2cmdkey(event)
        # Check if the key was bound
        if key in self._commands:
            # Call the bound function
            func = self._commands[key]
            func()
        else:
            event.Skip()
    
    def _onKeyUp(self, event):
#        print "KeyUp",
#        print "KeyCode:",event.GetKeyCode(),"RawKeyCode:",event.GetRawKeyCode()
        event.Skip()

    def __setattr__(self, name, value):
        if name=="":
            return
        # If the name starts with an underscore then it's not a key description
        if name[0]=="_":
            object.__setattr__(self, name, value)
            return

        # Bind key...

        # Create the key tuple
        key = self._str2cmdkey(name)
        # Remove an existing binding
        if self._commands.has_key(key):
            self.__delattr__(name)
        # Store the key binding
        self._commands[key] = value

        # Update menu items
        self._updateMenu(value)

    def __delattr__(self, name):
        # If the name starts with an underscore then it's not a key description
        if name[0]=="_":
            object.__delattr__(self, name)
            return

        # Create the key tuple
        key = self._str2cmdkey(name)
        # Check if a key binding exists
        if self._commands.has_key(key):
            func = self._commands[key]
            del self._commands[key]
            # Update menu items
            self._updateMenu(func)
        else:
            raise KeyNotBound, "Key '%s' is not bound to a function."%name


    def _updateMenu(self, func):
        """Update all menu items that are bound to func."""
        # Check if any menu items have to be updated
        menu = getattr(self._window, "menu", None)
        if menu==None:
            return
        nodes = menu.findCommandNodes(func)
        for n in nodes:
            n.update()        
        

    def _event2cmdkey(self, event):
        """Convert a key event into a tuple which can be used as key."""
        return (bool(event.ShiftDown()), bool(event.ControlDown()),
                bool(event.AltDown()), bool(event.MetaDown()),
                event.GetKeyCode())

    def _str2cmdkey(self, s):
        """Convert a key description string into the key tuple."""

        f = s.upper().split("_")

        # Check if the modifiers are correct
        for m in f[:-1]:
            if m not in ["SHIFT", "CTRL", "ALT", "META"]:
                raise InvalidKeyDescription, "Key '%s' contains invalid modifiers."%s

        # Convert the last argument into a key code
        skey = f[-1]
        if len(skey)==1:
            key = ord(skey)
        else:
            key = getattr(wx, "WXK_%s"%skey, None)
            if key==None:
                raise InvalidKeyDescription, "Key '%s' does not exist."%s
        
        return ("SHIFT" in f, "CTRL" in f, "ALT" in f, "META" in f, key)

    def _cmdkey2text(self, key):
        shift, ctrl, alt, meta, key = key
        mods = []
        if shift:
            mods.append("Shift")
#            mods.append("Umschalt")
        if ctrl:
            mods.append("Ctrl")
#            mods.append("Strg")
        if alt:
            mods.append("Alt")
        if meta:
            mods.append("Meta")

        ks = self._wxkeystrs.get(key, None)
        if ks==None:
            ks=chr(key)
        mods.append(ks)
            
        return string.join(mods, "+")
        
            
        
    
        
