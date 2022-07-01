import numpy as np
import pandas as pd
from pathlib import Path
import requests
import re
from bs4 import BeautifulSoup
import sys

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


def scrape_wikipedia_data_regarding_state_change():
	'''

	A method to scrape data from wikipedia regarding the melting and boiling point of the elements

	Returns a dataframe with the data. There are a few NaN values, but for the purposes of this excersise, this 
	shouldn't impact the overall accuracy.

	'''

	# create an empty dataframe which will hold the state change values of each element
	df_element_change_of_state = pd.DataFrame(columns=['element', 'melting_point', 'boiling_point'])

	# Get the url's and turn into soup
	url_melting = "https://en.wikipedia.org/wiki/Melting_points_of_the_elements_(data_page)"
	url_boiling = "https://en.wikipedia.org/wiki/Boiling_points_of_the_elements_(data_page)"

	### get data related to the melting points ###
	webpage = requests.get(url_melting)
	soup = BeautifulSoup(webpage.content, "html.parser")

	# Scrape the table and convert to a df
	melting_point_table_scrape = soup.find(id='Melting_point').findNext('table')

	# convert into dataframe 
	melting_data_frame = pd.read_html(str(melting_point_table_scrape))[0] # read html into table
	df_element_change_of_state = parse_scraped_data_from_wikipedia_regarding_state_change(df_element_change_of_state, melting_data_frame)


	### get data relating to the boiling points ###
	webpage = requests.get(url_boiling)
	soup = BeautifulSoup(webpage.content, "html.parser")

	# Scrape the table and convert to a df
	melting_point_table_scrape = soup.find(id='Boiling_point').findNext('table')
	boiling_point_data_frame = pd.read_html(str(melting_point_table_scrape))[0]

	# rename the cols so that I can reference them properly in the method called next
	boiling_point_data_frame.columns = ['Reference', 'Kelvin', 'degrees_c', 'farh']

	# scrape the data for boiling point, and set flag to 1 to indicate this in below function
	df_element_change_of_state = parse_scraped_data_from_wikipedia_regarding_state_change(df_element_change_of_state, boiling_point_data_frame, 1)

	return df_element_change_of_state


def parse_scraped_data_from_wikipedia_regarding_state_change(df_element_change_of_state, input_data_frame, is_melting=0):

	'''
	A method to handle the parsing and sanitising of data scraped from wikipedia.

	Takes in: the overall dataframe relating to the final result, input data from the table, and a flag whether this is melting or freezing.

	Returns: dataframe
	'''

	# manually add hydrogen to the dataframe, as the scrape includes it as a column heading, as opposed to data
	if is_melting == 0:
		input_data_frame.loc[-1] = ['1 H hydrogen', np.nan, np.nan, np.nan, np.nan]
	else:
		input_data_frame.loc[-1] = ['1 H hydrogen', np.nan, np.nan, np.nan]

	# resort index
	input_data_frame.index = input_data_frame.index + 1
	input_data_frame.sort_index(inplace=True)

	# iterate through the reference column, every time it starts with a number, this is the atomic number of the element
	# what I then want to do is find the 'use' kelvin value of the element. I'll use the fact the atomic number is first in
	# the reference column as a hook to know which element the data relates to
	for index, row in input_data_frame.iterrows():

		# get the data in the reference column at the specific index we are iterating over
		if is_melting == 0:
			frame_reference = input_data_frame['Reference'].iloc[index].to_string(index=False)
		else:
			frame_reference = input_data_frame['Reference'].iloc[index]

		# if the row starts with a number (it is the atomic number) so lets get the kelvin data
		# use regex to only keep numeric values and decimal place within the data
		if frame_reference[0].isdigit():
			if is_melting == 0:
				kelvin = input_data_frame['Kelvin'].iloc[index+1].to_string(index=False) # moved inside if to prevent out of bounds
				kelvin = re.sub("[^0-9.]", "", kelvin)
			else:
				kelvin = input_data_frame['Kelvin'].iloc[index+1] # moved inside if to prevent out of bounds
				kelvin = re.sub("[^0-9.]", "", str(kelvin))

			# where kelvin is blank set to nan, 3 occurrences of this
			if kelvin == '':
				kelvin = np.nan # setting to 0 would mess with averages, so set to nan instead


			# add values into the dataframe
			if is_melting == 0:
				df_element_change_of_state.loc[len(df_element_change_of_state)]=[frame_reference, float(kelvin), np.nan] 

			else:
				row_of_ele = df_element_change_of_state[df_element_change_of_state['element'] == frame_reference].index # get the row with the same element
				df_element_change_of_state.loc[row_of_ele,'boiling_point'] = float(kelvin) # correct math now with row insertion

	return df_element_change_of_state


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
	exoplanets['planet_density'] = np.nan
	exoplanets['is_planet_gas_giant'] = np.nan

	merge_data_rows(exoplanets)


	for index, row in exoplanets.iterrows():
		compute_data_each_row_of_exoplanet_df(index, row, exoplanets, null_list)


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



