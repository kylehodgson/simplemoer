
# Description

This project encapsulates calling the [WattTime](https://www.watttime.org/) API in order to get marginal operating emissions rate (MOER) for power use at a certain lattitude and longitude. It does this by mapping the coordinates to a balancing authority (or power grid), and tracking the emissions of each of those grids. WattTime's MOER is provided in pounds of of emissions per megawatt-hour (e.g. CO2 lbs/MWh). It represents the emissions rate of the electricity generators which are responding to changes in load on the local grid at a certain time. More information on how they produce marginal emissions rates can be found on their [methodology page](https://www.watttime.org/marginal-emissions-methodology/).  While the actual CO2 lbs/MWh is provided only by paid API access, they do provide free access to an index value.  From this users can infer the result of power use at this moment; if the MOER index value is 33%, for instance, the grid's emissions are cleaner than usual right now. A value of 100% means that the grid is emitting more than it has at any point in the previous 30 days. You can think of this as "using cleaner power", though it may be more correct to think of it in the terms of "if I use power right now, am I likely to move the grid towards higher emissions". 

WattTime provides their own [Python client](https://github.com/WattTime/apiv2-example/blob/master/query_apiv2.py), which this library is inspired by. One benefit of their client is that it provides a means for registration, and in fact may be the easiest way to register for the free use of WattTime's API (as they don't currently provide registration via the web). Their example code isn't available as a python package, however, and I wanted to add some niceties such as using environment variables for username, password, lattitude and longitude.

# Using the client to obtain a MOER index

Usage is geared towards quickly obtaining the MOER index for a given lattitude and longitude. To use the client and provide these via environment variables, set up the environment variables, then run the code.

## Setting environment variables

```bash
export WATTTIMEUSERNAME=<your watttime username>
export WATTTIMEPASSWORD=<your watttime password>
export LATT=<lattitude where you will be using power>
export LONG=<longitude where you will be using power>
```

## Executing the client

```python
from simplemoer import WattTime

wt=WattTime()
index=wt.get_index()
print(f"index: {index}")
```

## Example results
Running the example code for my given lattitude and longitude, the WattTime client will acquire my balancing authority as IESO_NORTH. Results for this point in time indicate the grid's moer value is 49%. This index value is valid for 300 seconds from this point in time, as indicated by the `freq` and `point_time` values.
```
% python example.py
index: {'ba': 'IESO_NORTH', 'freq': '300', 'percent': '49', 'point_time': '2022-10-22T13:15:00Z'}
```

# Use case

I often use this client building python scripts related to IoT and home automation. I'm often turning on or off a device, and it might be a device where it wouldn't hurt anything to wait 5 minutes. So I will often query the MOER index value and compare it against a maximum MOER value; often 50 in my case. So, instead of turning on an infrared heating panel, or a dehumidifier, as soon as conditions warrant it (for instance the room is reaching a temperature that's too cool), I might compare the current MOER index against the maximum MOER and choose to delay turning on the heating panel or dehumidifier. For example in the case of a thermostat turning on and off a heating source, if the MOER value is over 50 I might subtract 1 or 2 degrees celcius from the desired temperature. In that way as soon as energy is greener we can go back to warming up the room, and if we don't get such favorable power conditions we will eventually heat up the room, just perhaps not as quickly, and to a lower temperature. When power is cleaner again, we'll go ahead and warm the room to the desired temperature (or possibly even a degree higher). 


