import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)

datas = pd.read_csv("amirali_0_0_new_task.csv")

ors = [-2, -1.5, -1, -0.5, -0.25, 0.25, 0.5, 1, 1.5, 2]
l_to_total = len(ors) * [0]
for i in range(len(ors)):
    for j in range(200):
        if datas["Orientation"][j] == ors[i] and datas["SubjectAns"][j] == 'l':
            l_to_total[i] += 1

ors = np.array(ors)
l_to_total = np.array(l_to_total)
r_to_total = 1 - l_to_total/20
p0 = [max(r_to_total), np.median(ors) , 1, min(r_to_total)] # this is an mandatory initial guess
x_fit = np.linspace(np.min(ors), np.max(ors), 1000)
popt, pcov = curve_fit(sigmoid, ors, r_to_total, p0, method='dogbox')
y_fit = sigmoid(x_fit, *popt)
# print(y_fit)
plt.scatter(ors, r_to_total)
plt.plot(x_fit, y_fit, color = 'red', label='fit')
plt.ylim([0, 1.2])
plt.title("zero orientation adapter")

plt.show()