import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from pathlib import Path

def main():

	# This dataset has a gaps of imbalanced missing data and duplicates. ~ 32 000 rows of data in the imbalanced dataset.
	# This script is designed to work with the dataset from: 
	# https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PS, I have included a copy of the csv.

	'''
		* Work out habitability zone - can I use a ML model to determine whether there is habitability?
		* Graph out the black body spectrum of a system's star - from the black body work out its temperature
		* Do a map of systems
		# Histograms:
			* Histogram distance to exo from earth vs number of exo
			* Histogram radius of planet against earth, and jupiter
			* Histogram temperature of planet (if observed)
			* Histogram eccentricity
		# Scatter for mass vs luminosity vs distance of orbit
		# Balance gaps - is there data missing which is in another row that has been discounted?
		# Do some stats on the habitable planets
		# Can i look at any spectra re the planets?
		# Look at solar data
		# Can i find pictures of the planets from scraping the web:
			* https://exoplanetarchive.ipac.caltech.edu/docs/data.html
			* http://www.openexoplanetcatalogue.com/systems/ (note, this contains data that NASA / Caltech doesnt have -> look into obtaining 
			extra data)
		# Calculate gravity of all planets, calculate gravity of habitable - any that would be suitable for us to live on?
			* First part done - pick up next from here, calculate are they suitable for us?
		# Split into classes / modules
		# Scrape web / other resources to find additional data such as mass, radius for a more complete dataset.

	'''

	LENGTH_OF_LIST = 32542 # raw data
	CLEAN_DATA_FILE_PATH = './cleaned_data.xlsx'
	INPUT_DATA_PATH = './deps/PS_2022.06.01_08.42.24.xlsx'

	# set some rules for debug output - I dont want rows, but columns in full:
	pd.set_option('display.max_columns', None)
	pd.options.mode.chained_assignment = None  # turn off warnings as they are used in a safe way

	# Check if there is the santisised xl, if not it is first run (or changes to code) so import large dataset, otherwise import sanitised 
	# dataset to save load times..
	# Just remember to delete this file if you make changes to clean_data_exoplanets or similar.
	if Path(CLEAN_DATA_FILE_PATH).is_file():
		print("Importing sanitised data..")
		exoplanets = pd.read_excel(CLEAN_DATA_FILE_PATH)
	
	else:
		print("Importing un-sanitised data.. This could take a while")

		# first create data frame with CSV in, ~ 30 000 rows.
		master_data = pd.read_excel(INPUT_DATA_PATH)

		# Examine the shape
		print("Shape of the import: {}".format(master_data.shape))

		# Clean & format the data
		exoplanets = data_cleansing_methods(master_data, LENGTH_OF_LIST, CLEAN_DATA_FILE_PATH)
		

	# produce a scatter plot for planet mass against the temperature (K) of its host star, is there a correlation? 
	# TODO - this should also take into account the distance from the host star - probably use 'orbital_period_widest_radius_in_AU' for this.
	scatter_plot_for_planet_mass_vs_solar_temp(exoplanets, 
		'./output/scatter_plot_mass_vs_temp.png', 
		'A graph to show the mass (1e29) (kg) of known exoplanets orbiting stars of a \ncertain temperature (K), with earth denoted as an orange dot.')

	# A histogram to show the frequency of host stars with different numbers of exoplanets.
	# TODO - it would be interesting to add additional data to this histogram, size of star, temperature, habitability etc.
	# Could I analyse the data to show those in habitabiltiy zone AND multiple planets? Would they look similar to our solar system in terms
	# of their composition?
	histogram_exoplanets_per_star(exoplanets, './output/histogram_exoplanets_per_star.png', 
		'A histogram to show the frequency of exoplanets orbiting a host star.')

	graph_habitable_exoplanets(exoplanets)

	# TODO - more general analytics of data, maybe some statistics, histograms etc.

	# lets have a look at the solar data
	'''
	solar_data_manipulation(exoplanets)
	habitability_data_manipulation(exoplanets)
	'''

