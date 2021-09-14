
# Required setup
# 
# Download Raspberry Pi OS
# Burn SD Card
# Add empty SSH file to boot directory
# Add wpa_supplicant.conf to boot directory
#   country=US
#   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
#   update_config=1
# 
#   network={
#   scan_ssid=1
#   ssid="your_wifi_ssid"
#   psk="your_wifi_password"
#   }
#
# sudo apt update
# sudo apt full-upgrade
#
# Change Password
#
# sudo apt-get install -y i2c-tools python-dev python3-smbus
# Enable I2C via raspi-config
# 
# Copy Windows public key to ~/.ssh/authorized_keys
#
# Edit hosts file 
# 
# Edit /etc/rc.local Add the following line
# python /home/pi/pressure_mon.py /home/pi/pressure_data
#


import smbus
import time
import sys
#import argsparse


#parser = arguments.ArgumentParser()
#parser.add_Argument("sum",help = "Monitor Irrigation Water Pressure")



#args = parser.parse_args()

i2c = smbus.SMBus(1)

path = sys.argv[1]

addr = 0x48

# Config Values
os    = (1<<15)
chan0 = (4<<12)
chan1 = (5<<12)
chan2 = (6<<12)
chan3 = (7<<12)
pga   = (0<<9)
mode  = (1<<8)
dr    = (4<<5)
cmod  = (0<<4)
cpol  = (0<<3)
clat  = (0<<2)
cque  = (3<<0)

adc_cfg = os | chan0 | pga | mode | dr | cmod | cpol | clat | cque

volts = 6.144
max_cnt = 0x7fff

uvpercnt = volts/max_cnt
psi_per_volt = 100/4.0

# Read a register from the ADC
def rd_reg(raddr):
  val = i2c.read_i2c_block_data(addr, raddr, 2)
  tval = (val[0]*256)+val[1]
  return tval

# Write a register in the ADC
def wr_reg(raddr, val):
  i2c.write_i2c_block_data(addr, raddr, [(val/256)&0xff, val&0xff])

# Get ADC Data
def getAdcData():
  wr_reg(1, adc_cfg)
  while((rd_reg(1)&0x8000) == 0):
    continue
  val = rd_reg(0)
  return val

# Calculate PSI based upon voltage. 0 psi(0.5) 100 (4.5V) 
def pressureFromVoltage(volts):
    if volts < 0.5: 
      return 0.0
    return round((volts - 0.5)*psi_per_volt)

def getPressure():
  val = getAdcData()
  volts = val * uvpercnt
  return pressureFromVoltage(volts)

def getTimeStamp(ts):
  return (ts.tm_hour*3600) + (ts.tm_min*60) + ts.tm_sec

# Generate File Name 
def getFileName():
  ts = time.localtime()
  filename = path + "/" + "data_" + str(ts.tm_year) + "_" + str(ts.tm_mon) + "_" + str(ts.tm_mday) + ".dat"
  return filename

# Get the current day
def getCurDay():
  ts = time.localtime()
  return ts.tm_mday

# Set initial current day
curday = getCurDay()

lastpressure = -1
lastdatabypassed = False

f = open(getFileName(), "a")

# Endless While loop
while(1):
  time.sleep(1)
  if curday != getCurDay():
    f.close
    f = open(getFileName(), "a")
    curday = getCurDay()
    lastpressure = -1

  curpressure = getPressure()
  if curpressure != lastpressure:
    if lastdatabypassed:
      f.write(str(getTimeStamp(time.localtime())-1) + " " + str(lastpressure)+" " + "\n") 
    f.write(str(getTimeStamp(time.localtime())) + " " + str(curpressure)+" " + "\n") 
    lastpressure = curpressure
    lastdatabypassed = False
  else:
    lastdatabypassed = True
    

