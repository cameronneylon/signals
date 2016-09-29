import numpy as np
import os
from ncomms_utils import open_and_process, write_csv, indir, outdir


doi_list = []
fieldnames = ['doi', 'views, total', 'views, first month', 'views, first week', 'views, first day']
for datafile in os.listdir(indir):
    inpath = os.path.join(indir, datafile)
    l, dates, doi  = open_and_process(inpath)
    dates.sort()

    if len(l) > 1:
        continue
        
    cumulative = np.cumsum([l[0].get(date) for date in dates[0:-1]])
    views_first_month = cumulative[30]
    views_first_week = cumulative[7]
    views_first_day = cumulative[0]
    total_views = cumulative[-1]
    
    d = {'doi' : doi,
         'views, total' : total_views,
         'views, first month' : views_first_month,
         'views, first week' : views_first_week,
         'views, first day' : views_first_day
        }
        
    doi_list.append(d)
    
outpath = os.path.join(outdir, 'articles_with_no_events.csv')
write_csv(outpath, doi_list, fieldnames)
        
    