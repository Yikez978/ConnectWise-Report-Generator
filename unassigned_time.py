import report
import request

new_request = request.ReportRequestData(report="Time", limit=0, start_date="10/01/2014", end_date="10/31/2014")
print new_request.print_url()
new_report = report.Report(new_request.document())
print new_report.tech_hours_unassigned()