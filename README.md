# MonteCarlo-Energysavings

TODO: texts to merge for algorithm descrition:

I have two cycles: One Subsurface cycle, where groundwater is pumped to the surface and a building cycle, where heat and cold are circulated in the building. Both cycles are connected by a heat exchanger.

During summertime, cold groundwater is pumped to the subsurface and cold temperatures are transferred in the heat exchanger to the building cooling system. The cold temperatures of the groundwater can be used directly, hence there is only electricity demand of the groundwater pump.

During wintertime, warm groundwater is pumped to the subsurface and warm temperatures are transferred by the heat exchanger to the building cycle. Since temperatures are not high enough, a heat pump increases the temperature level to the required temperatures of the building heating system. Thus, during wintertime, there is an electricity demand for both, the groundwater pump and the heat pump.

While the heat pump has a COP between 4 and 5, the COP of the groundwater pump ranges between 35 and 45. We know the amount of cold and warm energy from the subsurface transferred to the building cycle. It is 866 MWh for heating and 912 MWh for cooling.

During summertime, the demand for electricity can be calculated by 912 MWh / 40 =22.8 MWh. With an electricity price of 0,15 €/kwh, the electricity costs amount to 3420 €.

In wintertime, we have again the electricity demand for the groundwater pump: 866 MWh/40 = 21.7 MWh. 21.7 * 0.15 €/kwh =3248 €
And secondly the electricity for the heat pump. The energy output can be calculated by:
Energy input * COP / (COP - 1) = 866 * 4.5 / (4.5-1)= 1113.4 MWh. The electricity demand is:
1113.4 / 4.5 = 247.42, which gives us electricity costs of 37114.3 €.

The total electricity costs are the sum of each component:
Electricity for gw pump (summertime) + Electricity for gw pump (wintertime) + electricity hp (wintertime)
= 3420€ + 3248€ +37114.3 €= 43782 €.

Since the electricity costs and the COP have an uncertainty, I want to create a triangular probability distribution for the variables. In the end, I also get an uncertainty for the energy costs. 
However, these uncertainties are not of triangular but of a normal distribution.

