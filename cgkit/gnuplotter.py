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
# $Id: gnuplotter.py,v 1.3 2005/03/31 17:11:56 mbaas Exp $

## \file gnuplotter.py
## Contains the GnuPlotter class.

import sys
import component
import eventmanager, events
from scene import getScene
from slots import *
from cgtypes import *
import _core
try:
    import Gnuplot
    gnuplot_installed = True
except:
    gnuplot_installed = False


class _PlotDesc:
    def __init__(self, slot, title):
        self.slot = slot
        self.title = title
        self.data = []

# GnuPlotter
class GnuPlotter(component.Component):
    """Graph plotter using gnuplot.
    
    """

    def __init__(self,
                 name = "GnuPlotter",
                 title = None,
                 xlabel = None,
                 ylabel = None,
                 xrange = None,
                 yrange = None,
                 inputs = 1,
                 plottitles = [],
                 starttime = 0.0,
                 endtime = 99999.0,
                 enabled = True,
                 auto_insert = True):
        """Constructor.
        """
        global gnuplot_installed
        
        component.Component.__init__(self, name, auto_insert)

        self.enabled = enabled
        self.inputs = inputs
        self.plot_data = []
        self.starttime = starttime
        self.endtime = endtime

        for i in range(inputs):
            s = DoubleSlot()
            exec "self.input%d_slot = s"%(i+1)
            if i<len(plottitles):
                t = plottitles[i]
            else:
                t = None
            pd = _PlotDesc(slot=s, title=t)
            self.plot_data.append(pd)

        if not enabled:
            return

        if not gnuplot_installed:
            print >>sys.stderr, "Warning: PyGnuplot is not installed"
            return

        self.gp = Gnuplot.Gnuplot()
        self.gp('set data style lines')
        self.gp("set grid")
        self.gp("set xzeroaxis")
        if title!=None:
            self.gp.title(title)
        if xlabel!=None:
            self.gp.xlabel(xlabel)
        if ylabel!=None:
            self.gp.ylabel(ylabel)
        if yrange!=None:
            self.gp.set_range("yrange",yrange)
#            self.gp("set yrange [%f:%f]"%tuple(yrange))
        if xrange!=None:
            self.gp.set_range("xrange",xrange)

        self._delay = 0

        eventmanager.eventManager().connect(events.STEP_FRAME, self)
        
    def onStepFrame(self):
        if not self.enabled:
            return
        
        t = getScene().timer().time
        if t<self.starttime or t>self.endtime:
            return

        for pd in self.plot_data:
            pd.data.append((t, pd.slot.getValue()))
        
        if self._delay==0:
            a = []
            for pd in self.plot_data:
                data = pd.data
                # There seems to be a bug in Gnuplot.py 1.7 that prevents
                # data arrays with only one item to be displayed. So the
                # following is a workaround (the point is just duplicated).
                if len(data)==1:
                    data = 2*data
                data = Gnuplot.Data(data, title=pd.title)
                a.append(data)
            self.gp.plot(*a)
            self._delay = 0
        else:
            self._delay -= 1
        

