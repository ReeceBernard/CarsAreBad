import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime as dt
import src.formulas as formulas
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

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
STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
	"Delaware",'District of Columbia',"Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky",
	"Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri",
	"Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
	"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
	"South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington",
	"West Virginia","Wisconsin","Wyoming"]
CAR_YEARS = [year+1-i for i in range(50)]
AGES = [16+i for i in range(100)]
CLAIMS = [i for i in range(20)]
MPGS = [i for i in range(10,80)]

external_stylesheets = [dbc.themes.MINTY]
car_make_options = [dict(label=str(car), value=str(car)) for car in CAR_MAKES]
car_type_options = [dict(label=str(car), value=str(car)) for car in CAR_TYPES]
car_year_options = [dict(label=str(car), value=str(car)) for car in CAR_YEARS]
new_used_options = [dict(label=str(car), value=str(car)) for car in ['New', 'Used']]
policy_options = [dict(label=str(car), value=str(car)) for car in ['Liability', 'Comprehensive', 'Collision']]
state_options = [dict(label=str(car), value=str(car)) for car in STATES]
y_n = [dict(label=str(car), value=str(car)) for car in ['Yes', 'No']]
gas_options = [dict(label=str(car), value=str(car)) for car in ['Regular', 'Premium', 'Diesel']]
mpg_options = [dict(label=str(car), value=str(car)) for car in MPGS]


app = dash.Dash(external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[html.H1(children="The True Cost Of Buying A Car"),
	dcc.Markdown(children="""91.3% of Americans own or lease their cars. The average American spends around $37,000 buying their car,
		but most do not realize the cost does not end there. Fill out the information below to see a convervative estimate of how much your car truely costs you.  
		**Note:** Estimates are based on 15,000 miles driven a year.  
		**Note:** This site does not store user data, as well as does not require a sign in. The information you share is not monitored or stored by the site.
		The sole purpose of this site is to inspire more people to ditch the car for a healthier happier future.  
		**Note:** This is just for purchasing a car today. Eventually I will add the functionality to calculate the cost of owning your current car.
		Until then feel free to select the newest model of your car and go back as many years as your current car vs the time you bought it.
		This will not be a great estimate, but should get you in the ball park.""",style={'padding': '50'}),
	dcc.Markdown("""##### Currently there is a way better looking cost calculator provided by [edmunds](https://www.edmunds.com/tco.html "Cost To Own Calc") eventually mine will be better! :)""",style={'padding': '50'}),
	html.Br(),
	html.H2('Input Your Information Below.'),
	html.Div(children=[
		html.P(['Vehicle  Make:', dcc.Dropdown(id='c_make', options=car_make_options,value='Mazda')],style={'width': '10%', 'display': 'inline-block'}),
		html.P(['Vehicle  Type:', dcc.Dropdown(id='c_type', options=car_type_options,value='SUV/Crossover')],style={'width': '10%', 'display': 'inline-block'}),
		html.P(['Vehicle Year:', dcc.Dropdown(id='c_year', options=car_year_options,value=year)],style={'width': '10%', 'display': 'inline-block'}),
		html.P(['New or Used:', dcc.Dropdown(id='n_or_u', options=new_used_options,value='New')],style={'width': '10%', 'display': 'inline-block'}),
		html.P(['Financed?', dcc.Dropdown(id='p_financed', options=y_n,value='Yes')],style={'width': '10%', 'display': 'inline-block'}),
		],
		style={'width': '100%', 'display': 'inline-block'}),
	html.Div(children=[
		html.P(['State:', dcc.Dropdown(id='p_state', options=state_options,value='Georgia')],style={'width': '20%', 'display': 'inline-block'}),
		html.P(['Policy Type: (Select All)', dcc.Dropdown(id='c_policy', options=policy_options,value=['Liability', 'Comprehensive', 'Collision'],multi=True)],style={'width': '70%', 'display': 'inline-block'}),
		html.P(['Younger than 25:', dcc.Dropdown(id='p_age', options=y_n,value='No')],style={'width': '10%', 'display': 'inline-block'})
		], style={'width': '50%', 'display': 'inline-block'}),
	html.Div(children=[
		html.P(['Gas Type:', dcc.Dropdown(id='g_type', options=gas_options,value='Regular')],style={'width': '60%', 'display': 'inline-block'}),
		html.P(['MPG:', dcc.Dropdown(id='mpg_type', options=mpg_options,value='30')],style={'width': '40%', 'display': 'inline-block'})
		],style={'width': '15%'}),
	html.P(['Vehicle  Price: ',daq.NumericInput(id='c_price', size = 120,value=37500, max=500000)]),
	html.H2("Cost of 6 Year Ownership"),
	dcc.Markdown("""According to Autotrader the average car owner will own their car for 6.3 years."""),
	html.Div(id='total_cost_graph'),
	html.P(id='total_cost'),
	html.Br(),
	html.H2('Break Down Of Costs'),
	html.Br(),
	html.H3("Depreciation Costs"),
	html.Div(id='depreciation'),
	html.H3("Financing"),
	dcc.Markdown("""We will assume standard traditional financing of 10% down payment at 4.5% interest for 60 months."""),
	html.Div(children=[html.P(id='interest_cost')]),
	html.H3("Insurance Premiums"),
	dcc.Markdown("""Car insurance premiums are very difficult to get a clear
		 estimate. The below estimate will just use your states average cost.
		 More information can be found [Here](https://www.iii.org/fact-statistic/facts-statistics-auto-insurance "III Data Website")"""),
	html.Div(children=[html.P(id='insurance_cost')]),
	html.H3("Gas"),
	dcc.Markdown("""My calculations are assuming the car is driven 13,500 miles a year.  
		Fun Gas Calculator [Here](https://gasprices.aaa.com/ "AAA Gas Website")"""),
	html.Div(children=[html.P(id='gas_cost')]),
	html.H3("Maintence"),
	dcc.Markdown(""" \"Per AAA, maintenance is $766.50 and tires are $147 per year.
		Combining the two, we’re at $913.50, and that looks about right for late model cars.
		Of course, if your car is more than a few years old, that number could easily double.
		But how much you actually pay will again depend upon personal circumstances.
		If you take care of your vehicle, maintenance expenses are likely to be lower.
		If you live in an area that experiences harsh weather conditions, it will probably be higher.
		Still another variable is your ability to perform routine repairs yourself,
		versus bringing the car to a shop.\"  
		[Source](https://www.moneyunder30.com/true-cost-of-owning-a-car "MoneyUnder30 Website")"""),
	html.P('Your maintenance cost will be roughly $913.50 a year.')
	
	
])


