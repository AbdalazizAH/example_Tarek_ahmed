import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math as m
import pandas as pd
from sympy import symbols, solve


import data as d #!!


class WOterFoolting:
    def __init__(self, sw: list, kro_krw: list):
        self.sw = sw
        self.kro_krw = kro_krw

    def slope_inter(self):
        slope, intercept, r_value, p_value, std_err = linregress(
            self.sw, np.log(self.kro_krw)
        )
        return slope, intercept

    def get_b_a(self):
        slope, intercept = self.slope_inter()
        a = symbols("a")
        equation = a * np.exp(slope * self.sw[2]) - self.kro_krw[2]
        solution = solve(equation, a)
        a = solution
        b = slope
        return a[0], b

    def fw_fun(self):
        fwl = []
        a, b = self.get_b_a()
        for i in range(len(self.sw)):
            s = b * self.sw[i]
            fw = (1) / (1 + (1.0 / 2.0) * a * (m.exp(s)))
            fwl.append(fw)
        return fwl

    def dfw_dsw_fun(self):
        dfw_dswl = []
        a, b = self.get_b_a()
        for i in range(len(self.sw)):
            s = b * self.sw[i]
            dfw_dsw = (-(1 / 2) * a * b * (m.exp(s))) / (
                1 + (1 / 2) * a * (m.exp(s))
            ) ** 2
            dfw_dswl.append(dfw_dsw)
        return dfw_dswl

    def prsint_data(self):
        a, b = self.get_b_a()
        slope, intercept = self.slope_inter()
        print(f"a value = {a} and b value = {b}")
        print(f"slope : {slope}, intercept : {intercept}")

        dfs = pd.DataFrame(
            {
                "Sw": self.sw,
                "Kro/Krw": self.kro_krw,
                "fw": self.fw_fun(),
                "dfw/dsw": self.dfw_dsw_fun(),
            }
        )
        print(dfs)

    def plot1(self):
        plt.semilogy(self.sw, self.kro_krw)
        plt.title("kro/krw vs. Sw (Semi-log plot)")
        plt.xlabel("Sw (Water Saturation)")
        plt.ylabel("kro/krw")
        plt.grid(True)
        plt.show()

    def plot2(self):  #! div !
        # plt.plot(self.sw, self.fw_fun(), color="red")
        # plt.plot(sw, dfw_dswl )
        # x = [0.2, 0.707]
        # y = [0, 1.0]
        # plt.plot(x,y, color="black")
        # plt.grid(True)
        # plt.show()
        pass  


sw = d.ex["sw"]
kr = d.ex["kro_krw"]
sol = WOterFoolting(sw, kr)

sol.prsint_data()
sol.plot1()
sol.plot2()
