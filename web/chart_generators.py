import colorsys

def pie_chart(report_data_tuple_list, count):
    chart_data = []
    # I stole this, works well to generate an appropriate hex range.
    # change the count + 3 to make the last color match _less_ to the first chart color
    # change the .75 .75 to up/down the saturation and brightness
    HSV_tuples = [(x*(3.381966)/(count+3), 0.75, 0.75) for x in xrange(count+3)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    RGB_tuples = map(lambda x: tuple(map(lambda y: int(y * 255),x)),RGB_tuples)
    HEX_tuples = map(lambda x: tuple(map(lambda y: chr(y).encode('hex'),x)), RGB_tuples)
    HEX_tuples = map(lambda x: "".join(x), HEX_tuples)
    color_count = 0
    for nt, i in report_data_tuple_list:
        chart_data.append (
            {
                "value": i,
                "color": "#" + HEX_tuples[color_count],
                "title": nt,
            }
        )
        color_count += 1
    # this is a list of dictionaries. Not a json dump, but it needs to be json, so we'll do that in the view (easier
    # and less code)
    return chart_data

def bar_chart(report_data_tuple_list):
    # this is the same way as pie_chart, a dictionary we pass to the view for the js to handle.
    # this just follows the schema set forth in the ChartNew.js docs
    labels_and_data = zip(*report_data_tuple_list)
    chart_data = {
                    "labels": labels_and_data[0],
                    "datasets": [
                        {
                            "fillColor": "rgba(151,187,205,0.5)",
                            "strokeColor": "rgba(151,187,205,1)",
                            "pointColor": "rgba(151,187,205,1)",
                            "pointStrokeColor": "#fff",
                            "data": labels_and_data[1],
                            "title": "",
                        },
                    ],
                }
    return chart_data