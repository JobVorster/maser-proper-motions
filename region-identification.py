#(*******************************************************
#PROGRAM NAME - region-identification

#PROGRAMMER - Job Vorster - 2021/02/03

#USAGE - Compile using normal python terminal imput python(3) region-identification.py
#The program assumes you have a folder data containing the maser spot information in the format
#with the columns RA DEC VLSR FLUX DFLUX and separated by commas. The utils code should also be in the 
#same directory.


#DATE - Started 2021/02/03
       #Version 0.5.0 2021/02/03

#BUGS - Zoom mode does not work as planned. Interactions between different modes not yet well understood.

#DESCRIPTION - Program to easily identify regions with maser proper motion. Opens an interactive plot, which you can
#zoom in, and save data points into a text file, this text file is then used by the relative_pm.py (TODO make this code) python code 
#to calculate the proper motions for the maser spots in the regions specified. The program has the following features:
#- Makes interactive plots of all epochs measured using normal python interactive plot.
#- Pressing "m" puts you into "remove mode", which saves a box every time you click twice. With the box's corners being your two 
#click positions. All the maser spots within will be processed as a single maser feature in relative_pm.py. So make sure to keep the boxes the right size
#If you make the boxes two big, you will have huge unphysical proper motions, that might be flagged. If the boxes are two small, you might miss multi epochs of the
#same maser, which will let you not detect its proper motions.
#- Pressing "," lets you go into a "special zoom mode" this zoom mode changes the colorbar every time you zoom in. This makes it much easier to identify masers of the 
#same maser feature. When using "remove mode", try to box around masers with the same Vlsr. TODO Fix bugs with zoom mode, where it stops updating vlsr in certain circumstances.

#*******************************************************)


#TODO add inputs that specifies the input file directory 








#******************************************************************

#        Import all libraries

#*******************************************************************
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#Note the utils file should be in your directory.
from utils import extract_from_df,isolate
from glob import glob
from itertools import chain 
from matplotlib import patches as pat
import os


#*******************************************************************

#        Define all local functions.

#*******************************************************************


def onclick(event):
    '''Event handler for mouse clicks - Used for zooming in and out, and to choose regions for proper motion calculation.'''
    global click_no, saved_coords, RA,DEC,VLSR,FLUX,DFLUX, prev_click_x, prev_click_y,fig, mode1, o_no,zoom_coords,plot_boxes,plotboxnum,data_boxes,databoxnum
    
    #If special zoom mode is turned on.
    if dot_no == 1:
        zoom_coords = [[],[]]
        zoom_coords[0].append(event.xdata)
        zoom_coords[1].append(event.ydata)
        
    #Zooming must be turned off to mark regions to save.
    
    #prev_click arrays store two click values, that later gets saved.
    if mode1 == 'remove' and o_no == 0 and dot_no == 0:
        if click_no == 0:
            click_no = 1
            prev_click_x.append(event.xdata)
            prev_click_y.append(event.ydata)
        else:
            click_no = 0
            prev_click_x.append(event.xdata)
            prev_click_y.append(event.ydata)
            prev_click_x.sort()
            prev_click_y.sort()
            saved_coords.append([prev_click_x,prev_click_y])
            INDS = []
            for i in range(0,len(RA)):
                inds = isolate(RA[i],DEC[i],prev_click_x,prev_click_y)
                INDS.append(inds)
                del inds
            if len(INDS)!=0:
                print("Saved  box [[x0,x1],[y0,y1]:\n[[%.4f,%.4f],[%.4f,%.4f]]"%(prev_click_x[0],prev_click_x[1],prev_click_y[0],prev_click_y[1]))
                plot_boxes.append([prev_click_x[0],prev_click_x[1],prev_click_y[0],prev_click_y[1]])
                data_boxes.append([prev_click_x[0],prev_click_x[1],prev_click_y[0],prev_click_y[1]])
                plotboxnum += 1
                databoxnum += 1
            prev_click_x = []
            prev_click_y = []


