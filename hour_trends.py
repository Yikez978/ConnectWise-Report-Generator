from datetime import date, timedelta

import web.reporting.report as report
import web.reporting.cw_request as request

def check_contains(listOne, listTwo):
    for item in listOne:
        if item in listTwo:
            return True
    return False

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta


#for date_point in datespan(date(2014, 11, 16), date(2014, 11, 22), delta=timedelta(days=7)):
#    start_date = date_point
#    end_date = date_point + timedelta(days=7)
#    start_date = str(start_date).split("-")
#    end_date = str(end_date).split("-")
#    start_date = "/".join((start_date[1],start_date[2],start_date[0]))
#    end_date = "/".join((end_date[1],end_date[2],end_date[0]))
start_date = "12/28/2014"
end_date="01/03/2015"
new_request = request.ReportRequestData(report="Time", limit=0, start_date=start_date, end_date=end_date)

print(new_request.url())

new_report = report.Report(new_request.document())
tech_list = ["rodonnell", "lverone", "jhanna", "rgatollari", "vvieira", "dwilliams", "ykovalerchik", "mdanihy",
             "abyrnes", "cdelgaudio", "lmartinez"]

print("Week of", start_date)
sorted_list = []
company_time = []
#print new_report.company_hours_breakdown()
for company, tech_map in new_report.company_hours_breakdown().items():
    company_data = []
    total_hours = 0
    tech_hours = []
    #print tech_map
    if check_contains(tech_map.keys(), tech_list):
        for tech, hours in tech_map.items():
            if tech in tech_list:
                tech_hours.append((tech, hours))
                total_hours += hours
        sorted_tech_hours = sorted(tech_hours, key=lambda tup: tup[1], reverse = True)
        company_data.append((company.split(",")[0].title(), total_hours))
        company_time.append((company.split(",")[0].title(), total_hours))
        company_data += sorted_tech_hours
        sorted_list.append(company_data)
_sorted = sorted(sorted_list, key=lambda tup: tup[0][1], reverse = True)
company_time = sorted(company_time, key=lambda tup: tup[1], reverse = True)
#print _sorted

for group in _sorted:
    for tuple in group:
        print(tuple[0], ",", tuple[1])
    print("\n")

for tuple in company_time:
    print(tuple[0], ",", tuple[1])

#print start_date + " "  + str(new_report.incident_hours_by_group()["Service Desk"]) + " " + str(new_report.incident_hours_by_group()["NJU-GreenWay"])

