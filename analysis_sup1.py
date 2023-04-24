import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)

data = pd.read_csv("Datas/23June2021/amirali_1_total_task.csv")

ors = [-3, -2, -1, 0, 1, 2, 3]
r_to_total_pos = len(ors) * [0]
r_to_total_neg = len(ors) * [0]
r_to_total_nuc = len(ors) * [0]
counter_pos    = len(ors) * [0]
counter_neg    = len(ors) * [0]
counter_nuc    = len(ors) * [0]

# datas2 = pd.read_csv("mahdi_0_0_task.csv")

# ors2 = [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2]
# l_to_total = len(ors2) * [0]
# for i in range(len(ors2)):
#     for j in range(90):
#         if datas2["Orientation"][j] == ors2[i] and datas2["SubjectAns"][j] == 'l':
#             l_to_total[i] += 1

# ors2 = np.array(ors2)
# l_to_total = np.array(l_to_total)

# r_to_total = 1 - l_to_total/10
# p0 = [max(r_to_total), np.median(ors2) , 1, min(r_to_total)] # this is an mandatory initial guess
# x_fit2 = np.linspace(np.min(ors2), np.max(ors2), 1000)
# popt, pcov = curve_fit(sigmoid, ors2, r_to_total, p0, method='dogbox')
# y_fit = sigmoid(x_fit2, *popt)

for i in range(len(ors)):
    for j in range(len(data)):
        if data["Orientation"][j] == ors[i] and data["SubjectAns"][j] == 'r' and data['AdaptorOrientation'][j] == 20 and data['TestPlace'][j] == True:
            r_to_total_pos[i] += 1
        if data["Orientation"][j] == ors[i] and data["SubjectAns"][j] == 'r' and data['AdaptorOrientation'][j] == -20 and data['TestPlace'][j] == True:
            r_to_total_neg[i] += 1
        if data["Orientation"][j] == ors[i] and data["SubjectAns"][j] == 'r' and data['AdaptorOrientation'][j] == 0:
            r_to_total_nuc[i] += 1
        if data["Orientation"][j] == ors[i] and data['AdaptorOrientation'][j] == 20 and data['TestPlace'][j] == True:
            counter_pos[i]    += 1
        if data["Orientation"][j] == ors[i] and data['AdaptorOrientation'][j] == -20 and data['TestPlace'][j] == True:
            counter_neg[i]    += 1
        if data["Orientation"][j] == ors[i] and data['AdaptorOrientation'][j] == 0:
            counter_nuc[i]    += 1

ors = np.array(ors)
print(sum(counter_pos))
print(sum(counter_neg))
r_to_total_pos = np.array(r_to_total_pos) / counter_pos
r_to_total_neg = np.array(r_to_total_neg) / counter_neg
r_to_total_nuc = np.array(r_to_total_nuc) / counter_nuc

x_fit = np.linspace(np.min(ors), np.max(ors), 1000)

p0_pos = [max(r_to_total_pos), np.median(ors) , 1, min(r_to_total_pos)] # this is an mandatory initial guess
popt_pos, pcov = curve_fit(sigmoid, ors, r_to_total_pos, p0_pos, method='dogbox')
y_fit_pos = sigmoid(x_fit, *popt_pos)

plt.scatter(ors, r_to_total_pos)
plt.plot(x_fit, y_fit_pos, color = 'red', label='fit')
plt.ylim([0, 1.2])
plt.title("20 orientation adapter")


p0_neg = [max(r_to_total_neg), np.median(ors) , 1, min(r_to_total_neg)] # this is an mandatory initial guess
popt_neg, pcov = curve_fit(sigmoid, ors, r_to_total_neg, p0_neg, method='dogbox')
y_fit_neg = sigmoid(x_fit, *popt_neg)

plt.scatter(ors, r_to_total_neg)
plt.plot(x_fit, y_fit_neg, color = 'blue', label='fit')
plt.ylim([0, 1.2])
plt.title("-20 orientation adapter")

# p0_nuc = [max(r_to_total_nuc), np.median(ors) , 1, min(r_to_total_nuc)] # this is an mandatory initial guess
# popt_nuc, pcov = curve_fit(sigmoid, ors, r_to_total_nuc, p0_nuc, method='dogbox')
# y_fit_nuc = sigmoid(x_fit, *popt_nuc)

# plt.scatter(ors, r_to_total_nuc)
# plt.plot(x_fit, y_fit_neg, color = 'green', label='fit')
# plt.ylim([0, 1.2])
# plt.title("zero orientation adapter")

# plt.scatter(ors2, r_to_total)
# plt.plot(x_fit2, y_fit, color = 'green', label='fit')
# plt.ylim([0, 1.2])
# plt.title("zero orientation adapter")

plt.show()

# y_fit = y_fit.tolist()
y_fit_neg = y_fit_neg.tolist()
y_fit_pos = y_fit_pos.tolist()

# x_0 = x_fit2[y_fit.index(min(y_fit, key = lambda x:abs(x-0.5)))]
x_pos = x_fit[y_fit_pos.index(min(y_fit_pos, key = lambda x:abs(x-0.5)))]
x_neg = x_fit[y_fit_neg.index(min(y_fit_neg, key = lambda x:abs(x-0.5)))]

print("Calculated TAE is:")
print(str((x_pos - x_neg)/2) + " degree")