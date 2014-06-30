from flask import Blueprint, request, render_template, g, redirect, url_for, session, flash, jsonify
from reporting import request, report
from datetime import datetime, timedelta
import chart_generators
from base64 import b16encode
mod = Blueprint('reporting', __name__, url_prefix='/reports')

@mod.route('/', methods=['GET', 'POST'])
def index():
    """
        This is for the index of the BMT Reporting website.
        Contains the landing and launchpad for BMT reporting.
    """
    return render_template('index.html')

@mod.route('/company/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/company/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/company/<count>/<company>/', methods=['GET', 'POST'])
@mod.route('/company/', methods=['GET', 'POST'])
def company(company=None, date_range=None, count=20):
    """
        This is for the company report API
        Need a company and date range.
    """
    count = int(count)
    charts = []
    if company and date_range:
        date_range.replace("-","/")
        dates = date_range.split(":")
        new_request = request.ReportRequestData(limit=0, company=company,
                                        start_date=dates[0], end_date=dates[1])
        report_data = report.Report(new_request.document())
        print "Request sent for: " + new_request.url()
        type_count_by_contact = report.top_incidents(report_data.incident_type_count_by_contact(), count)
        # this is the chart data
        # putting it in a list of tuples for now, so we'll be able to handle it in the view later.
        charts = [("pie_chart", 'types_by_contact_pie',
                   "Types by Contact", chart_generators.pie_chart(type_count_by_contact, count)),
                  ]
    return render_template('company.html', company=company, date_range=date_range,
                           charts=charts)

@mod.route('/hours/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/hours/<count>/<company>/<date_range>/', methods=['GET', 'POST'])
@mod.route('/hours/<count>/<company>/', methods=['GET', 'POST'])
@mod.route('/hours/<count>/', methods=['GET', 'POST'])
@mod.route('/hours/', methods=['GET', 'POST'])
def hours(company=None, date_range=None, count=10):
    """
        This is to pull hour reports. If no company is set, or daterange, it will go to defaults.
    """
    count = int(count)
    if not date_range:
        now = datetime.now()
        end_date = now.strftime("%m-%d-%Y")
        start_date = now - timedelta(days=7)
        start_date = end_date.strftime("%m-%d-%Y")
        date_range = ":".join((start_date,end_date))
    print date_range
    date_range.replace("-","/")
    dates = date_range.split(":")
    new_request = request.ReportRequestData(limit=0, company=company,
                                    start_date=dates[0], end_date=dates[1])
    report_data = report.Report(new_request.document())
    print "Request sent for: " + new_request.url()
    incident_hours_by_group = report.top_incidents(report_data.incident_hours_by_group(), count)
    # this is the chart data
    # putting it in a list of tuples for now, so we'll be able to handle it in the view later.
    charts = [("bar_chart", 'incident_hours_by_group_bar',
               "Hours by Group", chart_generators.bar_chart(incident_hours_by_group)),
              ]
    return render_template('company.html', company=company, date_range=date_range,
                           charts=charts)