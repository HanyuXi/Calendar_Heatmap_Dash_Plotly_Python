# -*- coding: utf-8 -*-
import numpy as np
import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import dash
import copy
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import colorlover as cl

##Calendar Module
import calendar
import datetime
from datetime import datetime

app = dash.Dash(__name__)
##dummydata: To create the heatmap Calendar
pp_array = [10,10,10,10,20,30,50,60,70,90,100,100]
date_string_array = ['2018-05-01','2018-05-03','2018-05-04','2018-05-05','2018-05-06','2018-05-07','2018-05-08','2018-05-09','2018-05-10','2018-05-11','2018-05-12','2018-05-13']
##Initialize the Calendar Object. For more information, please read the calendar module library. https://docs.python.org/2/library/calendar.html
year = 2018
month = 5
calendar_object=calendar.Calendar()
days1 = calendar_object.monthdatescalendar(year,month)
days=[[None]*7,[None]*7,[None]*7,[None]*7,[None]*7]
for rows_number, rows in enumerate(days1):
    for time_index, time in enumerate(rows):
        days[rows_number][time_index] = time.day


##In terms of the color gradients/color scales. Please the read the doc. https://plot.ly/python/colorscales/
colorscale = [[0,'rgb(255,255,255)'],[0.25,'rgb(255,255,255)'],[0.25,'rgb(255,0,0)'],[0.5,'rgb(255,0,0)'],[0.5,'rgb(255,255,0)'], [0.75,'rgb(255,255,0)' ],[0.75,'rgb(0,254,0)'],[1,'rgb(0,254,0)']]
num = len(pp_array)
day_numbers= len(date_string_array)
##In python, values are passed by reference. Make a copy so it won't change the initial list. 

dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in date_string_array]  ##Convert date string objects to datetime objects
color_array=copy.deepcopy(days1)
textinfo = copy.deepcopy(days1)

x=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
y=['Week 1','Week 2','Week 3','Week 4','Week 5']
y=y[::-1]   ##REVERSE THE lists order

## Assign the value into specific day.
for rows_number, rows in enumerate(days1):
    for time_index, time in enumerate(rows):
       for i in range(day_numbers):
           if dates_list[i] == time:
               if pp_array[i] < 30 and pp_array[i] >=0:
                   color_array[rows_number][time_index] = 1
                   textinfo[rows_number][time_index] ='Grade: '+str(pp_array[i])
                   break
               if pp_array[i] < 60 and pp_array[i] >=30:
                   color_array[rows_number][time_index] = 2
                   textinfo[rows_number][time_index]= 'Grade:'+str(pp_array[i])
                   break
               if pp_array[i] >=60:
                   color_array[rows_number][time_index] = 3
                   textinfo[rows_number][time_index] = 'Grade: '+str(pp_array[i])
                   break
       else:
           color_array[rows_number][time_index] =0
           textinfo[rows_number][time_index] = 'Data is not uploaded yet'

## Z values indicate the color of date'cells.
z = color_array[::-1]
days = days[::-1]
textinfo = textinfo[::-1]

## Plot the heatmap calendar
pt = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=days, colorscale=colorscale, font_colors=['black'], hoverinfo='text', text = textinfo)  ##Figure

pt.layout.title= 'May'

##Colorbar
layout2 = go.Layout(
    autosize=False,
    width=700,
    height=450,
    margin=go.Margin(
        l=150,
        r=160,
        b=50,
        t=100,
        pad=3
    ),
        xaxis=dict(
        title='Week',
        showgrid=False,
        titlefont=dict(
            size=12,
        ),
       
    ),
)

##Plot the table in dash-plotly
fig = go.Figure(data=pt, layout=layout2)
app.layout = html.Div([dcc.Graph(id = 'my-graph', figure = fig)], style = {'width': '50%', 'display': 'inline-block'})


if __name__ == '__main__':
    app.run_server(debug =True, port=5000)
    
