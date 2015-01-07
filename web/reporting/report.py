import datetime
from collections import defaultdict

from bs4 import BeautifulSoup, SoupStrainer

class Report:
    def __init__(self, report_data):
        self.report = BeautifulSoup(report_data)

    def incident_count_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            service_item = []
            if item.servicetype and item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                #if item.servicesubtypeitem.contents:
                    #service_item.append(item.servicesubtypeitem.contents[0])
                if item.servicesubtype.contents:
                    service_item.append(item.servicesubtype.contents[0])
                if item.servicetype.contents:
                    service_item.append(item.servicetype.contents[0])
                type_count[u": ".join(service_item[::-1])] += 1
        return type_count

    def incident_hours_by_service_type(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            service_item = []
            if item.servicetype and item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                #if item.servicesubtypeitem.contents:
                    #service_item.append(item.servicesubtypeitem.contents[0])
                if item.servicesubtype.contents:
                    service_item.append(item.servicesubtype.contents[0])
                if item.servicetype.contents:
                    service_item.append(item.servicetype.contents[0])
                    # below is magic to reverse the list :O
                type_count[u": ".join(service_item[::-1])] += float("".join(item.hours_actual.contents))
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
        for item in self.report.find_all('row'):
            if item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.board_name.contents)] += float("".join(item.hours_actual.contents))
        return type_count

    def incident_count_by_group(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.board_name.contents)] += 1
        return type_count

    def incident_count_by_day(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.board_name and item.servicetype.contents:
                if item.date_entered.contents and not (
                        (item.board_name.contents == [u'Managed Service Alerts']) or
                        ("MUST CHANGE" in item.servicetype.contents) or
                        ("No Action" in item.servicesubtype.contents)):
                    ticket_date = item.date_entered.contents[0].split(' ')
                    month, day, year = (int(x) for x in ticket_date[0].split('/'))
                    try:
                        ans = datetime.date(year, month, day)
                    except Exception as e:
                        print(e, year, month, day)
                    type_count[u"".join(ans.strftime("%A"))] += 1
        return type_count

    def incident_count_by_contact(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.contact_name and item.board_name and not (
                    (item.board_name.contents == [u'Managed Service Alerts']) or
                    ("Default Contact" in item.contact_name.contents)):
                type_count[u"".join(item.contact_name.contents)] += 1
        return type_count

    def incident_type_count_by_contact(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            service_item = []
            if item.servicetype and item.board_name and item.contact_name and not (
                    (item.board_name.contents == [u'Managed Service Alerts']) or
                    ("Default Contact" in item.contact_name.contents)):
                if item.servicesubtypeitem.contents:
                    service_item.append(item.servicesubtypeitem.contents[0])
                if item.servicesubtype.contents:
                    service_item.append(item.servicesubtype.contents[0])
                if item.servicetype.contents:
                    service_item.append(item.servicetype.contents[0])
                if item.contact_name.contents:
                    service_item.append(item.contact_name.contents[0])
                type_count[u": ".join(service_item[::-1])] += 1
        return type_count

    def total_incidents(self):
        incidents = self.report.find_all('row').count()
        return "Total Incidents: ", incidents

    def incident_details(self):
        incident_details = []
        for item in self.report.find_all('row'):
            incident = {}
            if item.board_name \
                    and not (item.board_name.contents == [u'Managed Service Alerts'])\
                    and item.date_entered_utc.contents:
                # pull the info we need:
                #{{ incident.ticket_id }}
                #{{ incident.date_opened }}
                #{{ incident.contact }}
                #{{ incident.summary }}
                #{{ incident.service_type }}
                #{{ incident.status }}
                #   support_details = business group, resolved by, urgency
                #{{ incident.date_closed }}
                # details
                # resolution
                #

                incident["ticket_id"] = "".join(item.ticketnbr.contents)
                incident["date_opened"] = "".join(item.date_entered_utc.contents)
                incident["contact"] = "".join(item.contact_name.contents)
                incident["summary"] = "".join(item.summary.contents)

                if item.servicetype.contents:
                    incident["service_type"] = "".join(item.servicetype.contents)

                if item.servicesubtype.contents:
                    incident["service_type"] += (" " + "".join(item.servicesubtype.contents))

                incident["status"] = " ".join(item.status_description.contents)

                incident["support_details"] = " ".join([item.busgroup.contents[0]])
                if item.resolved_by.contents:
                    incident["support_details"] += (": \n" + "".join(item.resolved_by.contents) )

                if item.date_closed_utc.contents:
                    incident["date_closed"] = " ".join(item.date_closed_utc.contents)

                if item.detail_description.contents:
                    incident["details"] = "".join(item.detail_description.contents).replace(r"\r", "").replace(r"\n", "").replace("\n", "<br>")

                if item.resolution.contents:
                    incident["resolution"] = "".join(item.resolution.contents).replace(r"\r", "").replace(r"\n", "").replace("\n", "<br>")

                incident_details.append(incident)
            #print incident_details
        #
        _sorted = sorted(incident_details, key=lambda item: item["date_opened"], reverse = False)
        return _sorted

    def open_incidents_with_oldest(self):
        open_calls = 0
        oldest_open = {"summary":"","date":""}
        for item in self.report.find_all('row'):
            if item.closed_flag.contents == [u"False"] and item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                open_calls += 1
                if item.date_entered.contents[0] < oldest_open['date']:
                    oldest_open["summary"], oldest_open["date"] = item.summary.contents, item.date_entered.contents[0]
        return "Open Incidents: ", open_calls, oldest_open

    def incident_hours_by_company(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.company_name.contents[0].strip(','))] += float("".join(item.hours_actual.contents))
        return type_count

    def incident_count_by_company(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.contact_name and item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                type_count[u"".join(item.company_name.contents[0].strip(','))] += 1
        return type_count

    def tech_number_closed(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.contact_name and item.board_name and not (item.board_name.contents == [u'Managed Service Alerts']):
                if item.closed_by.contents:
                    type_count[u"".join(item.closed_by.contents[0].lower())] += 1
        return type_count

    def tech_hours_unassigned(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.charge_to or item.work_type:
                if item.charge_to.contents or item.work_type.contents:
                    if "Unassigned" in item.charge_to.contents or "Unallocated" in item.charge_to.contents or "Unallocated" in item.work_type.contents:
                        type_count[u"".join(item.member_id.contents[0].lower())] += float("".join(item.hours_actual.contents))
        return type_count

    def tech_hours_breakdown(self):
        tech_client_hour_mapping = {}
        for item in self.report.find_all('row'):
            if item.charge_to or item.work_type:
                if item.member_id.contents and item.company_name.contents:
                    tech = u"".join(item.member_id.contents[0].lower())
                    company = u"".join(item.company_name.contents[0].lower())
                    if not tech in tech_client_hour_mapping:
                        tech_client_hour_mapping[tech] = defaultdict(int)
                        tech_client_hour_mapping[tech][company] += float("".join(item.hours_actual.contents))
                    else:
                        tech_client_hour_mapping[tech][company] += float("".join(item.hours_actual.contents))
        return tech_client_hour_mapping

    def company_hours_breakdown(self):
        company_tech_hour_mapping = {}
        for item in self.report.find_all('row'):
            if item.results:
                pass
            if item.charge_to or item.work_type:
                if item.member_id.contents and item.company_name.contents:
                    tech = u"".join(item.member_id.contents[0].lower())
                    company = u"".join(item.company_name.contents[0].lower())
                    if not company in company_tech_hour_mapping:
                        company_tech_hour_mapping[company] = defaultdict(int)
                    company_tech_hour_mapping[company][tech] += float("".join(item.hours_actual.contents))
        return company_tech_hour_mapping

    def users_submitting_duplicate_accounts(self):
        type_count = defaultdict(int)
        for item in self.report.find_all('row'):
            if item.servicetype and item.servicesubtype and item.servicesubtypeitem and not (item.board_name.contents == [u'Managed Service Alerts']):
                if ("Applications" in item.servicetype.contents) and ("GreenWay" in item.servicesubtype.contents) and ("Duplicate Accounts" in item.servicesubtypeitem.contents):
                    type_count[item.contact_name.contents[0]] += 1
        return type_count

def top_incidents(service_items, count=None):
    l = []
    for k in sorted(service_items, key=service_items.get, reverse=True):
        if not (k == "Admin: No Action") and not (k == "Admin: Meeting"):
            l.append((k, int(service_items[k])))
    if count:
        return l[:count]
    return l

def comma_separated(items):
    for x,y in items:
        print(x,", ", y)

