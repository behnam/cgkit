# Test the slparams module

import unittest
from cgkit import slparams

class TestSlparams(unittest.TestCase):
    
    def testSlparams(self):
        """Test the slparams.slparams() function.
        """
        res = slparams.slparams("data/testshader.sl")
        self.assertEqual(len(res), 1)

        type,name,params = res[0]
        
        self.assertEqual(type, "surface")
        self.assertEqual(name, "testshader")
        self.assertEqual(len(params), 6)
        self.assertEqual(params[0], ('', 'uniform', 'float', None, 'Ka', None, '1'))
        self.assertEqual(params[1], ('', 'varying', 'vector', None, 'norm', "current", '0'))
        self.assertEqual(params[2], ('', 'uniform', 'float', 2, 'uv', None, '{1, 2}'))
        self.assertEqual(params[3], ('output', 'uniform', 'point', None, 'out', "world", '(0, 0, 0)'))
        self.assertEqual(params[4], ('', 'uniform', 'color', None, 'col', "rgb", '(1, 1, 1)'))
        self.assertEqual(params[5], ('', 'uniform', 'float', None, 'Kd', None, '0.5'))
        

######################################################################

if __name__=="__main__":
    unittest.main()
