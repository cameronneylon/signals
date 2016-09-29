import os
import json
import csv

indir = 'data/ncomms_data/data'
outdir = 'data/ncomms_processed'

def open_and_process(filepath):
    with open(filepath, 'rU') as f:
        print filepath
        j = json.loads(f.read())
        
    l = []
    dates = []

    # process views by date
    viewsbydate = j.get("counts").get("downloads").get("publisher").get("timeline")
    viewsbydate['source_id'] = 'views'
    l.append(viewsbydate)
    dates = [d for d in viewsbydate.iterkeys()]
    
    # process posts information to events by date
    posts = j.get('posts')
    if posts:
        for source in posts.iterkeys():
            p = {'source_id' : source}
            for post in posts[source]:
                timestamp = post.get('posted_on')
                date = timestamp.split('T')[0]
                if date not in dates:
                    dates.append(date)
                if p.get(date):
                    p[date] = p[date] + 1
                else:
                    p[date] = 1
            l.append(p)


    doi = j.get('citation').get('doi')        
    return l, dates, doi
        
def write_csv(filepath, l, fieldnames):
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(l)