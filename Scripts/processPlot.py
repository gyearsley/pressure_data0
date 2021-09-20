#
# sudo apt install python-pip or python3-pip
# sudo pip install matplotlib
# sudo pip install numpy
#
#

import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path
import glob
import datetime
import calendar
import sys

class PressureData:
  def __init__(self, filename):
    self.x1 = []
    self.y1 = []
    self.readPressureData(filename)
    self.getDate(filename)

  def readPressureData(self, filename):
    if os.path.exists(filename):
      fp = open(filename)
      finfo = fp.readlines()
      for f in finfo:
        f1 = f.rstrip()
        flds =  f1.split()
        if len(flds) == 2:
          self.x1.append(int(flds[0]))
          self.y1.append(float(flds[1]))
    else: 
      print("ERROR...File "+filename+" does not exist")
      exit(1)

  def getDate(self, filename):
    bf = os.path.basename(filename)
    self.fn = os.path.splitext(bf)[0]
    junk, year, mon, day = self.fn.split("_")
    date_val = datetime.date(int(year), int(mon), int(day))
    dow = date_val.weekday()
    dowStr = calendar.day_name[dow]
    monStr = calendar.month_name[int(mon)]
    self.titleStr = "Pressure Data "+dowStr+" "+monStr+" "+str(day)+", "+str(year)



class PlotPressureData:
  def __init__(self, data):
    self.genHourXAxis() 
    self.dptr = data

  def genPlot(self, filepath):
    fig, axs = plt.subplots()
    #plt.xlabel("Seconds")
    #ax.set_xlabel("Time")
    axs.set_ylabel("Pressure PSI")
    axs.grid(True)
    axs.axis([0,86400,0,70])
    axs.set_xticks(self.xd)
    axs.set_xticklabels(self.tl, rotation='vertical')
    axs.set_title(self.dptr.titleStr)
    axs.plot(self.dptr.x1,self.dptr.y1)
    #plt.show()
    ofile = self.getOutFile(filepath)
    plt.savefig(ofile, format="png")
    #plt.clear()

  def getOutFile(self, path):
    ofile = os.path.join(path, self.dptr.fn+".png") 
    return ofile

  def genHourXAxis(self):
    self.xd = np.arange(0, 86400, 3600)
    self.tl = ["12AM"]
    for h in np.arange(1,13,1):
      self.tl.append(str(h)+"AM")
    for h in np.arange(1,12,1):
      self.tl.append(str(h)+"PM")

datapath = sys.argv[1]

plotpath = sys.argv[2]
#path = "./plots"
files = glob.glob(datapath+"/data*.dat")
for f in files:
  day = PressureData(f)
  pp = PlotPressureData(day)

  if not os.path.exists(pp.getOutFile(plotpath)):
    pp.genPlot(plotpath)
    print(f)
  else:
    print(f+" Skipped")


