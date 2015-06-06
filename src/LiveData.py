import plotly.plotly as py # plotly library
from plotly.graph_objs import * # plotly graph objects
import time, datetime, random, math, threading # timer functions

class LiveData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


###########################################################################
# Cridentials and sign in
#
        self.username = 'andreas.kall'
        self.api_key = 'b7uwccjbpr'
        self.speed_token = 'i6ulgqn4mp'
        self.rpm_token = 'aj6o0eh54o'
        self.eng_block_token = '5cggy6tthh'
        self.cylinder_temp_token = 'ylptfineo4'
        self.cylinder_head_temp_token = '13dcofwzp8'
        self.air_temp_token = 'l0kjn8nu3q'
        self.air_pressure_token = 'ud1r76dcmb'

        py.sign_in(self.username, self.api_key)
        self.readyForData = False
        self.streaming = False


###########################################################################
# Traces
#

        self.speed = Scatter(
            x=[],
            y=[],
            name = 'Speed',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.speed_token,
                maxpoints=120
            )
        )

        self.rpm = Scatter(
            x=[],
            y=[],
            name = 'RPM',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.rpm_token,
                maxpoints=120
            )
        )

        self.eng_block_temp = Scatter(
            x=[],
            y=[],
            name = 'Eng. block',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.eng_block_token,
                maxpoints=120
            )
        )

        self.cylinder_temp = Scatter(
            x=[],
            y=[],
            name = 'Cylinder block',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.cylinder_temp_token,
                maxpoints=120
            )
        )

        self.cylinder_head_temp = Scatter(
            x=[],
            y=[],
            name = 'Cylinder head',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.cylinder_head_temp_token,
                maxpoints=120
            )
        )

        self.air_temp = Scatter(
            x=[],
            y=[],
            name = 'Air temp',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.air_temp_token,
                maxpoints=120
            )
        )

        self.air_pressure = Scatter(
            x=[],
            y=[],
            name = 'Air pressure',
            line=Line(
                shape='spline'
            ),
            stream=dict(
                token=self.air_pressure_token,
                maxpoints=120
            )
        )


###########################################################################
# Layouts
#
        self.speed_layout = Layout(
            title='Speed',
            showlegend=True,
            yaxis=YAxis(title='Speed [Km/h]')
        )

        self.rpm_layout = Layout(
            title='RPM',
            showlegend=True,
            yaxis=YAxis(title='RPM')
        )

        self.speed_rpm_layout = Layout(
            title='Speed and RPM',
            showlegend=True,
            yaxis=YAxis(
                title='Speed [Km/h]',
                titlefont=Font(
                    color='rgb(31, 119, 180)'
                ),
                tickfont=Font(
                    color='rgb(31, 119, 180)'
                ),
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(31, 119, 180)',
                gridwidth=1,
                zerolinewidth=2
            ),
            yaxis2=YAxis(
                title='RPM',
                titlefont=Font(
                    color='rgb(255, 127, 14)'
                ),
                tickfont=Font(
                    color='rgb(255, 127, 14)'
                ),
                overlaying='y',
                side='right',
                showgrid=False

            )
        )

        self.temp_layout = Layout(
            title='Temperatures',
            showlegend=True,
            yaxis=YAxis(title='Temp [degrees]')
        )

        self.air_layout = Layout(
            title='Air pressure and temperature',
            showlegend=True,
            yaxis=YAxis(
                title='Pressure [Pa]',
                titlefont=Font(
                    color='rgb(31, 119, 180)'
                ),
                tickfont=Font(
                    color='rgb(31, 119, 180)'
                ),
                showgrid=True,
                zeroline=True,
                gridcolor='rgb(31, 119, 180)',
                gridwidth=1,
                zerolinewidth=2
            ),
            yaxis2=YAxis(
                title='Temp [degrees]',
                titlefont=Font(
                    color='rgb(255, 127, 14)'
                ),
                tickfont=Font(
                    color='rgb(255, 127, 14)'
                ),
                overlaying='y',
                side='right',
                showgrid=False

            )
        )

    def run(self):

###########################################################################
# Init figures and streams
#

        self.speed_fig = Figure(data=[self.speed], layout=self.speed_layout)
        self.rpm_fig = Figure(data=[self.rpm], layout=self.rpm_layout)
        self.temp_fig = Figure(data=[self.eng_block_temp, self.cylinder_temp, self.cylinder_head_temp], layout=self.temp_layout)
        self.air_fig = Figure(data=[self.air_temp, self.air_pressure], layout=self.air_layout)



        py.plot(self.speed_fig, filename='Speed', auto_open=False)
        py.plot(self.rpm_fig, filename='RPM', auto_open=False)
        py.plot(self.temp_fig, filename='Temperatures', auto_open=False)
        py.plot(self.air_fig, filename='Environment data', auto_open=False)

        self.speed_stream = py.Stream(self.speed_token)
        self.speed_stream.open()
        self.rpm_stream = py.Stream(self.rpm_token)
        self.rpm_stream.open()

        self.eng_block_temp_stream = py.Stream(self.eng_block_token)
        self.eng_block_temp_stream.open()
        self.cylinder_temp_stream = py.Stream(self.cylinder_temp_token)
        self.cylinder_temp_stream.open()
        self.cylinder_head_temp_stream = py.Stream(self.cylinder_head_temp_token)
        self.cylinder_head_temp_stream.open()

        self.air_temp_stream = py.Stream(self.air_temp_token)
        self.air_temp_stream.open()
        self.air_pressure_stream = py.Stream(self.air_pressure_token)
        self.air_pressure_stream.open()
        self.readyForData = True



###########################################################################
# Update values
#
    def sendECUValues(self, logs):
        if self.readyForData and self.streaming:
            # Order in logs param: cylinder_temp, cylinder_head_temp, eng_block_temp, battery_voltage, air_pressure, air_temp, rpm, fuel_mass, error_code
            self.cylinder_temp_stream.write({'x': datetime.datetime.now(), 'y':logs[0]})
            self.cylinder_head_temp_stream.write({'x': datetime.datetime.now(), 'y': logs[1]})
            self.eng_block_temp_stream.write({'x': datetime.datetime.now(), 'y': logs[2]})
            self.rpm_stream.write({'x': datetime.datetime.now(), 'y': logs[6]})
            self.air_temp_stream.write({'x': datetime.datetime.now(), 'y': logs[5]})
            self.air_pressure_stream.write({'x': datetime.datetime.now(), 'y': logs[4]})



    def sendSpeed(self, speed):
        if self.readyForData and self.streaming:
            self.speed_stream.write({'x': datetime.datetime.now(), 'y': speed})

###########################################################################
# If run as main
#

if __name__ == '__main__':
    live = LivePlot()
    while True:
        sensor_data1 = math.sin(time.time())*10 + 10
        sensor_data2 = -random.random()*10

        temp1 = math.cos(time.time()/10)*5 + 3
        temp2 = 4
        temp3 = math.cos(time.time()*2)*3 - 2

        air_temp = math.sin(time.time()*10) + random.random() + 20 - math.cos(time.time())/5
        air_pressure = math.sin(time.time()*9) + random.random() + 1000 - math.cos(time.time())/6

        live.sendValues(sensor_data1, sensor_data2, temp1, temp2, temp3, air_temp, air_pressure)

        time.sleep(0.5) # delay between stream posts