def data_cleansing_methods(master_data, LENGTH_OF_LIST, output_file):
	'''
	Methods to clean the data up and produce an excel document for manual checking. Keeps the main method tidy.
	'''
	# check the dataset was read correctly
	check_data_read_okay(master_data, LENGTH_OF_LIST)

	### Data clensing ###

	# Start with only the colums I am interested in and rename them
	exoplanets = clean_data_exoplanets(master_data, LENGTH_OF_LIST)

	# output a file for debugging, and to read in after cleansed for a faster spool up of the program.
	exoplanets.to_excel(output_file)

	return exoplanets


def check_data_read_okay(df, len_of_list):
	###There are 32 542 rows, note there are 32 543 INCLUDING the column headers not included in the count.###
	if len(df) == len_of_list:
		print("Info - Data read correctly")
	else:
		sys.exit("Error - Error reading data.. exiting.")


def clean_data_exoplanets(df, len_of_list):
	
	'''
	A method to clean the dataset, and perform some balancing. 
	'''

	# Choose the columns I want to load
	exoplanets = df[[
	'pl_name',
	'hostname',
	'discoverymethod',
	'disc_year',
	'soltype',
	'pl_orbper',
	'pl_orbpererr1',
	'pl_orbpererr2',
	'pl_orbsmax',
	'pl_orbsmaxerr1',
	'pl_orbsmaxerr2',
	'pl_rade',
	'pl_radj',
	'pl_bmasse',
	'pl_bmassj',
	'pl_eqt',
	'pl_eqterr1',
	'pl_eqterr2',
	'st_teff',
	'st_tefferr1',
	'st_tefferr2',
	'st_rad',
	'st_raderr1',
	'st_raderr2',
	'st_mass',
	'st_masserr1',
	'st_masserr2',
	'sy_dist',
	'sy_disterr1',
	'sy_disterr2']]

	# Rename colums to something more sensible..

	rename_cols = {
		'pl_name' : 'name_of_planet',
		'hostname' : 'name_of_host_star',
		'soltype' : 'solution_type',
		'pl_orbper' : 'orbital_period',
		'pl_orbpererr1' : 'orbital_period_error_max',
		'pl_orbpererr2' : 'orbital_period_error_min',
		'pl_orbsmax' : 'orbital_period_widest_radius_in_AU',
		'pl_orbsmaxerr1' : 'orbital_period_widest_radius_in_AU_error_max',
		'pl_orbsmaxerr2' : 'orbital_period_widest_radius_in_AU_error_min',
		'pl_rade' : 'planet_radius_compared_to_earth',
		'pl_radj' : 'planet_radius_compared_to_jupiter',
		'pl_bmasse' : 'planet_mass_compared_to_earth',
		'pl_bmassj' : 'planet_mass_compared_to_jupiter',
		'pl_eqt' : 'equilibrium_temperature_K',
		'pl_eqterr1' : 'equilibrium_temperature_K_error_max',
		'pl_eqterr2' : 'equilibrium_temperature_K_error_min',
		'st_teff' : 'stellar_effective_temperature_black_body_radiation',
		'st_tefferr1' : 'stellar_effective_temperature_black_body_radiation_error_max',
		'st_tefferr2' : 'stellar_effective_temperature_black_body_radiation_error_min',
		'st_rad' : 'stellar_radius',
		'st_raderr1' : 'stellar_radius_error_max',
		'st_raderr2' : 'stellar_radius_error_min',
		'st_mass' : 'mass_of_star_compared_to_sol',
		'st_masserr1' : 'mass_of_star_compared_to_sol_error_max',
		'st_masserr2' : 'mass_of_star_compared_to_sol_error_min',
		'sy_dist' : 'distance_to_system_in_light_years',
		'sy_disterr1' : 'distance_to_system_in_light_years_error_max',
		'sy_disterr2' : 'distance_to_system_in_light_years_error_min'
		}

	exoplanets.rename(columns=rename_cols, inplace = True)

	# Create a count of null values to help below with choosing the best case duplicate (i.e. the one with the most data)
	null_list = exoplanets.isnull().sum(axis=1).tolist()

	# Check the null list is the length of the actual list otherwise there will be an issue..
	if len(null_list) != len_of_list:
		sys.exit("Error - Error matching NaN / null list.. exiting.")

	# create empty col's as required
	exoplanets['planet_mass_in_kg'] = np.nan
	exoplanets['planet_actual_radius'] = np.nan

	# Convert parsecs to light years
	# Convert planet_mass_compared_to_earth to actual mass (kg)
	# Also insert the null count and add that to the row

	parsec_to_ly = 3.261563776976 # 1 parsec to 13.s.f.

	for index, row in exoplanets.iterrows():

		# parsec to ly conversion to 13.s.f. Can quote to 3 s.f. in any display data.
		exoplanets.loc[index,'distance_to_system_in_light_years'] = row['distance_to_system_in_light_years'] * parsec_to_ly
		exoplanets.loc[index,'distance_to_system_in_light_years_error_max'] = row['distance_to_system_in_light_years_error_max'] * parsec_to_ly
		exoplanets.loc[index,'distance_to_system_in_light_years_error_min'] = row['distance_to_system_in_light_years_error_min'] * parsec_to_ly

		# calculate planet mass
		# earth is 5.972e24 kg so we need to multiply the planet_mass_compared_to_earth vs earths mass.
		exoplanets.loc[index,'planet_mass_in_kg'] = row['planet_mass_compared_to_earth'] * 5.972e24
		
		# Add a col to count nuls
		exoplanets.loc[index,'null_counter'] = null_list[index]

		# Calculate actual radius of star
		stars_rad = compute_radius_of_star(row['stellar_radius'])
		exoplanets.loc[index,'stellar_radius'] = stars_rad # TODO put this in the function 

		# compute and write the habitability zones
		compute_habitability_zone_and_luminosity(exoplanets, index, exoplanets.loc[index, 'stellar_radius'], 
			exoplanets.loc[index, 'stellar_effective_temperature_black_body_radiation'])

		# flag for habitability 
		does_planet_live_within_its_habitability_zone(exoplanets, index, exoplanets.loc[index, 'habitability_zone_inner'], 
			exoplanets.loc[index, 'habitability_zone_outer'], exoplanets.loc[index, 'orbital_period_widest_radius_in_AU'])

		# calculate the accelaration due to gravity on the planet:
		calculate_gravity_and_planet_radius(exoplanets, index, exoplanets.loc[index, 'planet_mass_in_kg'], row['planet_radius_compared_to_earth'])


	# Sort exoplanets by distance from our solar system AND sort by the least NaNs
	exoplanets.sort_values(['distance_to_system_in_light_years', 'null_counter'], ascending=[True, True], inplace = True)

	# now we can safely and locically drop duplicates, keeping the first, which will be the one with the most amount or data, or the least 
	# missing data, whichever way you wish to view it
	exoplanets.drop_duplicates('name_of_planet', keep='first', inplace = True)

	# Drop the null counter, as it's no longer needed.
	exoplanets.drop('null_counter', 1, inplace = True)

	return exoplanets


