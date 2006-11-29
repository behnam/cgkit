# Test the mayaascii module

import unittest
from cgkit import mayaascii

class TestMayaAscii(unittest.TestCase):

    def testMAReader_findString(self):
        """Test the MAReader.findString() method.
        """

        rd = mayaascii.MAReader()
        self.assertEqual(rd.findString(''), (None, None))
        self.assertEqual(rd.findString('Test string'), (None, None))
        self.assertEqual(rd.findString('a="foo"'), (2, 6))
        self.assertEqual(rd.findString('a="foo'), (2, None))
        self.assertEqual(rd.findString(r'a="foo\"'), (2, None))
        self.assertEqual(rd.findString(r'a="foo\"" - "spam"'), (2, 8))
        self.assertEqual(rd.findString(r'a="foo\"spam\""'), (2, 14))

    def testMAReader_splitCommand(self):
        """Test the MAReader.splitCommand() method.
        """

        rd = mayaascii.MAReader()
        self.assertEqual(rd.splitCommand('setAttr -k off ".v";'), (["setAttr", "-k", "off", ".v"],19))
        self.assertEqual(rd.splitCommand('setAttr -k off ".v"'), (["setAttr", "-k", "off", ".v"],-1))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;setAttr -k off ".v"'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;setAttr -k off ".v'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('setAttr -k off ".v";select -ne :defaultShaderList1;'), (["setAttr", "-k", "off", ".v"],19))
        self.assertEqual(rd.splitCommand('setAttr "-k off" foo ".v";select -ne :defaultShaderList1;'), (["setAttr", "-k off", "foo", ".v"],25))
        self.assertEqual(rd.splitCommand('setAttr "foo spam"'), (["setAttr", "foo spam"],-1))


######################################################################

if __name__=="__main__":
    unittest.main()
