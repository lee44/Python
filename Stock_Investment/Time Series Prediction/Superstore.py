import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib

df = pd.read_excel("Superstore.xls")
furniture = df.loc[df['Category'] == 'Furniture']
print(df)