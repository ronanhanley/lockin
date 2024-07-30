import serial
import time
import numpy as np
import qcodes as qc
from qcodes.instrument_drivers.stanford_research.SR830 import SR830
from qcodes import VisaInstrument

# Create an instance of the SR830 instrument
lockin = SR830('lockin', 'GPIB0::8::INSTR')
freq = np.linspace(80000,100000,500) # frequency array for scan in Hz, change depending on range of scan
Xs = np.empty_like(freq)
Ys = np.empty_like(freq)
Rs = np.empty_like(freq)
Thetas = np.empty_like(freq)
lockin.write('OUTX1\n') #tells lock in to send output to GPIB interface
lockin.write('FMOD1\n') #set trigger to internal, change to 0 if we want to use external trigger
lockin.write('ISRC0\n') #set input config to A
lockin.write('OFLT3\n') #set time constant, check manual for keys
lockin.write('OFSL2\n')
lockin.write('SLVL1.00\n')
lockin.frequency(freq[0])
time.sleep(10) #when you set the time constant it takes a while to restabilize 
i = 0
for f in freq:
    lockin.frequency(f) #set reference frequency
    #time.sleep(1)
    #lockin.write('OUTX1\n') #tells lock in to send output to GPIB interface
    #theta1 = float(lockin.ask('OUTP?4\n'))#asks for theta
    #lockin.write('OUTX1\n') #tells lock in to send output to serial interface
    #theta2 = float(lockin.ask('OUTP?4\n')) #asks for theta again
    #if (abs(theta1-theta2)>.1): #checks if theta is changing by more than .1
     #   lockin.write('APHS\n') #auto phase if needed
      #  time.sleep(3) #autophase needs "several time constants" to work and I am being overly cautious 
    lockin.write('OUTX1\n') #tells lock in to send output to serial interface
    xy = np.fromstring(lockin.ask('SNAP? 1,2,3,4'),sep=',') #asks for X ,Y, R, theta
    Xs[i] = xy[0] #save X to array of X values
    Ys[i]=xy[1] #save Y to array of Y values
    Rs[i]=xy[2]
    Thetas[i]=xy[3]
    i=i+1 
run_name= "peak_search"
output_path_x = "c:/Users/hanle/uiuc reu/lockin spectrum data/x_" + run_name +".txt"
output_path_y = "c:/Users/hanle/uiuc reu/lockin spectrum data/y_" + run_name +".txt"
output_path_f = "c:/Users/hanle/uiuc reu/lockin spectrum data/f_" + run_name +".txt"
output_path_R = "c:/Users/hanle/uiuc reu/lockin spectrum data/r_" + run_name +".txt"
output_path_theta = "c:/Users/hanle/uiuc reu/lockin spectrum data/theta_" + run_name +".txt"
np.savetxt(output_path_x,Xs,delimiter=',')
np.savetxt(output_path_y,Ys,delimiter=',')
np.savetxt(output_path_f,freq,delimiter=',')
np.savetxt(output_path_R,Rs,delimiter=',')
np.savetxt(output_path_theta,Thetas,delimiter=',')