def remove_nans_from_df(df):
	'''
	Remove any df rows with no nans, note this wont affect the master dataframe as it is only passed byval. This will therefore remove any
	nans when we are looking to graph / use data where all cols are required in each row.
	'''

	return df.dropna(inplace = True)

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


def compute_radius_of_star(data_radius):
	'''
	Mean radius of the sun: https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html

	There is a -very- small margin of error in this calculation, which is due to the error margins of the input data from the 
	dataset. Although the input data can have an error of only 0.01, this alone equates to a ~ 7000 km (1.s.f) difference 
	in the radius.
	
	'''

	radius_of_sun = 695700 # mean radius of the sun to 4.s.f.

	# The stellar_radius from the dataset is measured in units of radius of the sun, so do a simple conversion:
	actual_radius = radius_of_sun * data_radius
	return actual_radius


def calc_habitable_AU_values(radius, temp_of_star):
	sb_const = 5.67e-8 # Stefan-Boltzmann constant

	area_of_star = (4 * np.pi * (radius**2)) * 1e6 #4(pi)(R^2), multipled by 1e6 to unit convert from km^2 to m^2 to get into S.I. units

	# Calculate the lumin output of the star
	lumin = sb_const * area_of_star * (temp_of_star**4) # watts

	# calculate solar luminosity based off of sol's luminosity 
	one_sol = 3.850753858550298e26

	# convert absolute luminosity of the star against the absolute luminosity of our sun
	lumin = lumin / one_sol

	'''
		
		Manually checking math - note that there is a small difference between the results computed by this script, and my 
		math by hand. This is because again, the input values are different than the values on wikipedia etc. For instance, 
		Proxima Centauri, by my hand (and using data from Wikipedia & NASA) the result of the relative luminosity is
		0.0018 L(*) (5.s.f), whereas Wikipedia shows 0.0017 L(*). The result from the script is 0.0015 L(*) (5.s.f.) which is 
		correct based on the input values the script uses in the dataset it has to work with. 

		Below is manual verification of the math, and proof of rationale for the accuracy being close enough for the purposes
		of this excersise. 

		Test: https://en.wikipedia.org/wiki/Proxima_Centauri
		Radius = 0.1542 suns
		Temp = 3042 K
		
		~ Actual radius = 0.1542 suns x (695700 km x 1000 m) = 107276940 m (using mean values from NASA to approiximate)
		area = (4 x pi x rad^2)) = 1.44618e17 m^2
		lumin = 7.02170e23
		relative (star L/sun L) = 0.001823 L(*). (Wikipedia shows 0.0017)

		Discrepancy of 0.0001 - this is likely based on the input figures as opposed to the logic. To check - I'll test another star.

		###

		I'll use the next closest star with an exoplanet just for convenience:

		Star: Epsilon Eridani (https://en.wikipedia.org/wiki/Epsilon_Eridani)
		Radius: 0.735 suns
		Temp: 5084 K

		Radius = 0.735 suns x (695700 km x 1000 m) = 511339500 m
		Area = 3.235704851e18 m^2
		lumin = 1.244611402e26 watts
		rel = 0.3232 L(*).
		
		Wikipedia shows a luminosity of 0.34 L(*), my answer is 0.32 L(*) 2.s.f, so there is a discrepancy of 0.02 L(*). Again, this is likely to be
		explained by using values from different sources to make measurements.

		I'll try one more, a larger and hotter/colder star to see how close that is, these two stars have both been around the same temperature as 
		the sun and smaller than the sun. This last attempt will give me confidence that it is not a logical / math error, and is an error based on 
		input values & slight variations from sources (as no 1 source seems to have all the information I need).

		###

		NY Virginis - https://en.wikipedia.org/wiki/NY_Virginis
		Radius: 0.151 suns
		Temp: 32740 K (+- 400 K)

		Radius = 0.151 suns x (695700 km x 1000 m) = 105050700 m
		Area = 1.38678e17 m^2
		lumin = 9.034529e27 watts
		rel = 23.46171561

		From the wiki, the star has a luminosity of 23.3 +- 1.5 L(*). My results are 23.4 3.s.f L(*). This is a discrepancy of 0.1 L(*) however, 
		the error is +- 1.5 L(*).

		Therefore, my assessment is the math is correct, however any answers will have a small margin of error. 
		For the purposes of this, I assess that the accuracy is close enough.

	'''

	inner_hab_zone = np.sqrt(lumin/1.1) # hab zone is now in AU
	outer_hab_zone = np.sqrt(lumin/0.53) # hab zone is now in AU

	return inner_hab_zone, outer_hab_zone, lumin


