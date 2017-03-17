import os,sys
import ROOT
from larlite import larlite as fmwk
import numpy as np
import matplotlib.pyplot as plt

if (len(sys.argv) != 2):
    print 'ERROR: run as follows:'
    print 'python hitamplitude_profile.py WIRE_FILE.ROOT'
    print 'script currently accepts a single input file'
    sys.exit(0)

# vectors where to store ADC amplitudes
ADC_Y_max_v = []
ADC_V_max_v = []
ADC_U_max_v = []

ADC_Y_min_v = []
ADC_V_min_v = []
ADC_U_min_v = []

#ADC_ch_max_mat = [[]]*8256
#ADC_ch_min_mat = [[]]*8256
# DC
ADC_ch_max_mat = {}
ADC_ch_min_mat = {}

# open ROOT file
fin = ROOT.TFile(sys.argv[-1])
# open TTree
t = fin.Get('wire_caldata_tree')
print "entries ", t.GetEntries()
# loop over all entries in TTree (each entry one event)
for n in xrange(2):   #t.GetEntries()):   # t.GetEntries()-1,(t.GetEntries()-11),-1):  #t.GetEntries()):

    # get nth entry
    t.GetEntry(n)

    # get larlite wire branch. This is an instance
    # of event_wire which you can find in core/DataFormat/wire.h
    # this won't work if larlite is not setup
    # wire_v is a C++ std::vector so you can use all
    # the functions you know about std::vectors on it
    wire_v = t.wire_caldata_branch
#    print "wire_v ", wire_v.size() 
    # loop through all wires
    for i in xrange(wire_v.size()):

        wire = wire_v.at(i)
        channel = wire.Channel()
    	#print 'channel ',channel
     	#continue 
        #if(channel<100):
        # the goal is to find, for each wire, the
        # maximum (or minimum, it is up to you) ADC value for that wire
        # and plot it
        # to figure out how to navigate the wire object go read
        # core/DataFormat/wire.h

        # the plane number is a bit tricky, so you get that like this:
        plane = int(wire.View())

        ROIs = wire.SignalROI()

        ranges = ROIs.get_ranges()

        # copy of maximum ADCs for this wire
        maxadcs = []
        minadcs = []
	    #print "size of ranges ", ranges.size()
        for j in xrange(ranges.size()):
	    
            print "channel is ", channel
            data = ranges.at(j).data()
            adcmax = -1
            adcmin = 4095
            for adc in data:
                if (adc > adcmax): adcmax = adc
                if (adc < adcmin): adcmin = adc
                print "adc is ", adc
            maxadcs.append( adcmax )
            minadcs.append( adcmin )
        """
        if (plane == 2):
            for adc in maxadcs:
                ADC_Y_max_v.append( adc )
            for adc in minadcs:
                ADC_Y_min_v.append( adc )
        if (plane == 1):
            for adc in maxadcs:
                ADC_V_max_v.append( adc )
            for adc in minadcs:
                ADC_V_min_v.append( adc )
        if (plane == 0):
            for adc in maxadcs:
                ADC_U_max_v.append( adc )
            for adc in minadcs:
                ADC_U_min_v.append( adc )
        """
        # print "size of max/min ADCs ", len(maxadcs)," ", len(minadcs)
        if not (channel in ADC_ch_max_mat):
            ADC_ch_max_mat[channel] = []
        if not (channel in ADC_ch_min_mat):
            ADC_ch_min_mat[channel] = []
        for adc in maxadcs:
            ADC_ch_max_mat[channel].append( adc )        
        for adc in minadcs:
            ADC_ch_min_mat[channel].append( adc )
sys.exit()

#for channel in ADC_ch_max_mat:
   # print 'channel %i has entries '%channel
   # print ADC_ch_max_mat[channel]
   # print
   # print


#        print "matrix value max  ", ADC_ch_max_mat[channel]   
#        print "matrix value min  " , ADC_ch_min_mat[channel]   
#for g in xrange(len( ADC_ch_max_mat[10])):
 #  print "difference ", ADC_ch_max_mat[10][g] - ADC_ch_max_mat[101][g]