def onkey_press(event):
    '''Event handler - For key presses. The options (other than the normal interactive python plot options - https://matplotlib.org/3.1.1/users/navigation_toolbar.html)
    available: 
    - o key - This is the normal zoom option for the plots.
    - , key - This is a special zoom mode, that restricts the clim for the colourbar to the masers on the screen, useful for identifying masers that might be associated over 
    different epochs. After pressing the key, a message in the terminal indicates that "Zoom mode is now on", then you can zoom in using a mouse drag. Note that the clim updates sometimes stop working.
    - m key - This puts the plots into remove mode TODO (Update name), this mode one specifies a box from which proper motions will be calculated. Please note that the box should only 
    contain masers that are suspected to be from the same maser feature. If you make too big boxes, the proper motions might be flagged further down the code. After pressing the key, a terminal message "Remove mode is now on" signifies that you can save regions by clicking at two corners a box containing the masers in question. When you turn it off, it saves the regions into a textfile TODO (Specify text file) that will be piped into relative_pm.py.
    - r key - Resets the plot, keeping all maser position boxes saved and on the screen.'''
    global mode1,o_no,dot_no,data_boxes,databoxnum
    if event.key == 'o':
        if o_no == 0:
            o_no = 1
        else:
            o_no = 0
    if event.key == ',':
        if dot_no ==0:
            print("Zoom mode is now on")
            dot_no = 1
        else:
            print("Zoom mode is now off")
            dot_no = 0
    if event.key == 'r':
        plt.clf()
        all_scatter(RA,DEC,VLSR)
        plt.draw()
    if event.key == 'm':
        if mode1 != 'remove':
            print('Remove mode is now on')
            mode1 = 'remove'
        else:
            print("Remove mode is now off")
            plt.clf()
            all_scatter(RA,DEC,VLSR)
            plt.draw()
            print("Saving to data file")
#TODO add option to start a new parameter file or use an old one.
            if len(data_boxes)!= 0:
                f = open("pm_pars.txt", "a")
                if databoxnum == 1:
                    f.write(str(data_boxes) + '\n')
                else:
                    for i in range(0,databoxnum):
                        f.write(str(data_boxes[i])+'\n')
                f.close()
                data_boxes =[]
                databoxnum = 0
            mode1 = 'none'
            
def onrelease(event):
    '''Event handler for mouse key releases. Only use at this moment is with the special zoom mode. '''
    global RA,DEC,VLSR,zoom_coords,dot_no
    if dot_no == 1:
        zoom_coords[0].append(event.xdata)
        zoom_coords[1].append(event.ydata)
        zoom_coords[0].sort() 
        zoom_coords[1].sort()
        plt.clf()
        all_scatter(RA,DEC,VLSR,zoom_coords)
        plt.draw()
        

