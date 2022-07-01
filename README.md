# HOME - Habitable or Mapped Exoplanets

A project to map and conduct data mining / analysis on exoplanets and their host systems. What information can I obtain from astronomical data in the search for habitable, unique, or interesting exoplanets / systems / stars.
 
 Data cleansing takes place in execution, as well as analysis of data. It is my intention to update this to conduct various different sorts of analysis to this project, and also potentially mapping all exoplanets and their systems. 
 
'explore.py' is the entry to the program. Required modules (available via pip): numpy, pandas, matplotlib.

To run, clone the project and run in your console / terminal: 'python3 explore.py'.

As the project has grown far bigger than expected at this stage, I have split it into numerous modules which can be found within the deps/ subdirectory to handle physics & math, plotting and data cleansing.

# Result!

The following is the output result of my program, which is a result of the input data! There is still a few tweaks I would like to make, however the first lot of results can be found as follows! This is very exciting, and it's amazing to think that results such as this could be the focus of major scientific discovery!

    Potentially habitable planet found! Planet name: K2-18 b, it has an orbital period of:
			33 days (2.s.f) (meaning it takes 33 (2.s.f) many days to orbit its star), 
			it has a possible temperature of: 10.9 degrees celsius (3.s.f), 
			the temperature of its star is 3457.0 Kelvin, 
			the radius of the star is: 285237.0 km, 
			the distance to the planet is 124.0261811215556 light years, 
			the radius of the planet is 15099.27 km,
			the planet lives in the habitable zone of the star and is not a gas planet or an iron planet. Gravity has an acceleration of 
			 15.6 meters per second per second (3.s.f), which is 1.59 (3.s.f) times that of Earth.
    
    Potentially habitable planet found! Planet name: TRAPPIST-1 e, it has an orbital period of:
			6.1 days (2.s.f) (meaning it takes 6.1 (2.s.f) many days to orbit its star), 
			it has a possible temperature of: -22.1 degrees celsius (3.s.f), 
			the temperature of its star is 2559.0 Kelvin, 
			the radius of the star is: 83484.0 km, 
			the distance to the planet is 39.0 light years, 
			the radius of the planet is 5848.578 km,
			the planet lives in the habitable zone of the star and is not a gas planet or an iron planet. Gravity has an acceleration of 
			 7.22 meters per second per second (3.s.f), which is 0.736 (3.s.f) times that of Earth.


## Blog!

The below is a blog written by me, documenting my progress and a way for me to express what I am doing as I do it. It is intended to show my workflow periodically. I will provide a more well rounded writeup of my results when the project is complete. For now, please enjoy the blog where I may talk about bugs or challenges I have had to overcome, data which I find interesting, and anything unique to this project I would like to communicate! I may also refine or add to the data used in this investigation, so the below data in the blog may not be the final data I end up using in my analysis.

Any major changes I'll probably do as a branch and pr, so don't forget to check live branches!

### Update July 2022:

In the latest update, I have refactored my code to condense the duplicate rows in a much better style. Previously the way I removed duplicates was to drop duplicate rows and only keep the first - the problem this created however was that if row 1 was missing data duplicate rows 2, 3 and 4 contained, the final dataframe would be missing data which could potentially mean habitable exoplanets were not being found by my program!

To combat this, I first create a temp dataframe and iterate through the input data identifying where the gaps are per set of duplicates. If any of the subsequent duplicate rows contain data that are missing in the first row, then it adds these values into the temp dataframe which only has one planet per row. I'm quite proud of my code and the results.

From analysing the results from this refactored code, more exoplanets can be manipulated! So it has been worthwhile! For example, here is the difference on a histogram (left is the old version, right is the new version) because the program is able to manipulate more data!

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176934028-e7e05855-4aec-4368-a585-a2c766850a46.png">

You can quite clearly see there was a fair amount of data missing because of the old way I was removing duplicate values!

The differences between old graphs (left) and new graphs (right) are presented below in no particular order - this is the most up to date data that the program now uses! And on the first image, you can see what a huge difference it has made as one planet has a huge density of approximately 7.5 x 10^6 kg m^3 (2.s.f), but in the old data the largest value for density was approximately 4.1 x 10^6 kg m^3 (2.s.f)! That is (nearly) double!! And what is more impressive, is the planet has a low mass for its density! This is a good example of how using python in science or in data analysis can easily help triage specific things or anomalies to research!

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176934422-87461b59-b976-4b74-8916-e55dadb62f02.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176934940-e746c767-49d5-4a58-aec8-cb98fa9ad3ab.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176934964-f3a143bd-8dc9-41c4-a9ee-dadfd2376945.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935041-e0d9b43b-3182-4438-866e-4ec426919c69.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935063-fe7169ca-c959-40c6-999f-558edb3690b3.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935102-e27bcd16-e5d9-4dce-8fb9-8a297e134b2d.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935130-c791203f-ec46-4b8a-bb09-b758c28c7d1e.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935183-499014b8-f94e-4d56-8206-e2eb46117d36.png">

<img width="947" alt="image" src="https://user-images.githubusercontent.com/49762827/176935237-d80c4440-5d9d-4580-a7f7-2e3115abe251.png">


