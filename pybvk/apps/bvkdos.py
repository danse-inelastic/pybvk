#!/usr/bin/env python

# given the python module to create "system", calculate dos
# the python module is optional. if it is not given, then "system" file must exist already.

import os

def run(systempy, system, df, N, Vecs):
    # can not specify both of systempy and system
    if systempy and system:
        raise ValueError, "both systempy and system are specified. systempy=%s, system=%s" %(
            systempy, system)
    # if neither systempy nor system is specified, it is assumed that we have a "system" file
    if not systempy and not system:
        system = 'system'

    # check if input file exists
    if system:
        if not os.path.exists(system):
            raise RuntimeError, "system file %r does not exist" % system
        else:
            systempath = os.path.abspath(system)
    if systempy:
        if not os.path.exists(systempy):
            raise RuntimeError, "system python file %r does not exist" % systempy
        else:
            systempypath = os.path.abspath(systempy)
            systempyfilename = os.path.basename(systempy)

    #
    Vecs = int(Vecs)

    # make work directory
    import tempfile
    workdir = tempfile.mkdtemp()

    # pwd
    pwd = os.path.abspath(os.curdir)

    # build the command to run
    cmds = []
    cmds.append('cd %s' % workdir)

    if systempy:
        cmds.append('cp %s ./' % (systempypath,))
        cmds.append('python %s' % systempyfilename)

    if system:
        cmds.append('cp %s ./system' % (systempath,))
        
        
    cmds += [
        'bvkrandomQs %s' % N,
        'bvkdisps %s' % Vecs,
        'bvkpartialdos %s %s' % (Vecs, df),
        ]
    for f in ['DOS']:
        cmds.append('cp %s %s' % (f, pwd))
    print cmds
    spawn(cmds)

    import shutil
    shutil.rmtree(workdir)
    return


def spawn(cmds):
    cmd = '&&'.join(cmds) 
    import os
    ret = os.system( cmd )
    if ret: raise RuntimeError, 'cmd %r failed' % (cmd,)
    return


def ispythonfile(f):
    s = open(f)
    


from optparse import OptionParser

def main():
    usage = "usage: %prog [options] [system]"
    parser = OptionParser(usage)
    parser.add_option(
        "-N", "--N-kpts-1D", dest="N",
        default = 10,
        help="Number of k points in 1D for sampling reciprocal space",
        )
    parser.add_option(
        "-d", "--df", dest="df",
        default = 0.1,
        help="frequency axis bin size(THz)",
        )
    parser.add_option(
        "-E", "--compute-eigen-vectors",
        default = False,
        help='compute eigne vectors or not?',
        dest="Vecs",
        )
    parser.add_option(
        '-P', '--system-python-file',
        default = '',
        help = 'python file that generates the "system" file when executed. when this option is supplied, please do not specify the "system" file path as the argument',
        dest = 'systempy',
        )

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")

    if len(args) == 1:
        system = args[0]
    else:
        system = None
    N = int(options.N)
    df = float(options.df)
    Vecs= bool(options.Vecs)

    systempy = options.systempy
    return run(systempy, system, df, N, Vecs)
    
if __name__ == "__main__":
    main()

