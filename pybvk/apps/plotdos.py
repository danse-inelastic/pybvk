#!/usr/bin/env python

# plot the density of states in idf format

def run(path):
    from idf import DOS
    info, e, I = DOS.read(path)
    import pylab
    pylab.plot(e, I)
    pylab.show()
    return


from optparse import OptionParser

def main():
    usage = "usage: %prog [options] filepath"
    parser = OptionParser(usage)
    # parser.add_option(
    # "-N", "--N-kpts-1D", dest="N",
    #    default = 10,
    #    help="Number of k points in 1D for sampling reciprocal space",
    #    )
    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")

    if len(args) == 1:
        filename = args[0]
    else:
        filename = 'DOS'
    return run(filename)

    
if __name__ == "__main__":
    main()

