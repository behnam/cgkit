# Test the sl module

import unittest
from cgkit import sl
from cgkit.cgtypes import vec3
import math

class TestSL(unittest.TestCase):
    """Test the sl module.
    """
    
    def testMath(self):
        """Test the math functions.
        """
        self.assertEqual(math.pi, sl.PI)
        self.assertEqual(0.3, sl.abs(-0.3))
        self.assertEqual(math.acos(0.2), sl.acos(0.2))
        self.assertEqual(math.asin(0.2), sl.asin(0.2))
        self.assertEqual(math.atan(0.2), sl.atan(0.2))
        self.assertEqual(math.atan2(0.2, 0.5), sl.atan(0.2, 0.5))
        self.assertEqual(2, sl.ceil(1.3))
        self.assertEqual(0.3, sl.clamp(0.3, 0.0, 1.0))
        self.assertEqual(0.0, sl.clamp(-0.1, 0.0, 1.0))
        self.assertEqual(1.0, sl.clamp(1.5, 0.0, 1.0))
        self.assertEqual(math.cos(0.2), sl.cos(0.2))
        self.assertEqual(math.exp(0.2), sl.exp(0.2))
        self.assertEqual(math.degrees(0.3), sl.degrees(0.3))
        self.assertEqual(1.0, sl.floor(1.8))
        self.assertEqual(1.0/math.sqrt(5), sl.inversesqrt(5))
        self.assertEqual(math.log(8), sl.log(8))
        self.assertEqual(math.log(8, 2), sl.log(8, 2))
        self.assertEqual(5, sl.max(1, 5, 3))
        self.assertEqual(1, sl.min(1, 5, 3))
        self.assertEqual(0.5, sl.mix(0.0, 1.0, 0.5))
        self.assertEqual(0.5, sl.mod(2.5, 1))
        self.assertEqual(16, sl.pow(4, 2))
        self.assertEqual(math.radians(45), sl.radians(45))
        self.assertEqual(2.0, sl.round(2.4))
        self.assertEqual(-1, sl.sign(-18))
        self.assertEqual(1, sl.sign(18))
        self.assertEqual(0, sl.sign(0))
        self.assertEqual(math.sin(0.2), sl.sin(0.2))
        self.assertEqual(0.5, sl.smoothstep(0.0, 1.0, 0.5))
        self.assertEqual(0.5, sl.spline(0.5, [0.0, 0.0, 1.0, 1.0]))
        self.assertEqual(4, sl.sqrt(16))
        self.assertEqual(0, sl.step(1.0, 0.5))
        self.assertEqual(1, sl.step(1.0, 1.5))
        self.assertEqual(math.tan(0.2), sl.tan(0.2))
        
        # For now, just make sure the functions can be called
        sl.color_cellnoise(0.3,0.2)
        sl.color_noise(0.1,0.3)
        sl.color_pnoise(0.1,0.3, 2, 2)
        sl.color_random()
        sl.float_cellnoise(0.3,0.2)
        sl.float_noise(0.1,0.3)
        sl.float_pnoise(0.1,0.3, 2, 2)
        sl.float_random()
        sl.point_cellnoise(0.3,0.2)
        sl.point_noise(0.1,0.3)
        sl.point_pnoise(0.1,0.3, 2, 2)
        sl.point_random()
        sl.vector_cellnoise(0.3,0.2)
        sl.vector_noise(0.1,0.3)
        sl.vector_pnoise(0.1,0.3, 2, 2)

    def testGeomFuncs(self):
        """Test the geometric functions.
        """
        self.assertEqual(2.0, sl.distance(vec3(1,0,0), vec3(3,0,0)))
        self.assertEqual(vec3(0,1,0), sl.faceforward(vec3(0,1,0), vec3(0,1,0), vec3(0,-1,0)))
        self.assertEqual(vec3(0,-1,0), sl.faceforward(vec3(0,1,0), vec3(0,1,0), vec3(0,1,0)))
        self.assertEqual(1.0, sl.length(vec3(0,1,0)))
        self.assertEqual(vec3(0,1,0), sl.normalize(vec3(0,3,0)))
        self.assertEqual(1.0, sl.ptlined(vec3(0,0,0), vec3(1,0,0), vec3(0,1,0)))
        self.assertEqual(vec3(-0.5,0.5,0), sl.reflect(vec3(0.5,0.5,0), vec3(-1,0,0)))
        self.assertEqual(vec3(0.5,0.5,0).refract(vec3(-1,0,0), 0.5), sl.refract(vec3(0.5,0.5,0), vec3(-1,0,0), 0.5))
        self.assertEqual(0.5, sl.xcomp(vec3(0.5, 1.0, 1.5)))
        self.assertEqual(1.0, sl.ycomp(vec3(0.5, 1.0, 1.5)))
        self.assertEqual(1.5, sl.zcomp(vec3(0.5, 1.0, 1.5)))
        v = vec3(1,2,3)
        sl.setxcomp(v, 0.5)
        self.assertEqual(vec3(0.5,2,3), v)
        sl.setycomp(v, 1.0)
        self.assertEqual(vec3(0.5,1.0,3), v)
        sl.setzcomp(v, 1.5)
        self.assertEqual(vec3(0.5,1.0,1.5), v)

        self.assertEqual(0.5, sl.comp(vec3(0.5, 1.0, 1.5), 0))
        self.assertEqual(1.0, sl.comp(vec3(0.5, 1.0, 1.5), 1))
        self.assertEqual(1.5, sl.comp(vec3(0.5, 1.0, 1.5), 2))
        c = vec3(1,2,3)
        sl.setcomp(c, 0, 0.5)
        self.assertEqual(vec3(0.5,2,3), c)
        sl.setcomp(c, 1, 1.0)
        self.assertEqual(vec3(0.5,1.0,3), c)
        sl.setcomp(c, 2,  1.5)
        self.assertEqual(vec3(0.5,1.0,1.5), c)
        
    def testStrFuncs(self):
        """Test the string functions.
        """
        self.assertEqual("ab", sl.concat("a", "b"))
        self.assertEqual("c=(0.2, 0.3, 0.4)", sl.format("c=%c", vec3(0.2,0.3,0.4)))
        self.assertEqual(True, sl.match("pa", "spam"))
        self.assertEqual(False, sl.match("ap", "spam"))

######################################################################

if __name__=="__main__":
    unittest.main()
