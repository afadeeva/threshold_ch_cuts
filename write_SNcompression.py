# Load libraries
import sys, os
import ROOT
from larlite import larlite as fmwk
from ROOT import compress

# Create ana_processor instance
my_proc=fmwk.ana_processor()

# Specify IO mode
my_proc.set_io_mode(fmwk.storage_manager.kBOTH)
#my_proc.set_io_mode(fmwk.storage_manager.kWRITE)
#my_proc.set_io_mode(fmwk.storage_manager.kREAD)


for x in xrange(len(sys.argv)-8):
    my_proc.add_input_file(sys.argv[x+1])

#set output data file
#my_proc.set_output_file(outfilename)

# Set output root file: this is a separate root file in which your
# analysis module can store anything such as histograms, your own TTree, etc.
my_proc.set_ana_output_file("")
my_proc.set_output_file(sys.argv[-7])

#my_proc.set_output_rootdir("scanner")
# Create analysis class instance. For this example, ana_base.
# To show how one can run multiple analysis modules at once,
# we make multiple ana_base instance.

compAna=fmwk.ExecuteCompression()
compAna.SetSaveOutput(True)
compAna.SetUseSimch(False)
#add Compression Algorithm
compAlgo = compress.CompressionAlgosncompress()
compAlgo.SetDebug(False)
compAlgo.SetVerbose(False)
compAlgo.SetFillTree(True)
compAlgo.SetBlockSize(64)
compAlgo.SetBaselineThresh(2.0)
compAlgo.SetVarianceThresh(2.0)

threshU = float(sys.argv[-6])
threshV = float(sys.argv[-5])
threshY = float(sys.argv[-4])

ubU = int(sys.argv[-3])
ubV = int(sys.argv[-2])
ubY = int(sys.argv[-1])

compAlgo.SetPolarity(ubU,ubV,ubY)
compAlgo.SetCompressThresh(threshU,threshV,threshY)
compAlgo.SetMaxADC(4095)
compAlgo.SetUVYplaneBuffer(7,8,7,8,7,8)
#compAlgo.SetUVYplaneBuffer(30,55,15,20,15,10);
compAna.SetCompressAlgo(compAlgo)

#add HIT study Algorithm
compStudy = compress.CompressionStudyHits()
compStudy.setThreshold(5.)
compStudy.setConsecutiveTicks(3)

#add IDE study Algorithm
compIDE = compress.CompressionStudyIDEs()
compIDE.SetVerbose(False)

compAna.SetCompressAlgo(compAlgo)
#compAna.SetCompressStudy(compStudy)
#compAna.SetIDEStudy(compIDE)

# Add analysis modules to the processor

my_proc.add_process(compAna)

# Let's run it.

my_proc.run(0,20)

# done!
