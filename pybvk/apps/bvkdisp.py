#!/usr/bin/env python

# given the python module to create "system", calculate dispersion

# bvkdisp system-python-file N-kpts-in-1D


def run(systempy, N):
    Vecs = 1
    cmds = [
        'python %s' % systempy,
        'bvkregularQs %s' % N,
        'bvkdisps %s' % Vecs,
        #'bvkpartialdos %s %s' % (Vecs, df), 
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
    #parser.add_option(
    #    "-d", "--df", dest="df",
    #    default = 0.1,
    #    help="frequency axis bin size(THz)",
    #    )

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    systempy = args[0]
    N = int(options.N)
    #df = float(options.df)
    return run(systempy, N)
    
if __name__ == "__main__":
    main()

