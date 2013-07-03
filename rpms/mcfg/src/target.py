"""This module contains only the class Target"""

import logging
import os
import os.path
import shutil

class Target:
    """A Target is a (configuration) file to be created or manipulated.

    Target class does not deal with ini file syntax.
    Each target has a list of editors associated to it.
    Target class knows the interface of editors and deals with backup issues.
    """

    def __init__(self):
        """The constructor takes no arguments, because the only one we know
        when reading an ini file is the section name, i. e. the symbolic
        name of the target. But that one we currently don't store.

        Access to targetfileName and edlist in Python way, no data hiding, no
        accessors needed.
        """

        # self.name = name     # don't think we need the name for any purpose
                               # except good error messages maybe
        self.targetfile = None
        self.edlist = []

    def run_editors(self, incr):
        """Run all editors on the edlist relevant for the current increment
        Take care of backup. Backup serves two purposes: A editor cannot
        read & write the same file anyway, but also it makes it easier to
        debug if something goes wrong. However, we keep only the backup of the
        first editor otherwise it gets to messy (in really tricky cases
        one could still commment out the unlink statement).
        """
        if self.targetfile == None:
            raise ValueError, "template error: no mcfg_filename"
        backup = self.backup()
        incr_edlist = filter( incr.is_current, self.edlist)

        logging.debug("Target.run_editors, target file: %s, incr: %s",
                      self.targetfile , incr.incr)
        if len(incr_edlist) > 0:
            for (num, edi) in enumerate(incr_edlist, 1):
                logging.debug( "   %d: %s" , num , edi.name )
            if backup:
                # don't follow symbolic links, maybe not so much a
                # security issue here, but can at least cause confusion
                if not (os.path.exists(self.targetfile) and
                        os.path.isfile(self.targetfile) and
                        not os.path.islink(self.targetfile)):
                    raise IOError, "Target file {0} does not exist or is not " \
                                     "a regular file".format(self.targetfile)
            elif os.path.exists(self.targetfile):
                raise IOError, "Target file {0} already exists".format(
                                self.targetfile)
        else:
            logging.debug("   x: (no editors in this increment)")
        for (num, edi) in enumerate(incr_edlist, 1):
            in_file = None
            if backup:
                in_file = "{0}.backup.{1}".format(self.targetfile, int(incr))
                if num > 1:
                    in_file = "{0}.{1}".format(in_file, num)
                shutil.move(self.targetfile, in_file)
            edi.run_it(in_file, self.targetfile)
            if backup and num > 1:
                os.unlink(in_file)

    def backup(self):
        """Tell whether backup is needed.
        An empty list of editors obviously does not need backup.
        Otherwise all editors on the list must agree on the property, if not
        an exception will be raised.
        """
        # we calcalute backup over the whole edlist, not only over the current
        # increment. In theory we could support copy_file in an earlier
        # increment and replace in a later one. But it just makes things
        # more complicated and as long as we don't have a use case for it,
        # we don't support it.
        if len(self.edlist) == 0:
            result = False
        else:
            result = self.edlist[0].backup()
            for edi in self.edlist:
                if result != edi.backup():
                    raise ValueError, "Editors with incompatible backup " \
                                     "policy for {0}".format(self.targetfile)
        return result
