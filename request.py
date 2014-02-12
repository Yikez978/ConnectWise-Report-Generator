import requests
import config

class ReportRequestData:

    def __init__(self, report=None, limit=None, start_date=None, end_date=None, company=None):

        self.parameters = config.parameters

        # default parameters
        self.report_type = 'Service'

        if report:
            self.report_type = report

        # start formatting the query parameters
        query = []
        if start_date:
            query.append("date_entered >= '{0} 0:00:00 AM'".format(start_date))
        if end_date:
            query.append("date_entered < '{0} 0:00:00 AM'".format(end_date))
        if company:
            query.append("company_name = '{0}'".format(company))
        if limit:
            self.parameters['l'] = limit

        self.query = " and ".join(query)
        self.parameters['r'] = self.report_type
        self.parameters['q'] = self.query

        self.report = requests.get('https://myconnectwise.com/v4_6_release/webreport/', verify=False, params=self.parameters)

    def print_url(self):
        return self.report.url

    def request_document(self):
        return self.report.text