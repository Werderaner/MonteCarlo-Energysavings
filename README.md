Geothermal household system simulation 
=====================================


Introduction 
------------

There is a building which is supplied by a geothermal system with heat 
(wintertime) and cold (summertime).

There are two cycles:

1. subsurface cycle, where groundwater is pumped to the surface and 
2. building cycle, where heat and cold are circulated in the building. Both cycles are connected by a heat exchanger.

During summertime, cold groundwater is pumped to the subsurface and cold temperatures are transferred in the heat exchanger to the building cooling system. The cold temperatures of the groundwater can be used directly, hence there is only electricity demand of the groundwater pump.

During wintertime, warm groundwater is pumped to the subsurface and warm temperatures are transferred by the heat exchanger to the building cycle. Since temperatures are not high enough, a heat pump increases the temperature level to the required temperatures of the building heating system. Thus, during wintertime, there is an electricity demand for both, the groundwater pump and the heat pump.

```
                       Winter             Summer
  ------------------   -------------      ---------
  Heat pump            Heating            Not working
  ------------------   -------------      ---------
  Growndwater pump     Water supply       Water supply 
                       (heating)          (cooling)
  ------------------   -------------      ---------
```

Efficiencies and house energy demand
------------------------------------

While the heat pump has a coefficient of performance (COP) between 4 and 5, the COP of the groundwater pump ranges between 35 and 45. We know the amount of cold and warm energy from the subsurface transferred to the building cycle. It is `866` MWh for heating and `912` MWh for cooling.

EP-QUESTION: the constants are based on the house size and average room temperatures?

Groundwater cycle
-----------------

During summertime, the demand for electricity (EP: for a groundwater pump) can be calculated by `912 MWh / 40 = 22.8 MWh`. With an electricity price of 0,15 €/kwh, the electricity costs amount to 3420 €.

In wintertime, we have again the electricity demand for the groundwater pump: 866 MWh/40 = 21.7 MWh. 21.7 * 0.15 €/kwh = 3248 €

Heat pump cycle 
---------------

To calculate the electricity demand of the heat pump I need to know the energy 
output. This can be calculated by `energy_input * COP / (COP-1)`. The energy output 
divided by the COP gives me the electricity demand. The electricity costs times 
the specific electricity price gives me the total electricity costs for the heat pump.

Electricity demand for the heat pump is calculated as follows. The energy output can be calculated by: 

> Energy input * COP / (COP - 1) = 866 * 4.5 / (4.5-1)= 1113.4 MWh. 

The electricity demand is:

> 1113.4 / 4.5 = 247.42, 

which gives us electricity costs of 37114.3 €.

Total costs
-----------

The total **electricity costs** are the sum of each component:
Electricity for gw pump (summertime) + Electricity for gw pump (wintertime) + electricity hp (wintertime)
= 3420€ + 3248€ + 37114.3 €= 43782 €.

Uncertainties
-------------

For the calculation I assume uncertainities for: 
 - COP heat pump (triangular)
 - COP groundwater pump (triangular)
 - electricity price (gaussian)

Since the electricity costs and the COP have an uncertainty, I want to create a triangular probability distribution for the variables. In the end, I also get an uncertainty for the energy costs. However, these uncertainties are not of triangular but of a normal distribution.

Links
-----

- [EPA Heat Pumps](https://www.epa.gov/rhc/geothermal-heating-and-cooling-technologies#Ground-Source-Heat-Pumps)

