from flask import Blueprint, request, render_template, redirect, url_for, Request

from reporting import report
import chart_generators
import date_utils
from reporting import cw_request


mod = Blueprint('reporting', __name__, url_prefix='/reports')

@mod.route('/', methods=['GET', 'POST'])
def index():
    """
        This is for the index of the BMT Reporting website.
        Contains the landing and launchpad for BMT reporting.
    """
    return render_template('index.html')

@mod.route('/company/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/company/<count>/<company>/', methods=['GET', 'POST'])
@mod.route('/company/', methods=['GET', 'POST'])
def company(company=None, date_range=None, count=20):
    """
        This is for the company report API
        Need a company and date range.
    """
    company_list = ["Brian Trematore Plumbing & Heating, Inc.", "New Jersey Urology CBO-1",
                    "Business Machine Technologies", "Gramkow Carnevale Seifert, Inc.",
                    "Water-Jel Technologies LLC", "Freeman Hughes Freeman Law", "Dugan Colthart & Zoch",
                    "Sherwood Learning Solutions, Inc.",]
    if count == "default":
        count = 20
    count = int(count)
    if request.method == "POST" and request.form['start_date'] and request.form['end_date']:
        date_range = ":".join((request.form['start_date'],request.form['end_date']))
        return redirect(url_for('reporting.company', count="default", company=company, date_range=date_range))
    if not date_range or (date_range=="default"):
        date_range = date_utils.get_previous_week_range()
    dates = date_utils.format_date_for_cw(date_range)
    charts = []
    if company:
        new_request = cw_request.ReportRequestData(limit=0, company=company, start_date=dates[0], end_date=dates[1])
        report_data = report.Report(new_request.document())
        print "Request sent for: " + new_request.url()
        # the different datapoints we want to find
        incident_count_by_service_type = report.top_incidents(report_data.incident_count_by_service_type(), count)
        incident_count_by_contact = report.top_incidents(report_data.incident_count_by_contact(), count)
        incident_count_by_group = report.top_incidents(report_data.incident_hours_by_group(), count)
        type_count_by_contact = report.top_incidents(report_data.incident_type_count_by_contact(), count)
        # this is the chart data
        # putting it in a list of tuples for now, so we'll be able to handle it in the view later.
        charts = [("pie_chart", 'types_by_contact_pie',
                   "Types by Contact", chart_generators.pie_chart(type_count_by_contact, count)),
                  ("pie_chart", 'incident_count_by_service_type',
                   "Incidents by Service Type", chart_generators.pie_chart(incident_count_by_service_type, count)),
                  ("pie_chart", 'incident_count_by_contact',
                   "Incidents by Contact", chart_generators.pie_chart(incident_count_by_contact, count)),
                  ("bar_chart", 'incident_count_by_group',
                   "Incidents by Group", chart_generators.bar_chart(incident_count_by_group)),]
    return render_template('company.html', date_range=date_range,
                           start_date=date_utils.format_date_for_web(dates[0]),
                           end_date=date_utils.format_date_for_web(dates[1]),
                           company=company, charts=charts, company_list=company_list)

@mod.route('/hours/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/hours/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/hours/<count>/<company>/', methods=['GET', 'POST'])
@mod.route('/hours/', methods=['GET', 'POST'])
def hours(company=None, date_range=None, count=20):
    """
        This is to pull hour reports. If no company is set, or daterange, it will go to defaults.
    """
    if company == "default":
        company = None
    if count == "default":
        count = 20
    count = int(count)
    if request.method == "POST" and request.form['start_date'] and request.form['end_date']:
        date_range = ":".join((request.form['start_date'],request.form['end_date']))
        return redirect(url_for('reporting.hours', count="default", company="default", date_range=date_range))
    if not date_range or (date_range=="default"):
        date_range = date_utils.get_previous_week_range()
    dates = date_utils.format_date_for_cw(date_range)
    new_request = cw_request.ReportRequestData(limit=0, company=company,
                                    start_date=dates[0], end_date=dates[1])
    report_data = report.Report(new_request.document())
    print "Request sent for: " + new_request.url()
    incident_hours_by_group = report.top_incidents(report_data.incident_hours_by_group())
    incident_hours_by_company = report.top_incidents(report_data.incident_hours_by_company(),count)
    # this is the chart data
    # putting it in a list of tuples for now, so we'll be able to handle it in the view later.
    charts = [("bar_chart", 'incident_hours_by_group_bar',
               "Hours by Group", chart_generators.bar_chart(incident_hours_by_group)),
              ("bar_chart", 'incident_hours_by_company_bar',
               "Hours by Company", chart_generators.bar_chart(incident_hours_by_company)),
              ]
    return render_template('company.html', company=company, date_range=date_range,
                           charts=charts, start_date=dates[0], end_date=dates[1] )

@mod.route('/service/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/service/<company>/', methods=['GET', 'POST'])
@mod.route('/service/', methods=['GET', 'POST'])
def service(company=None, date_range=None, count=20):
    """
        This is to pull hour reports. If no company is set, or daterange, it will go to defaults.
    """
    if company == "default":
        company = None

    if not date_range or (date_range=="default"):
        date_range = date_utils.get_previous_week_range()

    dates = date_utils.format_date_for_cw(date_range)
    new_request = cw_request.ReportRequestData(limit=0, company=company,
                                    start_date=dates[0], end_date=dates[1])

    report_data = report.Report(new_request.document())
    print "Request sent for: " + new_request.url()
    incidents = report_data.incident_details()

    return render_template('incident_report_template.html', company=company, date_range=date_range, incidents=incidents,
                           start_date=dates[0], end_date=dates[1])