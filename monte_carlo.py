"""Simulate performance of geothermal heating/cooling system.

Find out electricity consumption of three cyles: 
1. groundwater pump (summer)
2. groundwater pump (winter)
3. heat pump (summer)

Apply electricity price to total comsumptiom to derive total electricity cost.  

Original code: 
    https://stackoverflow.com/questions/52258435/monte-carlo-simulation-with-triangular-and-normal-probability-density-distibutio/52260330?noredirect=1#comment91526700_52260330

"""

import matplotlib.pyplot as plt
from numpy.random import triangular


N=1_000_000

# Seed effieciencies and prices

DISTRIBUTION_PARAM_COP_GWP = dict(left=4, mode=4.5, right=5)
DISTRIBUTION_PARAM_COP_HP = dict(left=35, mode=40, right=45)
DISTRIBUTION_PARAM_PRICE = dict(left=140, mode=150, right=160)

def seed_cop_hp():
    return triangular(**DISTRIBUTION_PARAM_COP_HP)

def seed_cop_gwp():
    return triangular(**DISTRIBUTION_PARAM_COP_GWP) 

def seed_price(): #(€/MWh)
    return triangular(**DISTRIBUTION_PARAM_PRICE)

# Groundwater cycle

ENERGY_HEATING_MWH = 866
ENERGY_COOLING_MWH = 912


def gw_consumption():
    return (ENERGY_HEATING_MWH + ENERGY_COOLING_MWH) / seed_cop_gwp() 

def gw_cost():
    """Groundwater cycle cost, euro"""
    return gw_consumption() * seed_price()

# Heatpump cycle

def hp_consumption():
    """Calculations of the electricty consumption of the heat pump. 
       Input: ENERGY_HEATING_MWH = 866 (pumped energy from subsurface)
       Output: energy input divided by COP of the heat pump
    """
    # FIXME: there should be -1?
    return ENERGY_HEATING_MWH / (seed_cop_hp() - 1)

def hp_cost():
    """heat pump cost, euro"""
    return hp_consumption() * seed_price()

def total_costs():
    """Summation of heat pump and groundwater pump costs"""
    return hp_cost() + gw_cost()

# Utility function

def sim(func, n=N):
    return [func() for _ in range(n)]

def plot(x, header=""):
    plt.hist(x, bins=75, density=True)
    plt.title(header)
    plt.figure()

def plot_from_func():
    prices = sim(seed_price)
    plot(prices, "Electricity prices")
    
    gw_pump_costs = sim(gw_cost)
    plot(gw_pump_costs, "Groundwater pump costs")
    
    heat_pump_costs = sim(hp_cost)
    plot(heat_pump_costs, "Heatpump costs")
    
    total_costs_list = sim(total_costs)
    plot(total_costs_list, "Total costs")

# Numpy form (very short)

def seed_triangular(param):
    return triangular(**param, size=N)

cop_gw = seed_triangular(DISTRIBUTION_PARAM_COP_GWP)
cop_hp = seed_triangular(DISTRIBUTION_PARAM_COP_HP)
p = seed_triangular(DISTRIBUTION_PARAM_PRICE)
ec_gw = (ENERGY_HEATING_MWH + ENERGY_COOLING_MWH) / cop_gw
ec_hp = ENERGY_HEATING_MWH / (cop_hp - 1)
total_costs_np = (ec_gw + ec_hp) * p


# NEXT:
#   - what are parameters of 70 systems?

if __name__ == "__main__":
    plot(total_costs_np, header=f"Total costs, {N/10**6} mln simulations")