def all_scatter(RA,DEC,VLSR,lims = []):
    '''Function for making scatter plots - '''
    global plot_boxes,plotboxnum
    #Initializes the plot, plotsize is the x-size of the plot. 
    plotsize =7
    aspect_ratio = 4
    x_size = plotsize
    figsize = (x_size,x_size*aspect_ratio)
    newparams = {'figure.figsize': figsize, 'axes.grid': False,
                'lines.linewidth': 1.5, 'lines.markersize': 10,
                'font.size': 14}
    plt.rcParams.update(newparams)
    #Dates of the different observations in decimal dates. TODO (Make this an automatic input).
    epdates = ["%.2f"%(2014+262.0/365.),"%.2f"%(2014 + 329./365.),"%.2f"%(2015 + 31./365.),
            "%.2f"%(2015 + 104./365.),"%.2f"%(2015+322./365.),"%.2f"%(2016+40./365.),"%.2f"%(2016+71./365.)]
    clims = [-64.0,0.632865]
    INDS = []
    FV =[]
    CLIMS = []
    for i in range(0,len(RA)):
        #This code only runs when the image is zoomed in by the special zoom mode.
        if len(lims) != 0:
            inds = isolate(RA[i],DEC[i],lims[0],lims[1])
            INDS.append(inds)
            FV.append(VLSR[i])
            if len(inds) != 0:
                FV[i] = np.array(FV[i])[inds]
    if len(lims) != 0:
        #This line collapses an array containing all the vlsr values in the zoomed plot. To use the min and max for the clim.
        clims = [min(list(chain.from_iterable(FV))),max(list(chain.from_iterable(FV)))]            
    for i in range(0,len(RA)):
        if len(lims) !=0:
            #Plots all the epochs, this case is for when special zoomed mode is used, so only the data points in the zoomed box is plotted.
            plt.scatter(np.array(RA[i])[INDS[i]],np.array(DEC[i])[INDS[i]],c = np.array(VLSR[i])[INDS[i]],marker = "$%d$"%(i+1),cmap = 'jet',label = epdates[i])
            #Remember to specify the clim after every plot, and to keep it the same.
            plt.clim(clims)
        else:
            plt.scatter(RA[i],DEC[i],c = VLSR[i],marker = "$%d$"%(i+1),cmap = 'jet',label = epdates[i])
            plt.clim(clims)
    if len(plot_boxes) != 0:
        ax = plt.gca()
        for i in range(0,plotboxnum):
            #Plots a rectangle at boxes which the user has specified proper motion to be calculated
            p =pat.Rectangle((plot_boxes[i][0],plot_boxes[i][2]),plot_boxes[i][1] - plot_boxes[i][0],
                            plot_boxes[i][3]-plot_boxes[i][2],fill = False,linestyle = 'dashed',color = 'green')
            ax.add_patch(p)
    #To not let the plot invert every time this function is called. TODO (see if this works).
    if not plt.gca().xaxis_inverted():
        plt.gca().invert_xaxis()
    plt.colorbar(label = r"$V_{LSR}$ (km s$^{-1}$)")
    plt.legend()
    if len(lims) != 0:
        plt.xlim(lims[0])
        plt.ylim(lims[1])
    plt.xlabel('RA Offset (arcseconds)')
    plt.ylabel("Dec Offset (arcseconds)")
    plt.gca().autoscale(False)


#*******************************************************************

#        Code main body

#*******************************************************************    

#Note the capitalized versions of list names, these lists are 2D, containing all data of their type. For example, RA contains [ra1,ra2,....] 
RA = []
DEC = []
VLSR = []
FLUX = []
DFLUX = []
#The columns containing the data files in the input.
cols = ['RA','DEC','VLSR','FLUX','DFLUX']
plot_boxes = []
data_boxes = []
plotboxnum = 0
databoxnum = 0

#Controls of whether different keys have been pressed.
o_no = 0 #whether o has been pressed
click_no = 0 #whether the mouse click has been used.
dot_no = 0 #whether comma has been used TODO (Fix this).
prev_click_x = []
prev_click_y = []
saved_coords = []
zoom_coords  = [[],[]]
mode1 = 'none' #The current mode for the plots. TODO (Put some sort of in plot indicator of the mode).

#Reads data from text files into multidimensional arrays.
#Only need to specify the relative path to the data files folder. TODO (Make the data file location an input).
for name in glob("data/*"):
    df = pd.read_csv(name,sep = ',')
    ra,dec,vlsr,flux,dflux = extract_from_df(df,cols)
    RA.append(ra)
    DEC.append(dec)
    VLSR.append(vlsr)
    FLUX.append(flux)
    DFLUX.append(dflux)
    


all_scatter(RA,DEC,VLSR)
fig = plt.gcf()
#Links the event handlers to the functions above.
cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect('button_release_event',onrelease)
cid3 = fig.canvas.mpl_connect('key_press_event',onkey_press)
plt.show()