# we filled the vectors, let's plot them
# how to make histograms using matplotlib?
# se here: http://matplotlib.org/1.2.1/examples/api/histogram_demo.html
# or our many examples here: https://github.com/NevisUB/Tutorials/tree/master/matplotlib
tfile = ROOT.TFile("per_allch_max.root","RECREATE")
h_max_v = []
print "Filling histograms for max"
for channel in ADC_ch_max_mat:
 #   print 'channel %i has entries '%channel
  #  print ADC_ch_max_v
   # print
    #print
    #continue
    ch_ADC = ROOT.TH1I("ch%d_ADC" % channel,"channel %d ADC vals" % channel ,200,0,200)
    for adc in ADC_ch_max_mat[channel]:
        ch_ADC.Fill(int(adc))	
    h_max_v.append( ch_ADC )
#    print "channel (write loop) ", channel
print "Writing Max File"
for h in h_max_v:
   h.Write()
tfile.Close()

tf = ROOT.TFile("per_allch_min.root","RECREATE")
h_min_v = []
print "Filling histograms for min"
for channel in ADC_ch_min_mat:
    ch_ADC_min = ROOT.TH1I("ch%d_ADC_min" % channel,"channel %d ADC vals" % channel ,200,-200,0)
    for adc in ADC_ch_min_mat[channel]:
        ch_ADC_min.Fill(int(adc))	
    h_min_v.append( ch_ADC_min )

print "Writing Min File"
for h in h_min_v:
   h.Write()
tf.Close()                                                                          

bob = ROOT.TFile("chall_adc.root","RECREATE")
ch_ADC_min_all = ROOT.TH2I("ch_ADC_min_all","channel vs ADC",8256,0,8256,200,-200,0)
ch_ADC_max_all = ROOT.TH2I("ch_ADC_max_all","channel vs ADC",8256,0,8256,200,0,200)
for channel in ADC_ch_min_mat:
    for adc in ADC_ch_min_mat[channel]:
        ch_ADC_min_all.Fill(int(channel),int(adc))	
for channel in ADC_ch_max_mat:
    for adc in ADC_ch_max_mat[channel]:
        ch_ADC_max_all.Fill(int(channel),int(adc))	
ch_ADC_min_all.Write()
ch_ADC_max_all.Write()
bob.Close()                                                                          

"""
# change font-size once for entire plotting routine
plt.rcParams.update({'font.size': 20})

# Plane 2:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(0,200,100) # arguments are min, max, nbins
plt.hist( ADC_Y_max_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 2')
plt.xlabel('Max ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([0,200])
#plt.ylim([X,X])
plt.legend()
plt.show()


# Plane 1:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(0,100,100) # arguments are min, max, nbins
plt.hist( ADC_V_max_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 1')
plt.xlabel('Max ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([0,100])
#plt.ylim([X,X])
plt.legend()
plt.show()

# Plane 0:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(0,100,100) # arguments are min, max, nbins
plt.hist( ADC_U_max_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 0')
plt.xlabel('Max ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([0,100])
#plt.ylim([X,X])
plt.legend()
plt.show()

# Plane 2:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(-100,0,100) # arguments are min, max, nbins
plt.hist( ADC_Y_min_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 2')
plt.xlabel('Min ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([-100,0])
#plt.ylim([X,X])
plt.legend()
plt.show()

# Plane 1:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(-100,0,100) # arguments are min, max, nbins
plt.hist( ADC_V_min_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 1')
plt.xlabel('Min ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([-100,0])
#plt.ylim([X,X])
plt.legend()
plt.show()

# Plane 0:
fig = plt.figure(figsize=(10,10))
BINS = np.linspace(-100,0,100) # arguments are min, max, nbins
plt.hist( ADC_U_min_v, bins=BINS, histtype='stepfilled', color='r', label='Plane 0')
plt.xlabel('Min ADC amplitude')
plt.title('Pulse Height Distribution for SN output waveforms',fontsize=16)
plt.grid()
plt.xlim([-100,0])
#plt.ylim([X,X])
plt.legend()
plt.show()
    
"""
    
