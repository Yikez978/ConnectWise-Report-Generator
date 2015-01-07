import web.reporting.cw_request as request
import web.reporting.report as report

company_list = ['Application Consulting Group', 'Brian Trematore Plumbing & Heating, Inc.',
                'Business Machine Technologies', 'Rosica Strategic Public Relations', 'Gaccione Pomaco P.C.',
                'James Alexander Corporation', 'Smolin, Lupin & Co., P.A.', 'Robert A. Goodman & Co., LLP',
                'Bobcat of North Jersey', 'Canyon Capital Corp.', 'Coastal Financial Group Inc.',
                'Dugan Colthart & Zoch', 'Edgewood Consulting Group', 'Energy for America',
                'Freeman Hughes Freeman Law', 'Gabrellian Associates', 'Gramkow Carnevale Seifert, Inc.',
                'Let it Grow',  'Sherwood Learning Solutions, Inc.', 'Kolinsky Wealth Management, LLC',
                'MG America', 'Uniglobe Travel Partners', 'Jay-Hill Repairs', 'Marlyn Insurance',
                'NJ Family Planning League', 'Phoenix Aromas & Essential Oils', 'RC Andersen, LLC',
                'Construction Risk Partners NJ Office', 'Water-Jel Technologies LLC',
                'Halsted Corp', 'C-K Air Conditioning, Inc.', 'Dialectic Distribution, LLC', 'STEVEN R. LEHR, ESQ.',]

#new_request = request.ReportRequestData(limit=0, start_date='01/01/2014', end_date='04/30/2014', company='Halsted Corp')
#new_report = report.Report(new_request.document())
#
#print('Backup Tickets: ', new_report.incident_count_by_service_type()['Server: Backup'])
#print('Hours: ', new_report.incident_hours_by_service_type()['Server: Backup'])

company_and_list = []
for company in company_list:
    new_request = request.ReportRequestData(limit=0, start_date='01/01/2014', end_date='12/31/2014', company=company)
    new_report = report.Report(new_request.document())
    company_and_list.append((company, new_report.incident_count_by_service_type()['Server: Backup'] + new_report.incident_count_by_service_type()['Network: Backup'], new_report.incident_hours_by_service_type()['Server: Backup'] + new_report.incident_count_by_service_type()['Network: Backup']))

#print(company_and_list)
_sorted = sorted(company_and_list, key=lambda tup: tup[2], reverse = True)
for item in _sorted:
    print(item[0])
    print("Incidents: ", item[1])
    print("Hours: ", item[2])
    print("\n")

#sorted_list = []
#
##print new_report.company_hours_breakdown()
#for company, tech_map in new_report.company_hours_breakdown().items():
#    company_data = []
#    total_hours = 0
#    tech_hours = []
#    #print tech_map
#    if check_contains(tech_map.keys(), tech_list):
#        for tech, hours in tech_map.items():
#            if tech in tech_list:
#                tech_hours.append((tech, hours))
#                total_hours += hours
#        sorted_tech_hours = sorted(tech_hours, key=lambda tup: tup[1], reverse = True)
#        company_data.append((company.split(",")[0].title(), total_hours))
#        company_time.append((company.split(",")[0].title(), total_hours))
#        company_data += sorted_tech_hours
#        sorted_list.append(company_data)
#_sorted = sorted(sorted_list, key=lambda tup: tup[0][1], reverse = True)
#company_time = sorted(company_time, key=lambda tup: tup[1], reverse = True)