import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from pandas import datetime
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import itertools

def parser(x):
    return datetime.strptime(x,'%Y-%m')

sales = pd.read_csv('sales-cars.csv',index_col = 0,parse_dates=[0],date_parser = parser)

# -----AutoCorrelation graph-----
# Plots an AutoCorrelation graph by making a copy of the data and shifting it down by 1...n times. For each shift, subtracts the copy value by original value
# Graph shows data is non statationary because its slowly decreasing. Data is stationary if each point along x axis is opposite in magnitude
# plot_acf(sales)

# -----Convert non-stationary to stationary data-----
# To make data stationary, apply differences which subtracts current value by previous value. If periods = 2, then take result of period = 1 and perform the same subtraction
# sales_diff = sales.diff(periods = 1)
# sales_diff = sales_diff[1:]
# plot_acf(sales_diff)

# -----AR Model Construction-----
X = sales.values
# First 27 values will be used to train the AR model
train = X[0:27]
# Values after 27 will be used for comparing to the prediction
test = X[26:]

model_ar = AR(train)
model_ar_fit = model_ar.fit()
predictions = model_ar_fit.predict(start=26,end=36)
# plt.plot(test)
# plt.plot(predictions, color = 'red')
# plt.show()

# -----ARIMA Model Construction-----
# p - periods taken for AutoRegression Model e.g 1 means taking previous month to predict next month, 2 means taking previous 2 months to predict next month
# d - integrated order(differences)
# q - moving average. Argument specifies number of values to average at a time e.g 3 means adding 3 values divided by 3 then removing oldest value and adding the next value / 3
model_arima = ARIMA(train,order = (8,2,2))
model_arima_fit = model_arima.fit(disp=0)

predictions = model_arima_fit.forecast(steps=10)[0]
plt.plot(test)
plt.plot(predictions, color = 'red')

# AIC is math equation whose result indicates the accuracy of the ARIMA model. Lower results is good.
print(model_arima_fit.aic)

# -----Finding the right p,d,q values-----
# p=d=q=range(0,5)
# pdq = list(itertools.product(p,d,q))
# print(pdq)
#
# for param in pdq:
#     try:
#         model_arima = ARIMA(train, order = param)
#         model_arima_fit = model_arima.fit(disp=0)
#         print(param,model_arima_fit.aic)
#     except:
#         continue

# Mean Squared Error tells you how close a regression line(ARIMA model line) is to an actual dataset of points.
# It does this by taking the distances from the points to the regression line (these distances are the “errors”) and
# squaring them. The squaring is necessary to remove any negative signs
print(mean_squared_error(test,predictions))

plt.show()