def compute_data_each_row_of_exoplanet_df(index, row, exoplanets, null_list):
	parsec_to_ly = 3.261563776976 # 1 parsec to 13.s.f.

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

	# calculate density in kg m^-3
	density = pam.compute_density_of_planet(exoplanets.loc[index, 'planet_mass_in_kg'], exoplanets.loc[index, 'planet_radius_compared_to_earth'])
	exoplanets.loc[index,'planet_density'] = density

	# calc chances of planet being a gas giant based off of this source:
	# source: https://www.open.edu/openlearn/mod/oucontent/view.php?id=66947&extra=thumbnailfigure_idm491
	if density < 3000:
		exoplanets.loc[index,'is_planet_gas_giant'] = 1 # if above 3000 kg m^-3, it is likely gas
	if density > 3000:
		exoplanets.loc[index,'is_planet_gas_giant'] = 0 # if above 3000 kg m^-3, it is likely rocky
	if density > 7900:
		exoplanets.loc[index,'is_planet_gas_giant'] = 2 # if above 3000 kg m^-3, it is likely iron


def merge_data_rows(exoplanets):
	'''
	A method to merge data rows as there is a problem at the moment where some data nmay be missed because of empty rows
	The idea of this method is to consolidate missing values where data exists over multiple rows into one single row as a new
	dataframe.

	Takes in the exoplanet dataframe
	Returns another dataframe which sould be more complete than the first.

	By sorting the data alphabetically via planet name, it creates a faster search method for finding if that planet name exists elsewhere
	in the data.

	'''

	print('Removing duplicates and condensing any missing data from duplicate rows into one single row...')

	# sort the dataframe alphabetically by planet name.
	exoplanets.sort_values('name_of_planet')

	# properties for the new dataframe
	len_of_df = len(exoplanets.index)

	index_of_t_df = -1 # start counter from -1 so we dont need a flag system - the actual used value will never be -1 as its incremented

	t_df = pd.DataFrame(columns = exoplanets.columns)

	exoplanets.to_excel("beforeOps.xlsx")

	# create a list of planet names to establish if we are on a new planet, or the same on
	list_of_planets_processed = []

	# variable to store the name of the planet being iterated over where it is a duplicate
	name_of_planet_iterating = ""

	# start the iteration
	for index, row in exoplanets.iterrows():

		name_of_current_planet = exoplanets.loc[index,'name_of_planet']

		# ensure we don't go out of bounds
		if index < len_of_df - 1:
			# Check if the next planet in the nexr row is a match of the current planet being iterated over
			if name_of_current_planet == exoplanets.loc[index + 1,'name_of_planet']:

				# set the name of planet being iterated over which is duplicated in the raw data
				name_of_planet_iterating = name_of_current_planet

				# check if planet name is in list, if not it is a fresh insert,
				# if it is in the list then we need to check what rows we need to fill!
				if name_of_current_planet not in list_of_planets_processed:

					#print(f"Name of current planet: {name_of_current_planet}, list: {list_of_planets_processed}")

					index_of_t_df += 1 # do this first, as it starts from -1

					list_of_planets_processed.append(name_of_current_planet) # add to the list
					t_df.loc[index_of_t_df] = exoplanets.loc[index] # add the row to the temp database

					# create a list for the missing values that we want to search for in the subsequent rows in the below else
					missing_data_dict = create_dict_of_missing_values_from_row(exoplanets, index)

				else:
					# Search through the row for any missing values and insert into the row at t_df
					list_of_missing_values = list(missing_data_dict.keys())


			# if name of current planet isnt something being iterated over, then it is not a duplicate and needs inserting
			if name_of_current_planet != name_of_planet_iterating:
				# this will include the rows where there is only 1 row of data for an exoplanet
				index_of_t_df += 1 # do this first, as it starts from -1
				t_df.loc[index_of_t_df] = exoplanets.loc[index]


	t_df.to_excel("tdf.xlsx")

	sys.exit("Stop")

	return t_df


def create_dict_of_missing_values_from_row(exoplanets, index):
	''' 
	Create a dictionary of missing / nan values from the row that we need to search for in any duplicate data sets

	Returns a list
	'''
	missing_data_list = exoplanets.iloc[index].isnull().tolist() # iterate through row and ret true or false for if nan
	missing_data_dict = dict(zip(exoplanets.columns, missing_data_list)) # convert the list of bools to a dict
	missing_data_dict = {k: v for k, v in missing_data_dict.items() if v == True} # filter only by true - i.e. the missing ones
	return list(missing_data_dict.keys) # return list of keys (i.e. column names)


def remove_nans_from_df(df):
	'''
	Remove any df rows with no nans, note this wont affect the master dataframe as it is only passed byval. This will therefore remove any
	nans when we are looking to graph / use data where all cols are required in each row.
	'''

	return df.dropna(inplace = True)