def compute_habitability_zone_and_luminosity(df, index, radius, temp):
	'''
	Compute the habitability zone of a star using the Stefan-Boltzmann law to determine the luminosity of the star,
	then calculate the habitability zone (i.e. capable of producing liquid water under atmospheric condictions). The relationship
	is tied to the energy output of the star.

	I call the above method: calc_habitable_AU_values to do the math. Manually tested to verify calculations provided, and they are correct within reasonable accuracy.

	Refactored to improve efficiency in code execution.

	'''
	
	# create an empty column for hab zone - check if one of these does not exist, otherwise skip
	if not 'habitability_zone_inner' in df.columns:
		df['habitability_zone_inner'] = np.nan
		df['habitability_zone_outer'] = np.nan
		df['stars_luminosity_relative_to_sun'] = np.nan

	# Calculate luminosity of the star
	inner_hab_zone, outer_hab_zone, lumin = calc_habitable_AU_values(radius, temp)

	#breakpoint()

	# add the values based on the row and index passed into the func
	df.loc[index,'habitability_zone_inner'] = inner_hab_zone # add the value
	df.loc[index,'habitability_zone_outer'] = outer_hab_zone # add the value
	df.loc[index,'stars_luminosity_relative_to_sun'] = lumin # add the value


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


def does_planet_live_within_its_habitability_zone(df, index, hab_inner, hab_outer, widest_orbit_radius):
	'''
	A function to calculate whether a planet lies within the habitability zone, simply by comparing its widest radius to the hab zone margins
	'''	
	# create an empty column - check if one of these does not exist, otherwise skip
	if not 'is_planet_habitable' in df.columns:
		df['is_planet_habitable'] = 0 # 1 = true, 0 = false,  //  2 = no data

	if hab_inner <= widest_orbit_radius <= hab_outer:
		# add the values based on the row and index passed into the func
		df.loc[index,'is_planet_habitable'] = 1 # add the value


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


