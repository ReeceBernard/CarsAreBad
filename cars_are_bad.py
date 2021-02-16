import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime as dt
from src.formulas import depreciation
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

year = int(dt.today().year)
CAR_MAKES =["Abarth","Alfa Romeo","Aston Martin","Audi","Bentley","BMW","Bugatti","Cadillac",
	"Chevrolet","Chrysler","Citroën","Dacia","Daewoo","Daihatsu","Dodge","Donkervoort","DS","Ferrari",
	"Fiat","Fisker","Ford","Honda","Hummer","Hyundai","Infiniti","Iveco","Jaguar","Jeep","Kia","KTM",
	"Lada","Lamborghini","Lancia","Land Rover","Landwind","Lexus","Lotus","Maserati","Maybach","Mazda",
	"McLaren","Mercedes-Benz","MG","Mini","Mitsubishi","Morgan","Nissan","Opel","Peugeot","Porsche",
	"Renault","Rolls-Royce","Rover","Saab","Seat","Skoda","Smart","SsangYong","Subaru","Suzuki",
	"Tesla","Toyota","Volkswagen","Volvo"]
CAR_TYPES = ['Sedan','Truck','SUV/Crossover','Coupe','Hatchback','Van/Minivan','Convertible',
	'Wagon']
CAR_YEARS = [year+1-i for i in range(50)]

external_stylesheets = [dbc.themes.MINTY]
car_make_options = [dict(label=str(car), value=str(car)) for car in CAR_MAKES]
car_type_options = [dict(label=str(car), value=str(car)) for car in CAR_TYPES]
car_year_options = [dict(label=str(car), value=str(car)) for car in CAR_YEARS]
new_used_options = [dict(label=str(car), value=str(car)) for car in ['New', 'Used']]
app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[html.H1(children="The True Cost Of Buying A Car"),
	dcc.Markdown(children="""91.3% of Americans own or lease their cars. The average American spends around $37,000 buying their car,
		but most do not realize the cost does not end there. Fill out the information below to see a convervative estimate of how much your car truely costs you.  
		**Note:** This site does not store user data, as well as does not require a sign in. The information you share is not monitored or stored by the site.
		The sole purpose of this site is to inspire more people to ditch the car for a healthier happier future.  
		**Note:** This is just for purchasing a car today. Eventually I will add the functionality to calculate the cost of owning your current car.
		Until then feel free to select the newest model of your car and go back as many years as your current car vs the time you bought it.
		This will not be a great estimate, but should get you in the ball park.""",style={'padding': '50'}),
	html.Div(children=[
		html.P(['Vehicle  Make:', dcc.Dropdown(id='c_make', options=car_make_options)],style={'width': '25%', 'display': 'inline-block'}),
		html.P(['Vehicle  Type:', dcc.Dropdown(id='c_type', options=car_type_options)],style={'width': '25%', 'display': 'inline-block'}),
		html.P(['Vehicle Year:', dcc.Dropdown(id='c_year', options=car_year_options)],style={'width': '25%', 'display': 'inline-block'}),
		html.P(['New or Used:', dcc.Dropdown(id='n_or_u', options=new_used_options)],style={'width': '25%', 'display': 'inline-block'})],
		style={'width': '49%', 'display': 'inline-block'}),
	html.P(['Vehicle  Price: ',daq.NumericInput(id='c_price', size = 120,value=0, max=500000)]),
	html.Button('Find Cost', id='button'),
	html.P(id='status'),
	html.Div(id='depreciation')])

@app.callback(
    Output(component_id='depreciation', component_property='children'),
    [Input('button', 'n_clicks')],
    state=[
        State(component_id='c_make', component_property='value'),
        State(component_id='c_year', component_property='value'),
        State(component_id='n_or_u', component_property='value'),
        State(component_id='c_price', component_property='value')
    ]
)
def plot_costs(n_clicks,c_make, c_year, n_or_u,c_price):
	y = [int(year)+i for i in range(0,10)]
	dep_costs = depreciation(c_make,n_or_u,c_price,c_year)
	df = pd.DataFrame({"Depreciation": dep_costs,"Years": y})
	return dcc.Graph(id='dec_graph', figure={
		'data': [{'y': df.Depreciation, 'x' : df.Years , 'type':'line'}],
		'layout': {'title' : 'Depreciation Over 10 Years'}
		})

    

if __name__ == '__main__':
	app.run_server(debug=True)
