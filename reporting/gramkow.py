from reporting import request

new_request = request.ReportReq

uestData(limit=0, company="Gramkow Carnevale Seifert, Inc.", start_date='03/02/2014', end_date='03/08/2014')

print new_request.document()