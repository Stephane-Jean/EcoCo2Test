import requests
import csv
import json
from .models import Record
from datetime import datetime
from django.shortcuts import HttpResponse, Http404, render

def retrieve(request):
	# We will iterate on 9985 rows of data
	# It corresponds to 104 days of data + the first Record of the next day
	# The bigger the batch we use the faster the treatment gets and 10k is the maximum number of rows we can retrieve at once
	n_init = 9985
	n = n_init
	nhits = n_init
	rows = n_init
	
	# Total number of retrieved Records
	nTot = 0
	
	# We will retrieve all the record from 2017 and 2018
	# We start on 2017/01/01 end on 2018/12/31
	startDate = "2017-01-01"
	date = startDate
	endDate = "2018-12-31"
	
	# Test if there is anything wrong with the request
	response = requests.get("https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-cons-def&q=date_heure%3E%3D%22"+startDate+"T00%3A00%3A00Z%22%26date_heure%3C%3D%22"+endDate+"T23%3A59%3A59Z%22&rows="+str(rows)+"&sort=-date_heure&facet=date_heure")
	if response.status_code == 200:
		record = response.json()
		if record["nhits"] == 0 :
			raise Http404("There are no data for those starting and ending dates")
	else :
		raise Http404("Request was not successfully received")
	
	# At the last step of the data retrieval there will be less than 9985 Records to retrieve
	while nhits >= n_init :
		# Request q : date_heure>="2017-01-01T00:00:00Z"&date_heure<="2018-12-31T23:59:59Z"
		response = requests.get("https://opendata.reseaux-energies.fr/api/records/1.0/search/?dataset=eco2mix-national-cons-def&q=date_heure%3E%3D%22"+date+"T00%3A00%3A00Z%22%26date_heure%3C%3D%22"+endDate+"T23%3A59%3A59Z%22&rows="+str(rows)+"&sort=-date_heure&facet=date_heure")
		
		# Check if the request for data was successfully received
		if response.status_code == 200:
			record = response.json()
			
			# If there is not enough data in the response, we want to stop before reaching n
			nhits = record["nhits"]
			rows = record["parameters"]["rows"]
			if n > nhits :
				n = nhits
			if n > rows :
				n = rows
			
			for i in range(n) :
				fields = record["records"][i]["fields"]
				h = datetime.strptime(fields["heure"], "%H:%M")
				# Each half hour, the dataset from the API contains a value for the CO2 rate
				if (h.minute == 0) or (h.minute == 30) :
					r = Record(recordid = record["records"][i]["recordid"],
					date_heure = fields["date_heure"],
					date = fields["date"],
					heure = h,
					taux_co2 = fields["taux_co2"])
					
					r.save()
				# The rest of the time the dataset is missing the CO2 rate
				else :
					# We will save an entry into the database nevertheless
					r = Record(recordid = record["records"][i]["recordid"],
					date_heure = fields["date_heure"],
					date = fields["date"],
					heure = h)
					
					r.save()
			# The last row will be the first row of the next batch, we don't want to count it twice
			nTot += (n-1)
			date = record["records"][n-1]["fields"]["date"]
		else :
			raise Http404("Request was not successfully received")
	context = { 'nTot':  str(nTot+1), 'startDate':  str(startDate) , 'date':  str(date), 'nhits':  str(nhits), 'csv_url':  '/openDataEcoCo2/csv_url/' }
	return render(request, 'openDataEcoCo2/retrieve.html', context)
	
def csvGeneration(request):
	# Create the HttpResponse object with the appropriate CSV header.
	recordsFile = HttpResponse(content_type='text/csv')
	recordsFile['Content-Disposition'] = 'attachment; filename="OpenDataEcoCO2.csv"'
	writer = csv.writer(recordsFile)
	# First row with column names
	writer.writerow(["Date", "Heure", "Taux de CO2 (g/kWh)"])
	
	entries = Record.objects.all().order_by('date','heure')
	for e in entries:
		# Each half hour, the dataset from the API contains a value for the CO2 rate
		if (e.heure.minute == 0) or (e.heure.minute == 30) :
			writer.writerow([e.date, e.heure, e.taux_co2])
			# The rest of the time the dataset is missing the CO2 rate
		else :
			# We won't save an entry into the database, but we will add a line to the csv file
			# to be able to interpolate the mising data latter on
			writer.writerow([e.date, e.heure])
	
	return recordsFile