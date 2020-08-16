from chalice import Chalice, Rate
from chalicelib import req
import boto3
import time
import json

app = Chalice(app_name='weather-app')
s3 = boto3.client('s3', region_name='ca-central-1')

'''
Return Weather Data for Montreal
'''
@app.route('/')
def index():
    return req.request()
'''
Return Weather Data for the City defined in the Route
'''
@app.route('/{city}')
def weatherByCityName(city):
    return req.requestCity(city)
'''
Uploads curent weather data to S3 every minute
'''
@app.schedule(Rate(5, unit=Rate.MINUTES))
def periodic_task(event):
    data = req.request()
    name = str(round(time.time()))

    f = open("/tmp/weatherdata", "w")
    f.write(json.dumps(data))
    f.close()

    s3.upload_file("/tmp/weatherdata", "weather-app-data", name)
'''
Whenever weather data is uploaded to S3, insert it into dynamo DB
'''
@app.on_s3_event(bucket='weather-app-data')
def file_uploaded(event):
    objName = event.key
    print(objName)