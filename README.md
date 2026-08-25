Project Summary

This project analyzes healthcare accessibility across the Greater Accra Region of Ghana by estimating the population that can reach a healthcare facility within an 8-minute travel time using road network analysis.

Using 274 healthcare facilities, OpenStreetMap road data, and WorldPop (2020) population data, the study found that:

82.38% (4,405,459 people) can access a healthcare facility within 8 minutes.
17.62% (942,344 people) live beyond the 8-minute travel threshold.
Methodology

The workflow involved:

Retrieving healthcare facilities and road network data using OSMnx.
Cleaning and reprojecting spatial datasets (EPSG:32630).
Calculating road travel speeds and travel times.
Generating 8-minute isochrones around healthcare facilities.
Clipping WorldPop (2020) population data to the Greater Accra Region.
Estimating the population within and outside the accessibility zones.
Key Findings
Out of a total population of 5,347,803, approximately 4.4 million residents have access to a healthcare facility within 8 minutes.
Nearly 942,000 residents remain outside the 8-minute accessibility threshold.
Healthcare accessibility is highest in the western part of Greater Accra, where both population density and healthcare facility concentration are greatest.
Recommendation

The results indicate that while healthcare coverage is relatively high, nearly one in five residents still faces limited access to healthcare within an 8-minute travel time. To improve accessibility, policymakers and healthcare planners should prioritize underserved areas by:

Establishing new healthcare facilities in locations with low accessibility.
Improving road infrastructure to reduce travel times to existing facilities.
Expanding emergency and community-based healthcare services in underserved communities.
Using geospatial accessibility analyses to guide future investments and monitor progress toward equitable healthcare access.

This project demonstrates how geospatial analysis can support evidence-based healthcare planning by identifying gaps in service accessibility and helping decision-makers allocate resources more effectively.