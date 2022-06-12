import numpy as np
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

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

	gravity_compared_to_earth = force / 9.807 # divide G by earth G.

	df.loc[index,'accelaration_to_gravity'] = force # dip sample of results have been manually verified
	df.loc[index,'gravity_compared_to_earth'] = gravity_compared_to_earth # dip sample of results have been manually verified
	df.loc[index,'planet_actual_radius'] = radius # dip sample: HD 219134 b -> google shows radius 10206 km, my results are 10206.342 km


#def compute_planet_state_from_temperature(df, index, planet_mass, planet_radius, planet_temp):
def compute_planet_state_from_temperature(df):

	'''
	Pseudo code:

	1) method to convert K to *c (for general consumption graph)
	2) scrape data from wikipedia on freezing, melting, boiling points of each element
		* https://en.wikipedia.org/wiki/Melting_points_of_the_elements_(data_page)
		* https://en.wikipedia.org/wiki/Boiling_points_of_the_elements_(data_page)#WebEl
		* freezing -> just use anything under the melting point.
	3) Convert these into a dictionary 
	4) Obtain data about the most abundant, or the heaviest element, of a star of a particular system so I can
	   work out the relevent temp of state changes for that system (no data for the planet itself as no spectra).
	5) If 4 isnt possible, then calculate on the abundance of elements in our solar system, or do we go from iron based on the 
	   nuclear fusion process?

		https://academic.oup.com/mnras/article/450/3/2279/1056352
		It might be worth reading this article to see what data I can extract from some of the emission tables provided by NASA
		for the exoplanets. 

		https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=emissionspec shows the emission 
		spectrum from exoplanets, and WASP-80 b has an emission spectrum (central wavelength) of 3.6 um. How does this tell us
		the planet is a gas giant? That I do not know.. This wavelength is longer than visible light, and above the emission
		spectrums from atoms. So I'm not sure yet what this wavelength data relates to.


	6) Choose the most relevent elements, or those in highest abundance (or those that are heaviest?) and then 
	   calculate whether the planet will be an icy planet, rocky planet, gas planet, or a magma planet.
	7) Graph the above, including bubbles indicate the relevent 'zones' for each state
	8) Look at some stats.
	
	The hardest part is likely to be step 4, and finding this data...

	'''

	# Scrape data from wikipedia for state changes of each element in the periodic table
	df_element_change_of_state = scrape_wikipedia_data_regarding_state_change()


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