import requests
from .models import Record
from django.http import HttpResponse

def retrieve(request):
	# Request q : date_heure>="2017-01-01T00:00:00Z"&date_heure<="2018-12-31T23:59:59Z"
	response = requests.get("https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-cons-def&q=date_heure%3E%3D%222017-01-01T00%3A00%3A00Z%22%26date_heure%3C%3D%222018-12-31T23%3A59%3A59Z%22&rows=20&start=0&sort=-date_heure&facet=nature&facet=date_heure")

	#  For testing purposes we only iterate on 10 rows of data
	n = 10
	
	if response.status_code == 200:
		record = response.json()
		
		# If there is not enough data in the response, we want to stop before reaching 10 000
		nhits = record["nhits"]
		rows = record["parameters"]["rows"]
		if n > nhits :
			n = nhits
		if n > rows :
			n = rows
		
		for i in range(0, n, 2) :
			fields = record["records"][i+1]["fields"]
			
			r2 = Record(recordid = record["records"][i+1]["recordid"],
			prevision_j1 = fields["prevision_j1"],
			nature = fields["nature"],
			date_heure = fields["date_heure"],
			perimetre = fields["perimetre"],
			date = fields["date"],
			heure = fields["heure"],
			prevision_j = fields["prevision_j"])
			
			r2.save()
	else :
		raise Http404("Request was not succesfully received")
	return HttpResponse("All the from 2017 and 2018 has been retrieved")