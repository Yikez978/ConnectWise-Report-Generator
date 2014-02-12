import request
import report

new_request = request.ReportRequestData(limit=0, company="New Jersey Urology CBO-1", start_date='02/10/2014')
new_report = report.Report(new_request.request_document())

print new_request.print_url()

report.comma_separated(report.top_incidents(new_report.incident_count_by_service_type(), 10))
report.comma_separated(report.top_incidents(new_report.incident_hours_by_service_type()))

print "#### Incident hours ####"

report.comma_separated(report.top_incidents(new_report.incident_hours_by_group()))
report.comma_separated(report.top_incidents(new_report.incident_count_by_contact(), 10))

print new_report.incident_count_by_group()
print new_report.total_open_incidents()
print new_report.total_incidents()