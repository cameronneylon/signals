import json
import os.path
import datetime
import csv
import os

indir = 'output'
outdir = 'processed'

def write_csv(filepath, l, fieldnames):
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(l)

def open_and_process(filepath):
    l = []
    fieldnames = set(['source_id'])
    with open(filepath, 'rU') as f:
    	print filepath
        j = json.loads(f.read())
        
    for event in j['events']:
        d = {}
        d['source_id'] = event['source_id']
        months = [m for m in event['by_month']]
        for month in months:
            s = '%s-%02d' % ((month['year']), int(month['month']))
            fieldnames.add(s)
            d[s] = month['total']
            
        l.append(d)
    
    return l, fieldnames
        
for datafile in os.listdir(indir):
    inpath = os.path.join(indir, datafile)
    l, fieldnames  = open_and_process(inpath)
    fieldnames.remove('source_id')
    fields = ['source_id'] + (sorted(fieldnames))
    outpath = os.path.join(outdir, datafile)
    write_csv(outpath, l, fields)
    
    