@app.callback(
    Output(component_id='depreciation', component_property='children'),
    [Input(component_id='c_make', component_property='value'),
        Input(component_id='c_year', component_property='value'),
        Input(component_id='n_or_u', component_property='value'),
        Input(component_id='c_price', component_property='value')]
)
def plot_costs(c_make, c_year, n_or_u,c_price):
	y = [int(year)+i for i in range(0,10)]
	dep_costs = formulas.depreciation(c_make,n_or_u,c_price,c_year)
	df = pd.DataFrame({"Depreciation": dep_costs,"Years": y})
	return dcc.Graph(id='dec_graph', figure={
		'data': [{'y': df.Depreciation, 'x' : df.Years , 'type':'line'}],
		'layout': {'title' : 'Total Depreciation Cost Over 10 Years'}
		})

@app.callback(
    Output(component_id='insurance_cost', component_property='children'),
    [Input(component_id='p_state', component_property='value'),
    	Input(component_id='c_policy', component_property='value'),
    	Input(component_id='c_type', component_property='value'),
    	Input(component_id='p_age', component_property='value')]
)
def get_insurance_costs(p_state, c_policy, c_type, p_age):
	cost = formulas.get_insurance_estimate(p_state, c_policy, c_type,p_age)
	return "Your premiums will cost you ${:,.2f} annually.".format(cost)
	return cost

@app.callback(
    Output(component_id='gas_cost', component_property='children'),
    [Input(component_id='g_type', component_property='value'),
    Input(component_id='mpg_type', component_property='value'),
    	Input(component_id='p_state', component_property='value')]
)
def get_gas_costs(gas_type, mpg_type,p_state):
	cost = formulas.get_gas_estimate(gas_type, mpg_type,p_state)
	return "You will pay ${:,.2f} for gas annually.".format(cost)
    
@app.callback(
    Output(component_id='interest_cost', component_property='children'),
    [Input(component_id='p_financed', component_property='value'),
    	Input(component_id='c_price', component_property='value')]
)
def get_financing_costs(p_financed, c_price):
	cost = formulas.get_finance_estimate(p_financed, c_price)
	return "You will pay ${:,.2f} a year in interest.".format(cost[0])

@app.callback(
    [Output(component_id='total_cost_graph', component_property='children'),
    	Output(component_id='total_cost', component_property='children')],
    [Input(component_id='c_make', component_property='value'),
        Input(component_id='c_year', component_property='value'),
        Input(component_id='n_or_u', component_property='value'),
        Input(component_id='c_price', component_property='value'),
        Input(component_id='p_state', component_property='value'),
    	Input(component_id='c_policy', component_property='value'),
    	Input(component_id='c_type', component_property='value'),
    	Input(component_id='p_age', component_property='value'),
    	Input(component_id='g_type', component_property='value'),
   		Input(component_id='mpg_type', component_property='value'),
    	Input(component_id='p_financed', component_property='value')]
)
def get_total_costs(c_make, c_year, n_or_u,c_price,p_state,c_policy,c_type,p_age,g_type,mpg_type,p_financed):
	y = [int(year)+i for i in range(0,6)]
	dep_costs = formulas.depreciation(c_make,n_or_u,c_price,c_year)
	dep_cost_yearly = [dep_costs[0]]
	for i in range(1,6):
		dep_cost_yearly.append(dep_costs[i]-dep_costs[i-1])
	ins_cost = [formulas.get_insurance_estimate(p_state, c_policy, c_type,p_age)]*6
	gas_cost = [formulas.get_gas_estimate(g_type, mpg_type,p_state)]*6
	fin_cost = formulas.get_finance_estimate(p_financed, c_price)
	fin_cost.append(0)
	main_costs = [913.50]*6
	total_cost  = [a+b+c+d+e for a, b,c,d,e in zip(dep_cost_yearly, ins_cost,gas_cost,fin_cost, main_costs)]
	df = pd.DataFrame({"Total Cost": total_cost,"Years": y})
	total_cost_str = "${:,.2f}".format(np.sum(total_cost))
	return dcc.Graph(id='dec_graph', figure={
		'data': [{'y': df['Total Cost'], 'x' : df.Years , 'type':'line'}],
		'layout': {'title' : 'Total Cost Over 6 Years'}
		}), f'Your Total Cost Over 6 Years is {total_cost_str}'

if __name__ == '__main__':
	app.run_server(debug=True)
