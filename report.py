import request
from bs4 import BeautifulSoup
from collections import defaultdict

class Report:
    def __init__(self, report_data):
        self.report = BeautifulSoup(report_data)

    def incident_count_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.servicetype and not (item.board_name.contents == [u'Managed Service Alerts']):
                if item.servicesubtype.contents:
                    type_count[u": ".join(map(str,(item.servicetype.contents + item.servicesubtype.contents)))] += 1
                elif item.servicetype.contents:
                    type_count[u"".join(item.servicetype.contents)] += 1
        return type_count

    def incident_hours_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.servicetype and not (item.board_name.contents == [u'Managed Service Alerts']):
                if item.servicesubtype.contents:
                    type_count[u": ".join(map(str,(item.servicetype.contents + item.servicesubtype.contents)))] += float("".join(item.hours_actual.contents))
                elif item.servicetype.contents:
                    type_count[u"".join(item.servicetype.contents)] += float("".join(item.hours_actual.contents))
        return type_count

    # def incident_hours_by_technician(self):
    #     type_count = defaultdict(int)
    #     for item in self.report.find_all():
    #         if item.servicetype:
    #             if item.servicesubtype.contents:
    #                 type_count[u": ".join(map(str,(item.servicetype.contents + item.servicesubtype.contents)))] += float("".join(item.hours_actual.contents))
    #             elif item.servicetype.contents:
    #                 type_count[u"".join(item.servicetype.contents)] += float("".join(item.hours_actual.contents))
    #     return type_count

    def incident_hours_by_group(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.board_name.contents)] += float("".join(item.hours_actual.contents))
        return type_count

    def incident_count_by_group(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.board_name.contents)] += 1
        return type_count

    def incident_count_by_contact(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.contact_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.contact_name.contents)] += 1
        return type_count

    def total_incidents(self):
        incidents = 0
        for item in self.report.find_all('row'):
            incidents += 1
        return "Total Incidents: ", incidents

    def total_open_incidents(self):
        open_calls = 0
        oldest_open = {"summary":"","date":""}
        for item in self.report.find_all('row'):
            if item.closed_flag.contents == [u"False"] and not (item.board_name.contents == [u'Managed Service Alerts']):
                open_calls += 1
                if item.date_entered.contents < oldest_open['date']:
                    print item.board_name.contents
                    oldest_open["summary"], oldest_open["date"] = item.summary.contents, item.date_entered.contents[0]
        return "Open Incidents: ", open_calls, oldest_open

def top_incidents(service_items, count=None):
    l = []
    for k in sorted(service_items, key=service_items.get, reverse=True):
        l.append((k, service_items[k]))
    if count:
        return l[:count]
    return l

def comma_separated(items):
    for x,y in items:
        print x,", ", y

new_request = request.ReportRequestData(limit=0, company="New Jersey Urology CBO-1", start_date='02/10/2014')
report = Report(new_request.request_document())

print new_request.print_url()

comma_separated(top_incidents(report.incident_count_by_service_type(), 10))
comma_separated(top_incidents(report.incident_hours_by_service_type()))

print "#### Incident hours ####"

comma_separated(top_incidents(report.incident_hours_by_group()))
comma_separated(top_incidents(report.incident_count_by_contact(), 10))

print report.incident_count_by_group()
print report.total_open_incidents()

print report.total_incidents()

