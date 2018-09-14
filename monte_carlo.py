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
from numpy.random import triangular, normal


N=100_000

# Groundwater cycle

ENERGY_HEATING_MWH = 866
ENERGY_COOLING_MWH = 912

COP_DISTRIBUTION_PARAM = dict(left=4, mode=4.5, right=5)

# What is missnig is the COP of the groundwater pump
COP_GW_PUMP_DISTRIBUTION_PARAM = dict(left=35, mode=40, right=45)

# I changed this to a triangular distributon. 
PRICE_DISTRIBUTION_PARAM = dict(left=140, mode=150, right=160)

def seed_cop_hp():
    return triangular(**COP_DISTRIBUTION_PARAM)

def seed_price(): #(€/MWh)
    return triangular(**PRICE_DISTRIBUTION_PARAM) 

def seed_cop_gw_pump():
    return triangular(**COP_GW_PUMP_DISTRIBUTION_PARAM) 

def gw_consumption():
    return (ENERGY_HEATING_MWH + ENERGY_COOLING_MWH) / seed_cop_gw_pump() 

def gw_cost():
    """Groundwater cycle cost, euro"""
    return gw_consumption() * seed_price()

def hp_consumption():
    """Calculations of the electricty consumption of the heat pump. 
       Input: ENERGY_HEATING_MWH = 866 (pumped energy from subsurface)
       Output: energy input divided by COP of the heat pump
    """
    return ENERGY_HEATING_MWH / (seed_cop_hp() - 1)

def hp_cost():
    """heat pump cost, euro"""
    return hp_consumption() * seed_price()

# Summation of heat pump and groundwater pump costs
def total_costs():
    return hp_cost() + gw_cost()

def sim(func, n=N):
    return [func() for _ in range(n)]

def plot(x, header=""):
    # TODO: add header to plot
    plt.hist(x, bins=75, density=True)
    plt.figure()

# NOTE: same can be down with fewer fucntions and numpy arrays
# With the calculation of the heat pump costs, the code is getting quite long again. 
# It would be good to shorten it by using numpy.

if __name__ == "__main__":
    # triangular
    gw_consumption_list = sim(gw_consumption)
    plot(gw_consumption_list)
    # normal
    prices = sim(seed_price)
    plot(prices)
    # kind of normal (triangular * normal)
    total_cost_simulated = sim(gw_cost)
    plot(total_cost_simulated)
    # kind of normal (normal + normal)
    heat_pump_costs = sim(hp_cost)
    plot( heat_pump_costs)
    # kind of normal (normal + normal)
    total_costs = sim(total_costs)
    plot(total_costs)


