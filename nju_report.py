import request
import report

start = raw_input("Please enter start date (MM/DD/YYYY): ")
end = raw_input("Please enter end date (MM/DD/YYYY): ")

new_request = request.ReportRequestData(limit=0, company="New Jersey Urology CBO-1",
                                        start_date=start, end_date=end)
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

print "\n#### Incident Count by Group ####"
print new_report.incident_count_by_group()

print "\n#### Open Incidents With Oldest ####"
print new_report.open_incidents_with_oldest()

print "\n#### Total Incidents ####"
print new_report.total_incidents()

print "\n#### Duplicate Accounts ####"
print report.comma_separated(report.top_incidents(new_report.users_submitting_duplicate_accounts(), 10))