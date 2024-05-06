import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math as m
import pandas as pd
from sympy import symbols, solve


import data as d #!!


class WOterFoolting:

    def __init__(
        self,
        sw: list,
        kro_krw: list,
        ts: list,
        Iw: float,
        ph: float,
        A: float,
        assumed_sw,
    ):
        self.ts =ts
        self.Iw =Iw
        self.ph =ph 
        self.A  =A 
        self.assumed_sw = assumed_sw
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

    def dfw_dsw_fun_pro(self):
        dfw_dswl = []
        a, b = self.get_b_a()
        for i in range(len(self.assumed_sw)):
            s = b * self.assumed_sw[i]
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


    def time_destins_proFile(self):
        big_list = []
        for t, e in zip(range(len(self.ts)), self.ts):
            nsted_list = []
            s = self.dfw_dsw_fun_pro()
            for i in range(len(s)):
                X_sw = ((5.615 * self.Iw * self.ts[t]) / (self.ph * self.A)) * (
                    self.dfw_dsw_fun_pro()[i]
                )
                nsted_list.append(X_sw)
            big_list.append(nsted_list)
        return big_list

    def plots(self):
        w = self.time_destins_proFile()
        fig, (ax1, ax2) = plt.subplots(1, 2)

        # Plot 1: kro/krw vs Sw (linear scale)
        for i in range(len(w)):
            ax1.plot(
                w[i],
                sw_assumed,
                [w[i][0], w[i][0]],
                [sw_assumed[0], 0],
                color = "red"
                )
        ax1.set_title("Distance vs. Sw (Linear scale)")
        ax1.set_xlabel("Distance")
        ax1.set_ylabel("Sw (Water Saturation)")
        ax1.grid(True)

        # Plot 2: kro/krw vs Sw (semi-log scale)
        ax2.semilogy(self.sw, self.kro_krw)
        ax2.set_title("kro/krw vs. Sw (Semi-log plot)")
        ax2.set_xlabel("Sw (Water Saturation)")
        ax2.set_ylabel("kro/krw")
        ax2.grid(True)

        plt.tight_layout()
        plt.show()


# Data
sw = d.ex["sw"]
kr = d.ex["kro_krw"]
sw_assumed = d.assumed_sw
ts = [20.30,40 ,50 ,60]
A = d.td['A']
Iw = d.td["Iw"]
ph = d.td["ph"]
test = WOterFoolting(sw, kr, ts, Iw, ph, A, sw_assumed)


test.plots()
