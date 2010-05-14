#!/usr/bin/env python

# bvk core contains a bunch of binaries that works on a binary input
# file "system". this module provides harness around that
# so that it is easier to create pythonic applications running
# those core commands


import os, shutil


def createSystem(outputdir, systempy=None, system=None):
    """create "system" file in the given output directory
    the input could be
      system: path to the system file
      systempy: path to the python file that creates system file when executed
    """
    # can not specify both of systempy and system
    if systempy and system:
        raise ValueError, "both systempy and system are specified. systempy=%s, system=%s" %(
            systempy, system)

    # output
    path = os.path.join(outputdir, 'system')

    #
    if system:
        if not os.path.exists(system):
            raise RuntimeError, "system file %r does not exist" % system
        else:
            shutil.copyfile(system, path)
            return path
                            
    if systempy:
        if not os.path.exists(systempy):
            raise RuntimeError, "system python file %r does not exist" % systempy
        else:
            return createSystemFromSystemPy(systempy, outputdir)

    raise RuntimeError, "no input for creating 'system' file at %s" % path


def createSystemFromSystemPy(systempy, outputdir):
    "create 'system' file in the output directory given system python file"
    filename = os.path.basename(systempy)
    cmds = [
        'cp %s %s/' % (systempy, outputdir),
        'cd %s' % outputdir,
        'python %s' % filename,
        ]
    spawn(cmds)
    path = os.path.join(outputdir, 'system')
    if not os.path.exists(path):
        raise RuntimeError, "system python generator %r did not generate system files" % systempy
    return path


def execute(cmds, workdir=None, outputfiles=[]):
    # make work directory if necessary
    if not workdir:
        import tempfile
        workdir = tempfile.mkdtemp()

    # pwd
    pwd = os.path.abspath(os.curdir)

    # build the command to run
    allcmds = []
    allcmds.append('cd %s' % workdir)
    allcmds += cmds

    # run them
    spawn(allcmds)

    # move results
    for f in outputfiles:
        src = os.path.join(workdir, f)
        dest = os.path.join(pwd, f)
        try:
            shutil.move(src, dest)
        except Exception, msg:
            raise RuntimeError, "failed to move %s to %s:\n%s" %  (
                src,dest, msg)
        continue

    # clean up
    shutil.rmtree(workdir)
    
    return


def spawn(cmds):
    cmd = '&&'.join(cmds) 
    import os
    ret = os.system( cmd )
    if ret: raise RuntimeError, 'cmd %r failed' % (cmd,)
    return
