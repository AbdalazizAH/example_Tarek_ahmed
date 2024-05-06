# Water-Oil Relative Permeability Calculation

This Python script calculates water-oil relative permeability and generates plots based on provided data.

## Description

The script defines a class `WOterFoolting` that calculates water-oil relative permeability (`kro/krw`) based on saturation values (`Sw`). It implements methods to compute the slope and intercept of the data, calculate the `fw` , `dfw/dsw` , and print the results. Additionally, it provides methods to plot the data.

## Prerequisites

- Python 3.x
- Required packages: `numpy`, `matplotlib`, `scipy`, `pandas`, `sympy`

## Usage

1. Ensure you have Python installed on your system.
2. Install the required packages using `pip install numpy matplotlib scipy pandas sympy`.
3. Import the `WOterFoolting` class from the script.
4. Prepare your data for saturation (`sw`) and water-oil relative permeability (`kro_krw`).
5. Create an instance of the `WOterFoolting` class with your data.
6. Call the desired methods to compute and visualize the results.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import math as m
import pandas as pd
from sympy import symbols, solve

from data import ex  # Import your data

from woter_floot import WOterFoolting  # Import the class from your script


# Data
sw = d.ex["sw"]
kr = d.ex["kro_krw"]
sw_assumed = d.assumed_sw
ts = [20.30,40 ,50 ,60] #after 
A = d.td['A']
Iw = d.td["Iw"]
ph = d.td["ph"]
test = WOterFoolting(sw, kr, ts, Iw, ph, A, sw_assumed)

#test plots
test.plots()
