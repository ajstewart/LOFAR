#!/usr/bin/env python

import subprocess, optparse, os
import pyrap.tables as pt
import math as m

usage = "usage: python %prog [options] dataset.MS outfile"
description="Generate sky model directly from a measurement set."
vers="1.1"

#Defines the options as present in gsm.py
parser = optparse.OptionParser(usage=usage, version="%prog v{0}".format(vers), description=description)
parser.add_option("-r", "--radius", action="store", type="float", dest="radius", default=5., help="Specify cone radius in degrees [default: %default]")
parser.add_option("-c", "--cutoff", action="store", type="float", dest="cutoff", default=0.1, help="Choose the minimum flux of VLSS sources to use [default: %default]")
parser.add_option("-t", "--assoctheta", action="store", type="float", dest="assoctheta", default=0.00278, help="Uncertainty in matching in degrees [default: %default (10 arcsec)]")
(options, args) = parser.parse_args()

#gsm.py outfile RA DEC radius [vlssFluxCutoff [assocTheta]]


def clean(f):
  input_model=open(f+".temp", 'r')
	output_model=open(f, 'w+r')
	source_names=[]
	for line in input_model:
		source=str(line)
		source_name=source[:11]
		# print source_name
		if source_name not in source_names:
			source_names.append(source_name)
			output_model.write(source)
		else:
			print "Source {0} was doubled".format(source_name)
	input_model.close()
	output_model.close()
	print "Cleaned sky model {0} produced".format(f)
	subprocess.call("rm {0}.temp".format(f), shell=True)


ms=args[0]
outfile=args[1]
rad=options.radius
cut=options.cutoff
asth=options.assoctheta

print "Obtaining RA and Dec of MS..."
obs = pt.table(ms + '/FIELD')
ra = float(obs.col('PHASE_DIR')[0][0][0])
if ra > 0.:
	ra*=(180./m.pi)
else:
	ra=360.+(ra*(180./m.pi))
dec = float(obs.col('PHASE_DIR')[0][0][1])*(180./m.pi)
print "RA:{0}\tDec:{1}".format(ra, dec)
obs.close()
obs.close()

subprocess.call("gsm.py {0}.temp {1} {2} {3} {4} {5}".format(outfile, ra, dec, rad, cut, asth), shell=True)

clean(outfile)
