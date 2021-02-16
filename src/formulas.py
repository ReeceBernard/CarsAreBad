import pandas as pd
import numpy as np
from datetime import datetime as dt

def depreciation(make,new_tf,price,year):
	dep_year = int(dt.today().year)+1-int(year)
	high_dep = ['Buick', 'Cadillac','Land Rover', 'Mercedes-Benz', 'Infiniti', 'Lincoln', 'Audi']
	low_dep = ['Ford', 'Toyota', 'Honda', 'Mini', 'Nissan', 'Volkswagen']
	if make in high_dep:
		r_n = 35
		r_o = 21.4
	elif make in low_dep:
		r_n = 16
		r_o = 10.4
	else:
		r_n = 25
		r_o = 15.6
	after_five_r = 14
	if new_tf == 'New':
		a = [price*(1-r_n/100)]
	else:
		a = [price*(1-r_o/100)]
	for i in range(dep_year,dep_year+9):
		if i > 5:
			a.append(a[-1]*(1-after_five_r/100))
		else:
			a.append(a[-1]*(1-r_o/100))

	a = np.array(a)
	return price-a




