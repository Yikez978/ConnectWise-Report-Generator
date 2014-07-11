from datetime import datetime, timedelta

def get_previous_week_range():
    now = datetime.now()
    end_date = now.strftime("%m-%d-%Y")
    start_date = now - timedelta(days=7)
    start_date = start_date.strftime("%m-%d-%Y")
    date_range = ":".join((start_date,end_date))
    return date_range

def format_date_for_cw(date_range):
    date_range.replace("-","/")
    return date_range.split(":")

def format_date_for_web(date_range):
    return date_range.replace("/","-")