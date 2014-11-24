import requests
import config


class ReportRequestData:

    def __init__(self, report=None, limit=None, start_date=None, end_date=None, company=None):
        parameters = config.parameters
        # default parameters
        report_type = 'Service'
        if report:
            report_type = report
        # start formatting the query parameters
        query = []
        if report_type == 'Service':
            if start_date:
                query.append("date_entered >= '{0} 0:00:00 AM'".format(start_date))
            if end_date:
                query.append("date_entered < '{0} 11:59:59 PM'".format(end_date))

        if report_type == 'Time':
            if start_date:
                query.append("Date_Start >= '{0} 0:00:00 AM'".format(start_date))
            if end_date:
                query.append("Date_Start < '{0} 11:59:59 PM'".format(end_date))
        if company:
            query.append("company_name = '{0}'".format(company))
        if limit:
            parameters['l'] = limit
        query = " and ".join(query)
        parameters['r'] = report_type
        parameters['q'] = query
        self.report = requests.get('https://api-na.myconnectwise.net/v2014_6/webreport/', verify=False, params=parameters)

    def url(self):
        return self.report.url

    def document(self):
        return self.report.text