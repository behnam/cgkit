# Test the mayaascii module

import unittest
from cgkit import mayaascii

class TestReader(mayaascii.MAReader):
    def __init__(self):
        mayaascii.MAReader.__init__(self)
        self.cmds = []
    
    def onSetAttr(self, attr, vals, opts):
        self.cmds.append(("setAttr", attr, vals, opts))
    
    def onRelationship(self, args, opts):
        self.cmds.append(("relationship", args, opts))


class TestMayaAscii(unittest.TestCase):

    def testDefaultMAReader(self):
        rd = mayaascii.DefaultMAReader()
        rd.read("data/objects.ma")
        t = rd.nodelist[0]
#        print t.getAttrValue("t", "t", "double3")

    def testRelationshipCmd(self):
        """Check that the 'relationship' command gets processed.
        """
        rd = TestReader()
        rd.read("data/reftest.ma")
        cmds = [tup for tup in rd.cmds if tup[0]=="relationship"]
        self.assertEqual(('relationship', ['"link"', '":lightLinker1"', '":initialShadingGroup.message"', '":defaultLightSet.message"'], {}), cmds[0])
        self.assertEqual(('relationship', ['"link"', '":lightLinker1"', '":initialParticleSE.message"', '":defaultLightSet.message"'], {}), cmds[1])
        self.assertEqual(('relationship', ['"shadowLink"', '":lightLinker1"', '":initialShadingGroup.message"', '":defaultLightSet.message"'], {}), cmds[2])
        self.assertEqual(('relationship', ['"shadowLink"', '":lightLinker1"', '":initialParticleSE.message"', '":defaultLightSet.message"'], {}), cmds[3])

    def testMELCommands(self):
        rd = mayaascii.DefaultMAReader()
        rd.read("data/testmel.ma")

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
        self.assertEqual(rd.splitCommand('setAttr -k off ".v";'), (["setAttr", "-k", "off", '".v"'],19))
        self.assertEqual(rd.splitCommand('setAttr -k off ".v"'), (["setAttr", "-k", "off", '".v"'],-1))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;setAttr -k off ".v"'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('select -ne :defaultShaderList1;setAttr -k off ".v'), (["select", "-ne", ":defaultShaderList1"], 30))
        self.assertEqual(rd.splitCommand('setAttr -k off ".v";select -ne :defaultShaderList1;'), (["setAttr", "-k", "off", '".v"'],19))
        self.assertEqual(rd.splitCommand('setAttr "-k off" foo ".v";select -ne :defaultShaderList1;'), (["setAttr", '"-k off"', "foo", '".v"'],25))
        self.assertEqual(rd.splitCommand('setAttr "foo spam"'), (["setAttr", '"foo spam"'],-1))
        self.assertEqual(rd.splitCommand('setAttr "foo spam'), (["setAttr", '"foo spam"'],-1))

    def testMAReader_getOpt(self):
        """Test the MAReader.splitCommand() method.
        """

        rd = mayaascii.MAReader()
        args,n = rd.splitCommand('setAttr -k off ".v"')
        self.assertEqual(rd.getOpt(args[1:], rd.setAttr_opt_def, rd.setAttr_name_dict), (['".v"'], dict(keyable=["off"])))

        args,n = rd.splitCommand('setAttr "-k" off ".v"')
        self.assertEqual(rd.getOpt(args[1:], rd.setAttr_opt_def, rd.setAttr_name_dict), (['".v"'], dict(keyable=["off"])))

        args,n = rd.splitCommand('setAttr ".cuvs" -type "string" "map1";')
        self.assertEqual(rd.getOpt(args[1:], rd.setAttr_opt_def, rd.setAttr_name_dict), (['".cuvs"', '"map1"'], dict(type=["string"])))

        self.assertEqual(rd.getOpt(["-5"], rd.setAttr_opt_def, rd.setAttr_name_dict), (["-5"], {}))


######################################################################

if __name__=="__main__":
    unittest.main()
