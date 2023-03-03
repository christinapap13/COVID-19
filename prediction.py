import pandas as pd                             # import pandas library and define pd as its shortcut
import numpy as np                              # import numpy library and define np as its shortcut
import matplotlib.pyplot as plt                 # import matplotlib.pyplot library to plot and define plt as its shortcut
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model

#### LOAD DATA ####
data = pd.read_csv('Confirmed.csv', sep = ',')
data = data[['id', 'Confirmed']]

### PREPARE DATA ###
#We have to convert these into numpy array

x = np.array(data['id']).reshape(-1, 1)
y = np.array(data['Confirmed']).reshape(-1, 1)

plt.plot(y, '-m')
#plt.show()

#We are creating an object
polyFeat = PolynomialFeatures(degree=3) #x^2 and x if we put 3 then x^3, x^2, x
x = polyFeat.fit_transform(x)
#print(x)

### TRAINING DATA ###

model = linear_model.LinearRegression()
model.fit(x,y)
accuracy = model.score(x,y)
print(f'Accuracy:{round(accuracy*100,3)} %')

y0 = model.predict(x)
#plt.plot(y0, '--b')
#plt.show()


### PREDICTION ###

days = 10
print(f'Prediction - Confirmed after {days} days:', end='')
print(round(int(model.predict(polyFeat.fit_transform([[402+days]])))/1000000,2),'Million') #to get a Million value

x1 = np.array(list(range(1,402+days))).reshape(-1,1)
y1 = model.predict(polyFeat.fit_transform(x1))
plt.plot(y1,'--r')
plt.plot(y0, '--b')
plt.show()

#Xrisimopoioume polynomial regression giati einai enas eukolos tropos na kanoume problepsi me dataset pou den einai linear