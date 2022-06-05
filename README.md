# HOME - Habitable or Mapped Exoplanets

A project to map and conduct data mining / analysis on exoplanets and their host systems. What information can I obtain from astronomical data in the search for habitable, unique, or interesting exoplanets / systems / stars.
 
 Data cleansing takes place in execution, as well as analysis of data. It is my intention to update this to conduct various different sorts of analysis to this project, and also potentially mapping all exoplanets and their systems. 
 
'explore.py' is the entry to the program. Required modules (available via pip): numpy, pandas, matplotlib.

To run, clone the project and run in your console / terminal: 'python3 explore.py'.

## Blog!

The below is a blog written by me, documenting my progress and a way for me to express what I am doing as I do it. It is intended to show my workflow periodically. I will provide a more well rounded writeup of my results when the project is complete. For now, please enjoy the blog where I may talk about bugs or challenges I have had to overcome, data which I find interesting, and anything unique to this project I would like to communicate! I may also refine or add to the data used in this investigation, so the below data in the blog may not be the final data I end up using in my analysis.

### Update 1 - currently will show you the scatter graph of the mass of exoplanets plotted against the temperature of their host star as below:

<img width="626" alt="image" src="https://user-images.githubusercontent.com/49762827/172062620-8a625d88-6952-4e3d-a7d7-565a883c5b1e.png">

Most planets discovered are relativley low mass (to be expected), orbiting low temperature stars. There are a few exceptions to this, and it will be interesting to explore data in relation to them. My hypothesis would be that these larger planets would be gas giants, however I will examine the data to see whether this is correct.

This was particually interesting to write, as I have had to use multiple conversions and equations to calcualte the luminosity of the star, and then convert it to a relative luminosity, as well as working with AU as a measurement of distance. I plan on building a module which will look at the orbit of the exoplanet, and see whether it fits into the habitable zone of the star it orbits. I have also manually reviewed data and calculations to ensure the math is correct.

### Update 2 - Calculate luminosity of the star & calculate habitability zones of the star

Calculates the luminosity of the host star, and adds data relating to the habitabilty zones of the star. Future versions will analyse this vs data of the exoplanets to see whether liquid water could exist on them. I would like to add some data from EM specrtums observed from the planets / stars to test for the presence of certain elements which may increase the chance of life forming.

### Update 3 - Now produces a histogram of number of exoplanets around a star!

<img width="683" alt="image" src="https://user-images.githubusercontent.com/49762827/172060748-e5589720-6476-42f3-a6a5-481b71346b35.png">

The histogram shows some interesting results, the vast majority of discoveries are that 1 exoplanet orbits a star, with the maximum being 8 exoplanets. At the moment I havent examined the data any further with python, so it will be interesting to see how many of these are in a habitable region.

I expected this portion of coding to take no more than 15 minuets, however I was working on these small changes for about 2 frustrating hours! I had used a pivot table to count the exoplanets around a host star, and then put this into a histogram - however, this produced unexpected results. I spent a lot time manually verifying data (which was all correct), so the problem didn't arise from there. After going backwards and forwards with the dataset and debugging, I eventually re-wrote the method to use the groupby function to count the exoplanets. Sticking that into the histogram worked as intended. I am not exactly sure why using a pivot table produced this behaviour. However, on reflection the top value of the column with the counts was named by the pivot table 0 (zero as an integer). I wonder whether the histogram function interpereted this as a value instead of a column header.

### Update 4 - comparing basic graphs between the mass data, and those exoplanets in the habitable zone

More graphs will follow. However you can now see some interesting comparisons:

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172066182-931c1bcd-0ae4-477e-ac41-b032d15f523d.png">

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172066251-612c363c-9814-4be1-b5f1-533de0fa7b4e.png">
