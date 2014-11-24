
import request
import report

company_list = ['Application Consulting Group', 'Brian Trematore Plumbing & Heating, Inc.',
                'Bobcat of North Jersey', 'Canyon Capital Corp.', 'Coastal Financial Group Inc.',
                'Dugan Colthart & Zoch', 'Edgewood Consulting Group', 'Energy for America',
                'Freeman Hughes Freeman Law', 'Gabrellian Associates', 'Gramkow Carnevale Seifert, Inc.',
                'Let it Grow',  'Sherwood Learning Solutions, Inc.', 'Kolinsky Wealth Management, LLC',
                'MG America', 'Uniglobe Travel Partners', 'Jay-Hill Repairs', 'Marlyn Insurance',
                'NJ Family Planning League', 'Phoenix Aromas & Essential Oils', 'RC Andersen, LLC',
                'Construction Risk Partners NJ Office', 'Water-Jel Technologies LLC',
                'Halsted Corp', 'C-K Air Conditioning, Inc.',]

for company in company_list:
    new_request = request.ReportRequestData(limit=0, start_date='01/01/2014', end_date='09/15/2014', company=company)
    new_report = report.Report(new_request.document())
    print company
    #print "\n#### Generated URL ####\n"
    #print new_request.print_url()
    print "\n\n#### Incident Hours by Service Type ####\n"
    print report.comma_separated(report.top_incidents(new_report.incident_hours_by_service_type()))
    print "\n\n"