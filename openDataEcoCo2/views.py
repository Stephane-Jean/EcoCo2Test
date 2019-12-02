import requests
from django.http import HttpResponse

def retrieve(request):
	# Request q : date_heure>="2017-01-01T00:00:00Z"&date_heure<="2018-12-31T23:59:59Z"
	response = requests.get("https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-cons-def&q=date_heure%3E%3D%222017-01-01T00%3A00%3A00Z%22%26date_heure%3C%3D%222018-12-31T23%3A59%3A59Z%22&rows=20&start=0&sort=-date_heure&facet=nature&facet=date_heure")

	if response.status_code == 200:
		return HttpResponse("All the data from 2017 and 2018 has been retrieved")
	else :
		raise Http404("Request was not succesfully received")

# Create your views here.
