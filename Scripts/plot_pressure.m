# Prevent Octave from thinking that this
# is a function file:

1;


function plotData (days, data)  
  #plot(data(:,1), data(:,2));
  plot(data(:,1),data(:,2));
  set(gca,"XTick",0:3600*24:24*3600*days);
  grid on;
  set(gca,'xminorgrid','on');
  #set(gca,'xminorgrid',0:3600:24*3600*days);
  xlabel("Seconds");
  ylabel("PSI");
  title("Irrigation Water Pressure Data for July 24, 25 (Vertical Lines are Hours)"); 
endfunction

function retval = addDay(days, data)
  sec_2_add = days * (60 * 60 * 24);
  data(:,1) = data(:,1) + sec_2_add;
  retval = data;
endfunction

function wakeup (message)
  printf ("\a%s\n", message);
endfunction



# ("C:\Users\gyea1\OneDrive\Documents\Projects\PressureSensor\data_2021_7_25.dat");
#plotData ("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data_2021_7_25.dat");
#plotData ("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data_2021_7_26.dat");
data1 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_7_29.dat", " ");
data2 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_7_30.dat", " ");
data3 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_7_31.dat", " ");
data4 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_8_1.dat", " ");
data5 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_8_2.dat", " ");
dataT = [ data1; addDay(1, data2); addDay(2,data3); addDay(3,data4); addDay(4,data5) ];
figure(1);
plotData(5, dataT);


data1_1 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_8_7.dat", " ");
data1_2 = dlmread("C:/Users/gyea1/OneDrive/Documents/Projects/PressureSensor/data2021/data_2021_7_30.dat", " ");

figure(2);
plotData(1,data1_1);
#printf ("data");