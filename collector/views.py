# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from collector.models import HumidTemp
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import sys
import json
from datetime import datetime
from pytz import timezone

seoul = timezone('Asia/Seoul')

urlpatterns = staticfiles_urlpatterns()

def index(request, count='60'):
    latest_data = list(HumidTemp.objects.all().order_by('-id')[:count])
    latest_data.reverse()
    
    for d in latest_data:
        d.time = d.collect_datetime.astimezone(seoul).strftime('%H:%M:%S')

    return render_to_response('collector/chart.html', { 'latest_data': latest_data})


def img(request):
    import random

    import matplotlib as mpl
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    mpl.rcParams['timezone'] = 'Asia/Seoul'

    latest_data = HumidTemp.objects.all().order_by('-id')[:1440]

    fig = Figure()
    ax=fig.add_subplot(211)
    x=[]
    y=[]
    tempy=[]
    for data in latest_data:
        x.append(data.collect_datetime)
        y.append(data.humidity)
        tempy.append(data.temperature)

    # ax.plot_date(x, y, '-')
    #ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    ax.plot(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    ax2 = fig.add_subplot(212)
    ax2.plot(x, tempy, '-')
    ax2.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))

    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response= HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def put(request):
    if request.method == 'POST':
        sensor_data = json.loads(request.POST['data'])
        print >>sys.stderr, sensor_data
        datetime_format = datetime.fromtimestamp(sensor_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        humid_temp = HumidTemp(temperature=sensor_data['temperature'], \
            humidity=sensor_data['humidity'], \
            collect_datetime=datetime_format)
        humid_temp.save()
        return HttpResponse("{ 'success': 'true'}", mimetype='application/json')
    return HttpResponseBadRequest()


