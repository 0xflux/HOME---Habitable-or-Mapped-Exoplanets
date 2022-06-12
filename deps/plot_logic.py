import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from . import phys_and_math as pam

def scatter_plot_for_planet_mass_vs_solar_temp(df, savepath, graph_title):
	'''
	A function to plot planet mass vs the solar temperature, is there any correlation?

	Takes in a dataframe, for example:

	combined = {'stellar_effective_temperature_black_body_radiation': np.array(df['stellar_effective_temperature_black_body_radiation']), 
		'planet_mass_in_kg' : np.array(df['planet_mass_in_kg'])}

	t_df = pd.DataFrame(combined) <------ create a df from combined data before calling function
	new_df = remove_nans_from_df(t_df)

	'''

	# combine two arrays from the dataframe into a dictionary
	combined = {'stellar_effective_temperature_black_body_radiation': np.array(df['stellar_effective_temperature_black_body_radiation']), 
		'planet_mass_in_kg' : np.array(df['planet_mass_in_kg'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset
	x_solar_temp_array = np.array(t_df['stellar_effective_temperature_black_body_radiation'])
	y_planet_mass_array = np.array(t_df['planet_mass_in_kg'])

	# add some data for earth (orange dot on plot)
	earth_mass = 5.972e24
	sol_temp = 5778

	# plot
	plt.clf()

	plt.suptitle(graph_title, fontsize=10)
	plt.xlabel("Temperature of the host star / K")
	plt.ylabel("Mass of the exo-planet / kg")

	plt.scatter(x_solar_temp_array, y_planet_mass_array, s=5)
	plt.scatter(sol_temp, earth_mass, s=15)

	plt.savefig(savepath)


def graph_habitable_exoplanets(df):
	'''
	A function to graph the habitable planets
	'''
	# create a dataframe for habitable planets
	habitable = df.loc[df['is_planet_habitable'] == 1]

	scatter_plot_for_planet_mass_vs_solar_temp(habitable, 
		'./output/habitable_scatter_plot_mass_vs_temp.png', 
		'A graph to show the mass (1e28) (kg) of known exoplanets in the habitable zone orbiting \nstars of a certain temperature (K), ' + 
		'with earth \ndenoted as an orange dot.')

	# A histogram to show the frequency of host stars with different numbers of exoplanets.
	# TODO - it would be interesting to add additional data to this histogram, size of star, temperature, habitability etc.
	# Could I analyse the data to show those in habitabiltiy zone AND multiple planets? Would they look similar to our solar system in terms
	# of their composition?
	histogram_exoplanets_per_star(habitable, './output/habitable_histogram_exoplanets_per_star.png', 
		'A histogram to show the frequency of exoplanets with at least one \nin the habitable range orbiting a host star.')

	return habitable # return the habitable df


def histogram_exoplanets_per_star(df, savepath, graph_title):

	# provide a dataframe to count the planets around host stars
	solar_system_data = df.groupby(['name_of_host_star']).size().reset_index(name='count')

	# clear previous plot and make new plot
	plt.clf()
	plt.suptitle(graph_title,fontsize=10)
	plt.ylabel("Frequency")
	plt.xlabel("Number of detected exoplanets around star")
	
	num_bins, edges, bars = plt.hist(solar_system_data['count'], bins=range(1,10), rwidth=0.7)

	# add numbers onto plot as low values are unreadable
	plt.bar_label(bars)

	# export
	plt.savefig(savepath)


def graph_density(exo, savepath):

	'''
	A function to plot the density against mass
	'''

	# clear previous plot and make new plot
	plt.clf()
	combined = {'planet_density': np.array(exo['planet_density']), 
	'planet_mass_in_kg' : np.array(exo['planet_mass_in_kg'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset, independant variable on the x
	x_planet_mass = np.array(t_df['planet_mass_in_kg']) 
	y_dens = np.array(t_df['planet_density'])

	# add some data for earth (orange dot on plot)
	earth_mass = 5.972e24
	earth_dens = 5520 # source http://astronomy.nmsu.edu/mchizek/105/LABS/EarthDensity.pdf

	plt.suptitle("A graph to show the density vs its mass of all detected exoplanets, with Earth plotted as an organge point.", fontsize=10)
	plt.xlabel("Planet's mass / kg")
	plt.ylabel("Planet's density / kg m^-3")

	plt.scatter(x_planet_mass, y_dens, s=10)
	plt.scatter(earth_mass, earth_dens, s=10)

	plt.savefig(savepath)

	# scatter graph is too busy to provide any decent interpretations, so I'll use a histogram instead:

	


def graph_gravity(exo, hab, savepathall, savepathhab):
	''' 

	A function to graph the gravity of exoplanets.

	Produce as a scatter against their mass, it should be a straight line graph.. will be interesting to see
	if the results are different. Doen as g force (compared to earths g-force of 1 g) as apposed to m s^-2

	'''

	# clear previous plot and make new plot
	plt.clf()
	combined = {'gravity_compared_to_earth': np.array(exo['gravity_compared_to_earth']), 
	'planet_mass_in_kg' : np.array(exo['planet_mass_in_kg'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset, independant variable on the x
	x_planet_mass = np.array(t_df['planet_mass_in_kg']) 
	y_g_force = np.array(t_df['gravity_compared_to_earth'])

	# add some data for earth (orange dot on plot)
	earth_mass = 5.972e24
	earth_g = 1

	# plot
	plt.clf()

	plt.suptitle("A graph to show the G-force as a measure compared to earth (1 G) (vs. its mass) \n of all detected exoplanets with Earth plotted as an organge point.", fontsize=10)
	plt.xlabel("Planet's mass / kg")
	plt.ylabel("G-Force compared to Earth / G's")

	plt.scatter(x_planet_mass, y_g_force, s=5)
	plt.scatter(earth_mass, earth_g, s=15)

	# Humans could build the strength to survive up to 4 G's potentially (though i have seen studies suggeting we can only survive
	# 3 G's for up to 2 minuets, so not sure on the reliability of this.) Add a line to indicate this cut off point. 
	# Source: https://www.discovermagazine.com/the-sciences/whats-the-maximum-gravity-we-could-survive
	plt.axhline(y=4, color='r', linestyle='-') # plot line

	plt.savefig(savepathall)


	# plot habitable planets

	# clear previous plot and make new plot
	plt.clf()
	combined = {'gravity_compared_to_earth': np.array(hab['gravity_compared_to_earth']), 
	'planet_mass_in_kg' : np.array(hab['planet_mass_in_kg'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset, independant variable on the x
	x_planet_mass = np.array(t_df['planet_mass_in_kg']) 
	y_g_force = np.array(t_df['gravity_compared_to_earth'])

	# clear last plot
	plt.clf()

	plt.suptitle("A graph to show the G-force as a measure compared to earth (1 G) (vs. its mass) of all \ndetected habitable exoplanets with Earth plotted as an organge point.", fontsize=10)
	plt.xlabel("Planet's mass / kg")
	plt.ylabel("G-Force compared to Earth / G's")

	plt.scatter(x_planet_mass, y_g_force, s=5)
	plt.scatter(earth_mass, earth_g, s=15)

	# Humans could build the strength to survive up to 4 G's potentially (though i have seen studies suggeting we can only survive
	# 3 G's for up to 2 minuets, so not sure on the reliability of this.) Add a line to indicate this cut off point. 
	# Source: https://www.discovermagazine.com/the-sciences/whats-the-maximum-gravity-we-could-survive
	plt.axhline(y=4, color='r', linestyle='-') # plot line

	plt.savefig(savepathhab)


	### plot g's vs radius ###

	# clear previous plot and make new plot
	plt.clf()
	combined = {'gravity_compared_to_earth': np.array(exo['gravity_compared_to_earth']), 
	'planet_actual_radius' : np.array(exo['planet_actual_radius'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset, independant variable on the x
	x_planet_radius = np.array(t_df['planet_actual_radius']) 
	y_g_force = np.array(t_df['gravity_compared_to_earth'])

	# add some data for earth (orange dot on plot)
	earth_mass = 5.972e24
	earth_g = 1

	# plot
	plt.clf()

	plt.suptitle("A graph to show the G-force as a measure compared to earth (1 G) (vs. its radius) \n of all detected exoplanets with Earth plotted as an organge point.", fontsize=10)
	plt.xlabel("Planet's radius / km")
	plt.ylabel("G-Force compared to Earth / G's")

	plt.scatter(x_planet_radius, y_g_force, s=5)
	plt.scatter(6371, earth_g, s=15)

	# Humans could build the strength to survive up to 4 G's potentially (though i have seen studies suggeting we can only survive
	# 3 G's for up to 2 minuets, so not sure on the reliability of this.) Add a line to indicate this cut off point. 
	# Source: https://www.discovermagazine.com/the-sciences/whats-the-maximum-gravity-we-could-survive
	plt.axhline(y=4, color='r', linestyle='-') # plot line

	plt.savefig("./output/g_force_all_exoplanets_radius.png")


	### plot g's vs radius ###

	# clear previous plot and make new plot
	plt.clf()
	combined = {'gravity_compared_to_earth': np.array(hab['gravity_compared_to_earth']), 
	'planet_actual_radius' : np.array(hab['planet_actual_radius'])}

	# temp dataframe to remove nans - if there are nan values in the dataframe, remove the row as we need both x and y values to plot.
	t_df = pd.DataFrame(combined)
	t_df.dropna(inplace = True)

	# Create our final dataset, independant variable on the x
	x_planet_radius = np.array(t_df['planet_actual_radius']) 
	y_g_force = np.array(t_df['gravity_compared_to_earth'])

	# add some data for earth (orange dot on plot)
	earth_mass = 5.972e24
	earth_g = 1

	# plot
	plt.clf()

	plt.suptitle("A graph to show the G-force as a measure compared to earth (1 G) (vs. its radius) \n of all detected habitable exoplanets with Earth plotted as an organge point.", fontsize=10)
	plt.xlabel("Planet's radius / km")
	plt.ylabel("G-Force compared to Earth / G's")

	plt.scatter(x_planet_radius, y_g_force, s=5)
	plt.scatter(6371, earth_g, s=15)

	# Humans could build the strength to survive up to 4 G's potentially (though i have seen studies suggeting we can only survive
	# 3 G's for up to 2 minuets, so not sure on the reliability of this.) Add a line to indicate this cut off point. 
	# Source: https://www.discovermagazine.com/the-sciences/whats-the-maximum-gravity-we-could-survive
	plt.axhline(y=4, color='r', linestyle='-') # plot line

	plt.savefig("./output/g_force_all_exoplanets_habitable_radius.png")

	# plot
	plt.clf()

	g_f = t_df['gravity_compared_to_earth'].to_dict()

	# Create a pie chart of planets greater than, and less than, 4 G's of habitable exos
	#less_than = len(combined[combined.iloc[:,0] <= 4])
	less_than = len([g for g in g_f.values() if int(g) <= 4])
	more_than = len([g for g in g_f.values() if int(g) >= 4.01])
	#more_than = len(combined[combined.iloc[:,0] >= 4.01])

	arr = np.array([less_than, more_than])

	key = [f"Planets under 4G's: {less_than}", f"Planets greater than 4 G's: {more_than}"]
	
	plt.suptitle("A pie chart to show the number of habitable exoplanets that are over and under 4 G's.", fontsize=10)


	plt.pie(arr, labels = key)

	plt.savefig("./output/g_force_all_exoplanets_habitable_pie_chart.png")

