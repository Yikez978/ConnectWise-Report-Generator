from reporting import request, report

new_request = request.ReportRequestData(limit=0, start_date='05/25/2014', end_date='05/31/2014')
new_report = report.Report(new_request.document())

print "\n#### Generated URL ####"
print new_request.url()

print "\n#### Incident Count by Day ####"
print report.comma_separated(report.top_incidents(new_report.incident_count_by_day()))

print "\n#### Incident Count by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_service_type(), 10))

print "\n#### Incident Hours by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_service_type()))

print "\n#### Incident Hours by Group ####"
print report.top_incidents(new_report.incident_hours_by_group())

print "\n#### Incident Count by Contact ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_contact(), 10))

print "\n#### Incident Hours by Company ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_company()))

print "\n#### Incident Count by Company ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_company()))

print "\n#### Incident Count by Group ####"
print new_report.incident_count_by_group()\

print "\n#### Incidents Closed by Techs ####"
print new_report.tech_number_closed()

print "\n#### Total Incidents ####"
print new_report.total_incidents()

print "\n#### Incident Count by Contact and Type ####"
print report.top_incidents(new_report.incident_type_count_by_contact(), 50)