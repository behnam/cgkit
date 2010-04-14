# Test the eventmanager module

import unittest
from cgkit.eventmanager import eventManager, EventManager

class Receiver:
    def __init__(self, em=None):
        # Every callback adds a tuple to this list which is used to check
        # what callback has been called and in what order they have been called
        self.called = []
        self.em = em 
    
    def onSpam(self, arg=0):
        self.called.append(("spam", arg))
    
    def onEggs(self, arg1, arg2=None):
        self.called.append(("eggs", arg1, arg2))

    def onRemove(self):
        self.em.disconnect("Remove", self)
        self.called.append(("remove",))

    def otherCallback(self):
        self.called.append(("other",))


class TestEventManager(unittest.TestCase):
    
    def testEventManager(self):
        """Test the EventManager class.
        """
        em = eventManager()
        em.disconnectAll()
        rec = Receiver()
        
        em.connect("Spam", rec)
        em.connect("Spam", rec.otherCallback)
        em.event("Spam")
        self.assertEqual([("spam",0),("other",)], rec.called)
        
        em.disconnect("Spam", rec)
        rec.called = []
        em.event("Spam")
        self.assertEqual([("other",)], rec.called)
        
        em.disconnect("Spam", rec.otherCallback)
        rec.called = []
        em.event("Spam")
        self.assertEqual([], rec.called)

        # Check priorities
        em.connect("Spam", rec)
        em.connect("Spam", rec.otherCallback, priority=5)
        em.event("Spam")
        self.assertEqual([("other",), ("spam",0)], rec.called)
        
        # Add another receiver which must still be there after disconnect("Spam") has been called
        em.connect("Eggs", rec)
        em.disconnect("Spam")
        rec.called = []
        em.event("Spam")
        self.assertEqual([], rec.called)
        
        # Check that the Eggs receiver is still there...
        em.event("Eggs", arg2=5, arg1=3)
        self.assertEqual([("eggs", 3, 5)], rec.called)
        rec.called = []
        em.event("Eggs", 1, 2)
        self.assertEqual([("eggs", 1, 2)], rec.called)
        
        # Check disconnectAll()
        em.connect("Spam", rec)
        em.disconnectAll()
        rec.called = []
        em.event("Spam")
        em.event("Eggs", 3, 4)
        self.assertEqual([], rec.called)

    def testRemoveReceiver(self):
        """Test removing a receiver while the callbacks are still being called.
        
        (this has been a bug in earlier versions)
        """
        em = eventManager()
        em.disconnectAll()
        rec = Receiver(em=em)
        
        em.connect("Remove", rec)
        em.connect("Remove", rec.onSpam)
        em.connect("Remove", rec.otherCallback)
        em.event("Remove")
        self.assertEqual([("remove",),("spam",0),("other",)], rec.called)
        
        rec.called = []
        em.event("Remove")
        self.assertEqual([("spam",0),("other",)], rec.called)

######################################################################

if __name__=="__main__":
    unittest.main()
