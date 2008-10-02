#!/usr/bin/env python

# given the python module to create "system", calculate dos

# bvkdos system-python-file N-kpts-in-1D


def run(systempy, df, N, Vecs):
    Vecs = int(Vecs)
    cmds = [
        'python %s' % systempy,
        'bvkrandomQs %s' % N,
        'bvkdisps %s' % Vecs,
        'bvkpartialdos %s %s' % (Vecs, df), 
        ]
    print cmds
    return spawn(cmds)


def spawn(cmds):
    cmd = '&&'.join(cmds) 
    import os
    ret = os.system( cmd )
    if ret: raise RuntimeError, 'cmd %r failed' % (cmd,)
    return


from optparse import OptionParser

def main():
    usage = "usage: %prog [options] system-python-file"
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

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    systempy = args[0]
    N = int(options.N)
    df = float(options.df)
    Vecs= bool(options.Vecs)
    return run(systempy, df, N, Vecs)
    
if __name__ == "__main__":
    main()

