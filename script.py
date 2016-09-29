import requests
import json
import os.path


def save_json(doi, j, dir):
	name = doi.split('.')[3]+'_events'
	with open(os.path.join(dir,name), 'w') as f:
		f.write(json.dumps(j))

def get_events(doi, **kwargs):
	url = "http://alm.plos.org/api/works/"
	if url:
		resp = requests.get("%s%s/events" % (url, doi))
		resp.raise_for_status()

		j = resp.json()
		return j

outdir = 'data/output'
doifile = 'doilist.txt'
dois = []

with open(doifile, 'rU') as f:
	for line in f:
		dois.append(line.rstrip('\n'))

for doi in dois:
	j = get_events(doi)
	save_json(doi, j, outdir)



