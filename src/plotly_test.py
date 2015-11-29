#!/usr/bin/env python

import plotly.plotly as py # plotly library
from plotly.graph_objs import Scatter, Layout, Figure # plotly graph objects
import time # timer functions
import random, datetime

username     = 'andreas.kall'
api_key      = 'b7uwccjbpr'
stream_token = 'ntt8ksjjcz'


#>>> data = Data([trace1])
#>>> py.plot(data)
#>>> s = py.Stream('my_stream_id')
#>>> s.open()
#>>> s.write(dict(x=1, y=2))
#>> s.close()
i=1

py.sign_in(username, api_key)

trace1 = Scatter(
    x=[],
    y=[],
    stream=dict(
        token=stream_token,
        maxpoints=200
    )
)


layout = Layout(title='Raspberry Pi Streaming Sensor Data')

fig = Figure(data=[trace1], layout=layout)

url = py.plot(fig, filename='Raspberry Pi Streaming Example Values')
print(url)
#stream = py.Stream(stream_token)
#stream.open()


while True:
    #sensor_data = random.random()*5
    #stream.write(dict(x=i, y=sensor_data))
    #i +=1
    #print(i)
    time.sleep(1) # delay between stream posts

	