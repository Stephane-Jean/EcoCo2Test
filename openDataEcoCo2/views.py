import requests
from .models import Record
from datetime import datetime
from django.http import HttpResponse

def retrieve(request):
	# Request q : date_heure>="2017-01-01T00:00:00Z"&date_heure<="2018-12-31T23:59:59Z"
	response = requests.get("https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-cons-def&q=date_heure%3E%3D%222017-01-01T00%3A00%3A00Z%22%26date_heure%3C%3D%222018-12-31T23%3A59%3A59Z%22&rows=20&start=0&sort=-date_heure&facet=nature&facet=date_heure")

	#  For testing purposes we only iterate on 10 rows of data
	n = 10
	
	# Check if the request for data was successfully received
	if response.status_code == 200:
		record = response.json()
		
		# If there is not enough data in the response, we want to stop before reaching 10 000
		nhits = record["nhits"]
		rows = record["parameters"]["rows"]
		if n > nhits :
			n = nhits
		if n > rows :
			n = rows
		
		for i in range(n) :
			fields = record["records"][i]["fields"]
			h = datetime.strptime(fields["heure"], "%H:%M")
			
			# Each half hour, the dataset from the API contains a value for each field
			if (h.minute == 0) or (h.minute == 30) :
				r = Record(recordid = record["records"][i]["recordid"],
				hydraulique_step_turbinage = fields["hydraulique_step_turbinage"],
				perimetre = fields["perimetre"],
				hydraulique_lacs = fields["hydraulique_lacs"],
				eolien = fields["eolien"],
				hydraulique = fields["hydraulique"],
				ech_comm_italie = fields["ech_comm_italie"],
				ech_comm_suisse = fields["ech_comm_suisse"],
				fioul_autres = fields["fioul_autres"],
				prevision_j1 = fields["prevision_j1"],
				ech_physiques = fields["ech_physiques"],
				ech_comm_allemagne_belgique = fields["ech_comm_allemagne_belgique"],
				solaire = fields["solaire"],
				nucleaire = fields["nucleaire"],
				gaz_tac = fields["gaz_tac"],
				pompage = fields["pompage"],
				prevision_j = fields["prevision_j"],
				fioul = fields["fioul"],
				gaz = fields["gaz"],
				nature = fields["nature"],
				gaz_cogen = fields["gaz_cogen"],
				gaz_autres = fields["gaz_autres"],
				fioul_cogen = fields["fioul_cogen"],
				ech_comm_espagne = fields["ech_comm_espagne"],
				bioenergies_biomasse = fields["bioenergies_biomasse"],
				date = fields["date"],
				bioenergies_dechets = fields["bioenergies_dechets"],
				taux_co2 = fields["taux_co2"],
				heure = h,
				hydraulique_fil_eau_eclusee = fields["hydraulique_fil_eau_eclusee"],
				bioenergies_biogaz = fields["bioenergies_biogaz"],
				fioul_tac = fields["fioul_tac"],
				gaz_ccg = fields["gaz_ccg"],
				date_heure = fields["date_heure"],
				charbon = fields["charbon"],
				bioenergies = fields["bioenergies"],
				ech_comm_angleterre = fields["ech_comm_angleterre"],
				consommation = fields["consommation"])
				
				r.save()
			# The 2 other points of data each hour have a lot less filled out
			else :
				r = Record(recordid = record["records"][i]["recordid"],
				prevision_j1 = fields["prevision_j1"],
				nature = fields["nature"],
				date_heure = fields["date_heure"],
				perimetre = fields["perimetre"],
				date = fields["date"],
				heure = h,
				prevision_j = fields["prevision_j"])
				
				r.save()
	else :
		raise Http404("Request was not successfully received")
	return HttpResponse("All the data from 2017 and 2018 has been retrieved")