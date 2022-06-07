import numpy as np
import pandas as pd
from pathlib import Path

from . import phys_and_math as pam


# A list of methods to clean up the data. I did consider doing this with classes and OOP, but it isnt neccessary.

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
		stars_rad = pam.compute_radius_of_star(row['stellar_radius'])
		exoplanets.loc[index,'stellar_radius'] = stars_rad # TODO put this in the function 

		# compute and write the habitability zones
		pam.compute_habitability_zone_and_luminosity(exoplanets, index, exoplanets.loc[index, 'stellar_radius'], 
			exoplanets.loc[index, 'stellar_effective_temperature_black_body_radiation'])

		# flag for habitability 
		does_planet_live_within_its_habitability_zone(exoplanets, index, exoplanets.loc[index, 'habitability_zone_inner'], 
			exoplanets.loc[index, 'habitability_zone_outer'], exoplanets.loc[index, 'orbital_period_widest_radius_in_AU'])

		# calculate the accelaration due to gravity on the planet:
		pam.calculate_gravity_and_planet_radius(exoplanets, index, exoplanets.loc[index, 'planet_mass_in_kg'], row['planet_radius_compared_to_earth'])


	# Sort exoplanets by distance from our solar system AND sort by the least NaNs
	exoplanets.sort_values(['distance_to_system_in_light_years', 'null_counter'], ascending=[True, True], inplace = True)

	# now we can safely and locically drop duplicates, keeping the first, which will be the one with the most amount or data, or the least 
	# missing data, whichever way you wish to view it
	exoplanets.drop_duplicates('name_of_planet', keep='first', inplace = True)

	# Drop the null counter, as it's no longer needed.
	exoplanets.drop('null_counter', 1, inplace = True)

	return exoplanets


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




def remove_nans_from_df(df):
	'''
	Remove any df rows with no nans, note this wont affect the master dataframe as it is only passed byval. This will therefore remove any
	nans when we are looking to graph / use data where all cols are required in each row.
	'''

	return df.dropna(inplace = True)
