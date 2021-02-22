import pandas as pd
import numpy as np
from datetime import datetime as dt

def depreciation(make,new_tf,price,year):
	dep_year = int(dt.today().year)+1-int(year)
	high_dep = ['Buick', 'Cadillac','Land Rover', 'Mercedes-Benz', 'Infiniti', 'Lincoln', 'Audi']
	low_dep = ['Ford', 'Toyota', 'Honda', 'Mini', 'Nissan', 'Volkswagen']
	# if make in high_dep:
	# 	r_n = 35
	# 	r_o = 21.4
	# elif make in low_dep:
	# 	r_n = 16
	# 	r_o = 10.4
	# else:
	# 	r_n = 25
	# 	r_o = 15.6
	r_o = .14
	r_n = .24
	if new_tf == 'New':
		a = [price*(1-r_n)]
	else:
		a = [price*(1-r_o)]
	for i in range(dep_year,dep_year+9):
		# if i > 5:
		# 	a.append(a[-1]*(1-after_five_r/100))
		# else:
		# 	a.append(a[-1]*(1-r_o/100))
		a.append(a[-1]*(1-r_o))

	a = np.array(a)
	return price-a


def get_insurance_estimate(p_state, p_policy, c_type, gt_tf):
	if type(p_state) == type(None):
		return 'N/A'
	sheet = pd.read_csv('assets/2017_avg_ins.csv').set_index('STATE')
	if len(p_policy) == 3:
		total = round(sheet.loc[p_state, 'TOTAL'],2)
	else:
		total = 0
		if 'Liability' in p_policy:
			total += sheet.loc[p_state, 'LIABILITY']
		if 'Comprehensive' in p_policy:
			total += sheet.loc[p_state, 'COMP']
		if 'Collision' in p_policy:
			total += sheet.loc[p_state, 'COLLISION']
	if c_type == 'Sedan':
		total *= 1.348
	elif c_type == 'Truck':
		total *= 1.318 
	elif c_type == 'SUV/Crossover':
		total *= 0.93
	elif c_type == 'Coupe':
		total *= 1.1149
	elif c_type == 'Hatchback':
		total *= 1.343
	elif c_type == 'Van/Minivan':
		total *= 0.92
	elif c_type == 'Convertible':
		total *= 1.1149
	elif c_type == 'Wagon':
		total *= 1.501
	if gt_tf == 'Yes':
		return round(total * 2,2)
	else:
		return round(total * 1,2)

def get_gas_estimate(g_type, mpg,state):
	if type(g_type) == type(None) or type(mpg) == type(None) or type(state) == type(None):
		return 0
	gas = pd.read_csv('assets/gasprices.csv').set_index('State')
	price = gas.loc[state, g_type]
	gallons = 13500/int(mpg)
	return round(gallons*price,2) 

def get_finance_estimate(p_financed, c_price):
	if p_financed == 'No':
		return [0]*5
	else:
		P = c_price*.9
		R = .05
		T = 5
		return [round((P*R*T)/5,2)] * 5
