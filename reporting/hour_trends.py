from reporting import cw_request, report
from datetime import date, datetime, timedelta

def datespan(startDate, endDate, delta=timedelta(days=1)):
    currentDate = startDate
    while currentDate < endDate:
        yield currentDate
        currentDate += delta

for date_point in datespan(date(2014, 02, 01), date(2014, 06, 21), delta=timedelta(days=30)):
    start_date = date_point
    end_date = date_point + timedelta(days=30)
    start_date = str(start_date).split("-")
    end_date = str(end_date).split("-")
    start_date = "/".join((start_date[1],start_date[2],start_date[0]))
    end_date = "/".join((end_date[1],end_date[2],end_date[0]))
    new_request = cw_request.ReportRequestData(limit=0, report="Service", company="New Jersey Urology CBO-1",
                                        start_date=start_date, end_date=end_date)
    new_report = report.Report(new_request.document())
    print "\n#### Incident Hours by Group ####"
    print "For dates: " + start_date + " through: " + end_date
    print new_report.incident_hours_by_group()
