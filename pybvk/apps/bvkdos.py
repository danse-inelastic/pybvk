#!/usr/bin/env python

# given the python module to create "system", calculate dos
# the python module is optional. if it is not given, then "system" file must exist already.

import os

def run(systempy, system, df, N, Vecs):
    # if neither systempy nor system is specified, it is assumed that we have a "system" file
    if not systempy and not system:
        system = 'system'

    # create temporary work directory
    import tempfile
    workdir = tempfile.mkdtemp()

    # create the system file in the temporary work directory
    from bvk.applications.executionharness import createSystem, execute
    system = createSystem(workdir, systempy=systempy, system=system)

    #
    # build the command to run
    Vecs = int(Vecs)
    cmds = [
        'bvkrandomQs %s' % N,
        'bvkdisps %s' % Vecs,
        'bvkpartialdos %s %s' % (Vecs, df),
        ]
    return execute(cmds, workdir=workdir, outputfiles=['DOS'])


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

