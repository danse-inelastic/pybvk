#!/usr/bin/env python

# given the python module to create "system", calculate dispersion
# the python module is optional. if it is not given, then "system" file must exist already.


def run(systempy, N, df, inclusive=1):
    "inclusive: when generating regular Qs, include points on the edge (begin and end)"
    Vecs = 1
    cmds = []
    
    if systempy:
        cmds.append('python %s' % systempy)
        
    cmds += [
        'bvkregularQs %s %s' % (N, inclusive),
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
       help="frequency axis bin size(THz) for DOS",
       )

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")

    if len(args) == 1:
        systempy = args[0]
    else:
        systempy = None
        
    N = int(options.N)
    df = float(options.df)
    return run(systempy, N, df)
    
if __name__ == "__main__":
    main()

