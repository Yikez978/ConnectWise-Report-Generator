import request
import report

import sys
curstdout = sys.stdout
sys.stdout = open('reportoutput.txt', 'w')

new_request = request.ReportRequestData(limit=0, start_date="01/01/2014", end_date="08/10/2014",
                                        company="Water-Jel Technologies LLC")
new_report = report.Report(new_request.document())

print "\n#### Generated URL ####"
print new_request.print_url()

print "\n#### Incident Count by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_service_type(), 12))

print "\n#### Incident Hours by Service Type ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_service_type()))

print "\n#### Incident Hours by Group ####"
report.comma_separated(report.top_incidents(new_report.incident_hours_by_group()))

print "\n#### Incident Count by Contact ####"
report.comma_separated(report.top_incidents(new_report.incident_count_by_contact(), 12))

print "\n#### Incident Count by Group ####"
print new_report.incident_count_by_group()

print "\n#### Open Incidents With Oldest ####"
print new_report.open_incidents_with_oldest()

print "\n#### Total Incidents ####"
print new_report.total_incidents()

print "\n#### Duplicate Accounts ####"
print report.comma_separated(report.top_incidents(new_report.users_submitting_duplicate_accounts(), 10))

sys.stdout = curstdout

print "output results to reportoutput.txt"