## Old blog updates running oldest to newest:

### Scatter graph of the mass of exoplanets plotted against the temperature of their host star:

<img width="626" alt="image" src="https://user-images.githubusercontent.com/49762827/172062620-8a625d88-6952-4e3d-a7d7-565a883c5b1e.png">

Most planets discovered are relatively low mass (to be expected), orbiting low temperature stars. There are a few exceptions to this, and it will be interesting to explore data in relation to them. My hypothesis would be that these larger planets would be gas giants, however I will examine the data to see whether this is correct.

This was particularly interesting to write, as I have had to use multiple conversions and equations to calculate the luminosity of the star, and then convert it to a relative luminosity, as well as working with AU as a measurement of distance. I plan on building a module which will look at the orbit of the exoplanet, and see whether it fits into the habitable zone of the star it orbits. I have also manually reviewed data and calculations to ensure the math is correct.

### Significant progress - Calculate luminosity of the star & calculate habitability zones of the star:

Calculates the luminosity of the host star, and adds data relating to the habitability zones of the star. Future versions will analyse this vs data of the exoplanets to see whether liquid water could exist on them. I would like to add some data from EM spectrums observed from the planets / stars to test for the presence of certain elements which may increase the chance of life forming.

### Histogram of number of exoplanets around a star:

<img width="683" alt="image" src="https://user-images.githubusercontent.com/49762827/172060748-e5589720-6476-42f3-a6a5-481b71346b35.png">

The histogram shows some interesting results, the vast majority of discoveries are that 1 exoplanet orbits a star, with the maximum being 8 exoplanets. At the moment I haven’t examined the data any further with python, so it will be interesting to see how many of these are in a habitable region.

I expected this portion of coding to take no more than 15 minuets, however I was working on these small changes for about 2 frustrating hours! I had used a pivot table to count the exoplanets around a host star, and then put this into a histogram - however, this produced unexpected results. I spent a lot time manually verifying data (which was all correct), so the problem didn't arise from there. After going backwards and forwards with the dataset and debugging, I eventually re-wrote the method to use the groupby function to count the exoplanets. Sticking that into the histogram worked as intended. I am not exactly sure why using a pivot table produced this behaviour. However, on reflection the top value of the column with the counts was named by the pivot table 0 (zero as an integer). I wonder whether the histogram function interpreted this as a value instead of a column header.

### Comparing basic graphs between the mass data, and those exoplanets in the habitable zone:

More graphs will follow. However you can now see some interesting comparisons:

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172066182-931c1bcd-0ae4-477e-ac41-b032d15f523d.png">

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172066251-612c363c-9814-4be1-b5f1-533de0fa7b4e.png">

### A graph to show the G-Force acting on various planets, with a comparison of habitable and non-habitable planets:

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172438033-df992f4d-9b1f-468d-9926-c544cef445ae.png">

Interestingly, I expected the plot to be roughly a straight line graph as I was expecting there to be a correlation between the radius of a planet and its mass - the data is surprising! Looking at the data alone, seeing planets with a low mass but high g-force may indicate the planets have heavier elements present. I have then plotted the G-Force against radius, to see what that trend looks like, and that data reinforces this hypothesis. It would be interesting to obtain a spectroscopy sample from the exoplanet to see what wavelengths of light are emitted from the planet which may help determine what elements are present.

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/172435556-eb02c8a0-d606-488e-b1da-5f76bed376a0.png">

Personally, I am very excited to see what results the James Webb Space Telescope has to offer in terms of spectroscopy of exoplanets, and I will look to clean and add that data to this set! I would also like to see whether I could mathematically model what elements are likely to be present on a certain planet given the force of gravity vs its radius. Could any of these predicted elements be complex enough that they would only occur as a result of biological life?

It is also worth noting at this point that just because the line of 4 G's would be too much for humans to withstand, there is nothing to say that life could not emerge as an extremophile on other planets, capable of withstanding high amounts of gravity.

I have then produced a pie chart showing the split between planets over, and under, 4 G's.

<img width="480" alt="image" src="https://user-images.githubusercontent.com/49762827/172440464-13aedf23-e625-479f-be5e-ec82835d22e4.png">

### Determine whether a planet is gas, rocky, or iron based.

I have now implemented a fairly simple feature to calculate and plot the state of a planet. I approached this wrong at first, where I have scraped and processed (BeautifulSoup & Pandas) two tables from wikipedia relating to the melting and boiling points of all of the different elements. I was going to calculate the temperature of the planet against these temperatures, however, that itself does not determine whether a planet is a gas giant (or dwarf) or not. I have left that code in, as I am quite proud of the scraping & data cleansing required for that.

Data plotted as a scatter graph:

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/173242900-4bc58381-33f3-47f7-ade2-8988019e761d.png">

Data plotted as a histogram:

<img width="1233" alt="image" src="https://user-images.githubusercontent.com/49762827/173242981-17048343-57c4-4abe-b480-a7f50bb45e54.png">

What is really interesting about this data is that just because a planet is in the habitable zone, it is not always habitable. For instance, the research conducted so far shows that a planet must:

* Be in the habitable zone,
* Have a gravity consistent with life (as we know it), and
* Not be a gaseous planet
