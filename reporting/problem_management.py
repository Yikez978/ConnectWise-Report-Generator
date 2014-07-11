from reporting import cw_request, report

new_request = cw_request.ReportRequestData(limit=0, start_date='01/01/2014', end_date='06/13/2014')
new_report = report.Report(new_request.document())

print "\n#### Generated URL ####"
print new_request.url()


print "\n#### Incident Count by Contact and Type ####"
report.comma_separated(report.top_incidents(new_report.incident_type_count_by_contact(), 50))