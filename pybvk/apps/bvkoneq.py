#!/usr/bin/env python


def run(model, Q, cartesian):
    # print model, Q, cartesian

    # create temporary work directory
    import tempfile, os
    workdir = tempfile.mkdtemp()
    print '* work directory: %s' % workdir

    # create the system file in the temporary work directory
    from bvk import systemFromModel
    systempath = os.path.join(workdir, 'system')
    systemFromModel(model, filename=systempath)

    # create the WeightedQ file in the temporary work directory
    wqpath = os.path.join(workdir, 'WeightedQ')
    createWeightedQ(Q, wqpath)

    from bvk.applications.executionharness import execute

    # build the command to run
    cmds = []
    Vecs = 1
    cmds += [
        'bvkdisps %s' % Vecs,
        ]
    expected = [
        'Polarizations',
        'Omega2',
        'WeightedQ',
        ]

    # run
    execute(cmds, workdir=workdir, outputfiles=expected)

    # get results
    info, omega2 = readOmega2()
    omega2 = omega2[0]
    
    info, pols = readPols()
    pols = pols[0]
    
    # print omega2, pols
    writeOmegaTxt(omega2, 'omega2')
    writePolsTxt(pols, 'pols')
    return


def writeOmegaTxt(omega2, outfile):
    stream = open(outfile, 'w')
    for v in omega2:
        stream.write(_format(v))
        stream.write('\n')
        continue
    return


def writePolsTxt(pols, outfile):
    stream = open(outfile, 'w')
    nb_d, nb, d = pols.shape
    assert nb_d == nb*d
    for mode in pols:
        for v in mode:
            stream.write('\t'.join([str(i) for i in v]) + '\n')
        stream.write('\n')
    return


def _format(v):
    return '%10g'% v


def readOmega2():
    from idf import Omega2
    return Omega2.read()


def readPols():
    from idf import Polarizations
    return Polarizations.read()


def createWeightedQ(Q, outfile):
    from idf import WeightedQ
    NQ = 1; D = 3
    import numpy
    Q = numpy.array(Q)
    Q.shape = NQ, D
    weight = numpy.ones((NQ,1), float)
    WeightedQ.write(Q, weight, outfile)
    return


def loadModel(path):
    code = open(path).read()
    env = {}
    exec code in env
    if not env.has_key('model'):
        raise RuntimeError, "the model file %r does not define a bvk model" % path
    model = env['model']
    return model
    


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] model"
    parser = OptionParser(usage)
    parser.add_option(
        "-Q", dest="Q",
        default = '(0,0,0)',
        help="Q point",
        )
    parser.add_option(
       "-c", "--cartesian", dest="cartesian",
       action = 'store_true',
       help="if present, the Q point is in cartesian coordinate system",
       )
    parser.add_option(
        '-x', '--crystal', dest='cartesian',
        action = 'store_false',
        default = False,
        help="if present, the Q point is in crystal coordinate system",
        )

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")

    if len(args) == 1:
        model = args[0]
    else:
        model = 'model'

    import os
    if not os.path.exists(model):
        raise RuntimeError, "model %r does not exist" % model
    model = loadModel(model)
    Q = eval(options.Q)
    cartesian = options.cartesian
    return run(model, Q, cartesian)

    
if __name__ == "__main__":
    main()