def calculate_gravity_and_planet_radius(df, index, planet_mass, planet_radius):

	'''
	A function to calculate acceleration due to gravity using the well formula: g = G x M / (R^2)

	Test values for Earth to check math is correct, doing it by hand first in the comments, then I will test
	with a script (which will be removed to save making this too long)
	
	Earth's mass: 5.9722 x 10^24 kg
	Earth's mean volumetric radius: 6371.000 km 

	Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

	g = G x M / (R^2)

	g = ( 6.67 x 10^-11 N kg^-2 m^2 x 5.9722 x 10^24 kg ) / ( 6371.000 km )^2

	g = 9.81 m s^-2 (3.s.f.)

	Hand calculations are correct. Script calculations (deleted) correct.
	'''

	# create an empty column - check if one of these does not exist, otherwise skip
	if not 'accelaration_to_gravity' in df.columns:
		df['accelaration_to_gravity'] = np.nan
		df['gravity_compared_to_earth'] = np.nan

	if not 'planet_actual_radius' in df.columns:
		df['planet_actual_radius'] = np.nan

	# source of earth radius https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
	radius = planet_radius * 6371


	GRAVITY_CONSTANT = 6.67e-11 # no conversion needed as base units m^3 kg^-1 s^-2
	planet_radius = radius * 1000 # unit conversion from km to m, no conversion needed for mass as kg cancels out in the equation

	force = (GRAVITY_CONSTANT * planet_mass) / (planet_radius**2) # calculate the equation

	gravity_compared_to_earth = force / 9.807 # divide g by earth g.

	df.loc[index,'accelaration_to_gravity'] = force # dip sample of results have been manually verified
	df.loc[index,'gravity_compared_to_earth'] = gravity_compared_to_earth # dip sample of results have been manually verified
	df.loc[index,'planet_actual_radius'] = radius # dip sample: HD 219134 b -> google shows radius 10206 km, my results are 10206.342 km


def habitability_data_manipulation(df):
	'''
	
	A method to manipulate data relating to habitability zones

	TODO (Idea - Graph the data, mean, median, mode etc.)
	
	Calculate the mean value of the luminosities of stars - how close is it to the luminosity of the sun, is there a trend that for exoplanets to 
	exist / be detected, the star has to be a certain luminosity?

	Caluclate the variences of orbit if possible (scrape data?) to see how much of the orbit is in the hab zone, how much out, if this could mean 
	liquid would freeze / melt / sublime / deposition etc. Not sure if this can be calculated based on the data available. Would likely need 
	measurements from the planets at all phases of it's orbit.

	'''

	pass


def solar_data_manipulation(df):
	'''
	
	A method to manipulate data relating to solar readings

	TODO

	'''

	pass



if __name__ == '__main__':
	main()