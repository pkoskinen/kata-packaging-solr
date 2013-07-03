import datetime
import filecmp
import os
import sys
import unittest

# we live in subdirectory test, so we need to import the code to be tested
# from the parent directory. I don't like this hack, please suggest something
# better (well, nose does it already, but maybe not everybody uses it)
#
# better suggestion: http://docs.python.org/2/whatsnew/2.5.html
# see section "PEP 328: Absolute and Relative Imports", relative imports
# never touch a working code, so not implemented now
here=os.path.split( __file__ )[0]
if here == '' :
  here = os.getcwd()
above=os.path.split( here )[0]
hackedPath = [ above ]
hackedPath.extend( sys.path )
sys.path = hackedPath

import edfuncs

class TestEdfuncs(unittest.TestCase):

  def setUp(self):
    self.testFilesDir = os.path.join( here , "files" )

  def test_replaceSuccessful(self):
    # same files used by TestEditor.test_invokeEditor
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )

    # originally we used os.tempnam() here but it clutters up the test output
    # with a disturbing security warning.
    oFileName = os.path.join( self.testFilesDir , "replaceSuccessful.out-"
                                        + datetime.datetime.now().isoformat())

    # we could call the editor function in a easier way here, but let's
    # simulate it once the way it will be done when the name comes from a
    # text file
    func = getattr( edfuncs.Edfuncs , "replace" )
    func( iFileName , oFileName , 'toBeReplaced' , 'replacement' )

    oFileNameExpected = os.path.join( self.testFilesDir , "replace1.out.expected" )
    result = filecmp.cmp( oFileName , oFileNameExpected )
    if result:
      os.unlink( oFileName )
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName
    self.assertTrue( result )


  def test_replaceInputFileMissing(self):
    self.assertRaises(IOError, edfuncs.Edfuncs.replace, "foo", "bar", "1", "2")




  def test_copyFileSuccessful(self):
    iFileName = os.path.join(self.testFilesDir, "replace1.in" )
    oFileName = os.path.join(self.testFilesDir, "copyFileSuccessful.out-"
                                        + datetime.datetime.now().isoformat())
    edfuncs.Edfuncs.copy_file("dummy", oFileName, "location", iFileName)
    result = filecmp.cmp(iFileName, oFileName)
    os.unlink(oFileName)
    self.assertTrue(result)


  def test_CopyFileInputFileMissing(self):
    doesNotExist = "/tmp/seqwe/doesNotExist"
    args = ( "dummy", "dummy", "location",  doesNotExist )
    self.assertRaises(IOError, edfuncs.Edfuncs.copy_file, *args)
    # in Python 2.7 we could have used assertRaises as context manager,
    # in the first place, but we need to support Python 2.6
    # (of course this could be coded differently using try, but the
    # assertRaises conveys the idea what we are doing)
    try:
      edfuncs.Edfuncs.copy_file( *args )
    except IOError as e:
      self.assertEqual( "Input file " + doesNotExist + " missing" , str(e))


  def test_CopyFileTargetFileAlreadyThere(self):
    iFileName = os.path.join( self.testFilesDir , "replace1.in" )
    oFileName = os.path.join( self.testFilesDir , "replace1.out.expected" )
    args = ( "dummy", oFileName, "location",  iFileName )
    self.assertRaises( IOError , edfuncs.Edfuncs.copy_file , *args )
    # see comment about assertRaises above
    try:
      edfuncs.Edfuncs.copy_file(*args)
    except IOError as exc:
      self.assertEqual("Target file " + oFileName + " already exists",
                       str(exc))


  def test_CopyFileWrongParameter(self):
    args = ( "dummy" , "dummy" , "wrong" , "dummy" )
    self.assertRaises( ValueError , edfuncs.Edfuncs.copy_file, *args )
    # see comment about assertRaises above
    try:
      edfuncs.Edfuncs.copy_file(*args)
    except ValueError as e:
      self.assertEqual("Unknown parameter: wrong", str(e))


class TestEdfuncsManual(unittest.TestCase):
  """This class contains test cases, which cannot be run without previous
  manual preparation"""

  def setUp(self):
    self.testFilesDir = os.path.join( here , "files" )

  def test_replace_by_ip(self):
    manualReferenceFile = "/tmp/test-myip"
    # create that file manually, it must contain the current IP address without
    # any white space
    self.assertTrue(os.path.exists( manualReferenceFile))
    iFileName = os.path.join( self.testFilesDir , "ip.in" )

    # originally we used os.tempnam() here but it clutters up the test output
    # with a disturbing security warning.
    oFileName = os.path.join( self.testFilesDir , "ip.out-"
                                        + datetime.datetime.now().isoformat())

    # we could call the editor function in a easier way here, but let's
    # simulate it once the way it will be done when the name comes from a
    # text file
    func = getattr( edfuncs.Edfuncs , "replace_by_ip" )
    func( iFileName , oFileName , 'myip' , 'automatic' )

    result = filecmp.cmp(oFileName, manualReferenceFile)
    if result:
      os.unlink( oFileName )
    else:
      print >>sys.stderr , "\nUnexpected result in" , oFileName
    self.assertTrue( result )


if __name__ == '__main__':
  unittest.main()
