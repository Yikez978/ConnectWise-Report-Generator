import request
import report

new_request = request.ReportRequestData(limit=0, start_date='03/09/2014', end_date='03/15/2014')
new_report = report.Report(new_request.document())

print "\n#### Generated URL ####"
print new_request.print_url()

print "\n#### Incident Count by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_service_type(), 10))

print "\n#### Incident Hours by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_service_type()))

print "\n#### Incident Hours by Group ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_group()))

print "\n#### Incident Count by Contact ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_contact(), 10))

print "\n#### Incident Hours by Company ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_company()))

print "\n#### Incident Count by Company ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_company(), 10))

print "\n#### Incident Count by Group ####"
print new_report.incident_count_by_group()\

print "\n#### Incidents Closed by Techs ####"
print new_report.tech_number_closed()

print "\n#### Total Incidents ####"
print new_report.total_incidents()