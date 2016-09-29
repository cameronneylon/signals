import numpy as np
from scipy.optimize import curve_fit
import os
import datetime
from ncomms_utils import open_and_process, write_csv, indir, outdir
import matplotlib.pyplot as plt


def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c
    
def linear(x, a, b):
    return a * x + b

fit_list = []
fieldnames = ['doi', 'exponential_a', 'exponential_b', 'exponential_c', 'exponential_r2',
                     'linear_a', 'linear_b', 'linear_r2', 'mean_ss', 'std_dev_ss']


for datafile in os.listdir(indir):
    inpath = os.path.join(indir, datafile)
    l, dates, doi  = open_and_process(inpath)
    l[0].pop('source_id')
    dates.sort()
    d0 = datetime.datetime.strptime(dates[0], '%Y-%m-%d')
    ydata = []
    xdata = []
    for d in dates[0:-1]:
        if l[0].get(d):
            ydata.append(l[0].get(d))
            xdata.append((datetime.datetime.strptime(d,'%Y-%m-%d') - d0).days)
 
    xdata = np.array(xdata)
    ydata = np.array(ydata)

    try:    
        fit = { 'doi' : doi}
        popt, pcov = curve_fit(linear, xdata[30:], ydata[30:])
        r2 = np.sum((linear(xdata, *popt) - ydata)**2)/np.sum((ydata - np.mean(ydata))**2)

        fit['linear_a'] = popt[0]
        fit['linear_b'] = popt[1]
        fit['linear_r2'] = r2
        fit['mean_ss'] = np.mean(ydata[30:])
        fit['std_dev_ss'] = np.std(ydata[30:])
        
        popt, pcov = curve_fit(exponential, xdata, ydata)
        r2 = np.sum((exponential(xdata, *popt) - ydata)**2)/np.sum((ydata - np.mean(ydata))**2)

        fit['exponential_a'] = popt[0]
        fit['exponential_b'] = popt[1]
        fit['exponential_c'] = popt[2]
        fit['exponential_r2'] = r2
              
#         plt.plot(xdata+1, ydata, 'ro')
#         plt.xscale('log')
#         fitdata = [exponential(x, popt[0], popt[1], popt[2]) for x in xdata]
#         plt.plot(xdata+1, fitdata, '-')
#         plt.title(doi + 'r2=' + str(r2))
#         
#         plotfile = os.path.join(outdir, 'plots', doi.replace('/', '_') + '.png')
#         plt.savefig(plotfile)
#         plt.clf()
        
    except RuntimeError:
        fit = { 'doi' : doi,
                'exponential_r2' : 'Fit failed'
              }
    fit_list.append(fit)
     
outpath = os.path.join(outdir, 'exponential_fits.csv')
write_csv(outpath, fit_list, fieldnames)
        
    