import request
from bs4 import BeautifulSoup
from collections import defaultdict

class Report:
    def __init__(self, report_data):
        self.report = BeautifulSoup(report_data)

    def incident_count_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.servicetype:
                if item.servicesubtype.contents:
                    type_count[u": ".join(map(str,(item.servicetype.contents + item.servicesubtype.contents)))] += 1
                elif item.servicetype.contents:
                    type_count[u"".join(item.servicetype.contents)] += 1
        return type_count

    def incident_hours_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.servicetype:
                if item.servicesubtype.contents:
                    type_count[u": ".join(map(str,(item.servicetype.contents + item.servicesubtype.contents)))] += float("".join(item.hours_actual.contents))
                elif item.servicetype.contents:
                    type_count[u"".join(item.servicetype.contents)] += float("".join(item.hours_actual.contents))
        return type_count

    def incident_count_by_group(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.board_name:
                type_count[u"".join(item.board_name.contents)] += 1
        return type_count

    def incident_count_by_contact(self):
        type_count = defaultdict(int)
        for item in self.report.find_all():
            if item.contact_name:
                type_count[u"".join(item.contact_name.contents)] += 1
        return type_count

    def total_incidents(self):
        incidents = 0
        for item in self.report.find_all('row'):
            incidents += 1
        return incidents

def top_incidents(service_items, count):
    l = []
    for k in sorted(service_items, key=service_items.get, reverse=True):
        l.append((k, service_items[k]))
    return l[:count]

def comma_separated(items):
    for x,y in items:
        print x,", ", y

new_request = request.ReportRequestData(limit=100, company="New Jersey Urology CBO-1", start_date='02/03/2014')
report = Report(new_request.request_document())

print new_request.print_url()

comma_separated(top_incidents(report.incident_count_by_service_type(), 10))
comma_separated(top_incidents(report.incident_hours_by_service_type(), 10))
comma_separated(top_incidents(report.incident_count_by_contact(), 10))

print report.incident_count_by_group()

print report.total_incidents()

