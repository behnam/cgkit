# Test slots

import unittest
from cgkit import _core
from cgkit.all import *

class TestSlot(unittest.TestCase):
    
    def testConstructor(self):

        # Standard constructor
        as = _core.DoubleSlot()
        self.assertEqual(as.getValue(), 0)
        self.assertEqual(as.getController(), None)

        as = _core.IntSlot()
        self.assertEqual(as.getValue(), 0)

        as = _core.Vec3Slot()
        self.assertEqual(as.getValue(), vec3(0))

        as = _core.StrSlot()
        self.assertEqual(as.getValue(), "")        

        # Constructor (initialvalue, flags)
        as = _core.DoubleSlot(12.7, 0)
        self.assertEqual(as.getValue(), 12.7)
        self.assertEqual(as.getController(), None)

        as = _core.IntSlot(5, 0)
        self.assertEqual(as.getValue(), 5)

        as = _core.Vec3Slot(vec3(1,2,3), 0)
        self.assertEqual(as.getValue(), vec3(1,2,3))

        as = _core.StrSlot("spam", 0)
        self.assertEqual(as.getValue(), "spam")

    def testNoneConnection(self):
        """Check that connecting to None doesn't crash."""
        as = DoubleSlot()
        as.connect(None)

    def testNoneDisconnection(self):
        """Check that disconnecting from None doesn't crash."""
        as = DoubleSlot()
        as.disconnect(None)

    def testDisconnect(self):
        """Test the disconnect method."""
        ctrl = DoubleSlot(12)
        as = DoubleSlot(5)

        # Check that disconnecing a non-existent connection raises an error
        self.assertRaises(ValueError, ctrl.disconnect, as)

        # Connect and disconnect and check that the controller doesn't
        # influence as anymore
        ctrl.connect(as)
        self.assertEqual(as.getValue(), 12.0)
        ctrl.disconnect(as)
        ctrl.setValue(4)
        self.assertEqual(ctrl.getValue(), 4.0)
        self.assertEqual(as.getValue(), 12.0)


##class TestArraySlot(unittest.TestCase):
    
##    def testConstructor(self):

##        # Standard constructor (check if items are 0)
##        as = _core.IntArraySlot()
##        as.resize(100)
##        self.assertEqual(list(as), 100*[0])

##        as = _core.DoubleArraySlot()
##        as.resize(100)
##        self.assertEqual(list(as), 100*[0.0])
        

class TestProceduralSlot(unittest.TestCase):

    def doubleProcedure(self):
        """Dummy procedure to compute a slot value."""
        return 42.0

    def testGetValue(self):
        """Check that the procedural value is actually obtained."""
        ps = ProceduralDoubleSlot(self.doubleProcedure)
        self.assertEqual(ps.getValue(), 42.0)
    
    def testSetValue(self):
        """Check that setting a value has no effect."""
        ps = ProceduralDoubleSlot(self.doubleProcedure)
        ps.setValue(15.5)
        self.assertEqual(ps.getValue(), 42.0)

    def testInConnection(self):
        """Check that a procedural slot cannot take controllers."""
        ctrl = DoubleSlot(15.0)
        ps = ProceduralDoubleSlot(self.doubleProcedure)

        # The following should not throw an exception
        ps.setController(None)
        
#        ctrl.connect(None)


class TestTransformSlots(unittest.TestCase):

    def testConstructor(self):
        w = WorldObject()
        self.assertEqual(w.transform, mat4(1))
        self.assertEqual(w.pos, vec3(0))
        self.assertEqual(w.rot, mat3(1))
        self.assertEqual(w.scale, vec3(1))

    def testSetValueWithConnections(self):
        """Check setValue() in the presence of connections."""

        # Create an expression (which has a *fixed* output)
        e = Expression("(1,2,3)")
        w = WorldObject()
        w.pos = vec3(-1,5,0.5)
        self.assertEqual(w.pos, vec3(-1,5,0.5))
        self.assertEqual(w.transform, mat4(1).translation(vec3(-1,5,0.5)))

        # Connect the pos slot -> the new position must show up
        e.output_slot.connect(w.pos_slot)
        self.assertEqual(w.pos, vec3(1,2,3))
        self.assertEqual(w.transform, mat4(1).translation(vec3(1,2,3)))

        # Set a new pos -> should have no effect as the output slot of the
        # expression cannot be changed
        w.pos = vec3(0,0.2,0.5)
        self.assertEqual(w.pos, vec3(1,2,3))
        self.assertEqual(w.transform, mat4(1).translation(vec3(1,2,3)))

        # Set a new position via the transform slot -> should also have no
        # effect on the position
        w.transform = mat4([2,0,0,-1, 0,2,0,0.2, 0,0,2,1.7, 0,0,0,1])
        self.assertEqual(w.pos, vec3(1,2,3))
        self.assertEqual(w.transform, mat4([2,0,0,1, 0,2,0,2, 0,0,2,3, 0,0,0,1]))

######################################################################

if __name__=="__main__":
    unittest.main()
