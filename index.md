-   This document was rendered last on 2017-10-17

*THIS PROJECT IS STILL UNDER CONSTRUCTION*
------------------------------------------

The intention will be to mask the code as the project approaches completion.

Authors
-------

-   To shower praise for ingenuity on the project, contact [Melody Liu](https://www.linkedin.com/in/meifei-melody-liu/)
-   For criticism of avenues we couldn't investigate in 4 weeks contact [Gage Sonntag](https://www.linkedin.com/in/gage-sonntag/)

Executive Summary
-----------------

-   This project was produced for the Text Analytics Workshop for the Winter 2018 Masters of Management Analytics Cohort at Queen's University
-   The goal from the outset was to use text analytics techniques developed in class to examine jobs companies have posted on Indeed in Toronto and employ techniques discussed in class including document clustering, topic modelling, and visualization.

Project Rationale
-----------------

-   A open sourced project working with real world data was desired
-   Other projects can be found scraping DS/Analytics jobs from Indeed. Typically word frequencies for keywords like Python or Hadoop are calculated
-   Moving beyond that, we were interested in topic modelling and how the choice of words signals relationships between roles
-   Job postings fit the 'bag of words' or ngram approach taught in class. Not many employers say **"We don't want someone who knows Python"**

Gathering Data
--------------

-   Beautiful Soup & Selenium were used in Python to access [Indeed](https://www.indeed.ca/jobs?q=analytics&l=Toronto&start=10 "Indeed:Analytics Jobs in Toronto") and scrape unsponsored job titles, companies, and postings
-   1800 jobs were scraped from 9 search terms we believed captured the jobs most MMA students are pursuing.
-   Jobs were passed from Python to R using [Feather](https://blog.rstudio.com/2016/03/29/feather/ "Feather: A Fast On-Disk Format for Data Frames for R and Python, powered by Apache Arrow")

-   Our data returned 636 unique jobs within our search.
-   It's clear a considerable amount of cleaning is in order

<img src="Figs/Jobs Found-1.png" style="display: block; margin: auto;" />

-   We expect 200 jobs for each result, and removing the duplicate jobs in the order they were searched.
-   Interestingly, searching 200 jobs in analytics returns only 113 unique jobs, some redundancy exists.
-   As we search overlapping terms, data sciencist, data insights, fewer and fewer unique jobs are returned
-   Interestingly, each additional search term returns a surprising amount of new jobs. 75 jobs are shown for machine learning that were not found for data scientist, a fairly similar field.
-   Business Intelligence seems to be fairly lateral to other search terms, returning many unique jobs

<img src="Figs/Job title frequency-1.png" style="display: block; margin: auto;" />

-   The job search is currently dominated by data scientists, which have become a catch all word. But it's encouraging to see data engineering & machine learning engineering to begin to take hold.
-   Analytics is surprisingly absent, but is likely wrapped into titles like "Manager, Analytics" which is more heterogeneous. Let's take a closer look at where our Analytics jobs are.

<img src="Figs/titles for analytics only-1.png" style="display: block; margin: auto;" />

-   Here we can see much more heterogeneity in the job titles used by Analytics Practioners vs Data Scientists.

<img src="Figs/frequent companies-1.png" style="display: block; margin: auto;" />

-   This seems to resonate with what the Toronto Job environment is as a whole: Telecom, Banking and consultancies.

A Word Frequency Approach
=========================

-   The boiler plate at the end of each job posting, encouraging people to apply, discussing company acolades and culture distort our analysis. Let's spend some time cleaning up *job specific words* and *html related language*

<img src="Figs/Process unigrams Data-1.png" style="display: block; margin: auto;" />

-   We are starting to look better. Let's take a look at our bigrams. <img src="Figs/Process bigrams-1.png" style="display: block; margin: auto;" />
-   This is less fruitful. Likely some bi-grams have value that are less frequent. Words like **machine learning** or **project managment**. They are likely mentioned once in a few job postings, but have a low count.
-   We could cluster on tf-idf, but instead, let's first look at how often phrases are mentioned distinctly in jobs. This weights phrases mentioned in lots of jobs, not phrases mentioned many times.

<img src="Figs/Process distinct bigrams-1.png" style="display: block; margin: auto;" /> - This begins to get a bit more accurate of a assessment of what employers mention. Some of these are representative of the core requirements in analytics & DS: the fine line between communication and computer science, decision making & project management.

-   Typically when you see projects like this done, people look for some analytics or Data Science skills, and count the occurences. We want to go beyond that, but lets examine the landscape for analytical skills in Toronto.

A Skills Based Approach
=======================

<img src="Figs/skills mentioned-1.png" style="display: block; margin: auto;" /> - This seems to suggest excel, R and SQL are in high demand. Let's examine how inter related these concepts are. - Are the same jobs looking for R excel and SQL? - How many of these skills are required for different jobs?

<img src="Figs/frequency of skills-1.png" style="display: block; margin: auto;" /> - For the skills we have selected, analytics and data scientists have long tails. These are likely associated with the similarity between the big data tools we selected: hive, scala, spark etc. - Let's see how theses jobs get mentioned together.

A Network Diagram of Skills
===========================

<img src="Figs/pairwise correlation-1.png" style="display: block; margin: auto;" /> - The network analysis shown shows a few unique clusters. Excel and powerpoint don't seem correlated with the rest of our tech stack, despite the frequent mentions of excel (which presumably are the noun and not the verb) - 3 clusters seem present: - Traditional Analytics - R, SAS, and a smal relationship to - Big Data - Python leveraging Hadoop, AWS, Scala and spark - BI/Data Viz - Tableau, SQL and qlik - Our Trifecta of R, SQL, and excel don't seem as complimentary skills anymore

-   Let's look at clustering our data set, to see if these groups are also represented

Clustering
==========

-   An initial pass using hierarchical clustering revealed a number of outlier jobs, which were removed from the data set. The work will not be shown here, for brevity's sake. After removing these, let's look at how K-means clustering performs.

<img src="Figs/unnamed-chunk-1-1.png" style="display: block; margin: auto;" /> - Plotting the within cluster sum of squares vs number of clusters produces a scree plot. Here, good clustering could be judged by the slope of the line decreasing rapidly after the ideal clustering was run. here this is not the case, with a shallow change in slope. - Evaluating instead by Dunn's Metric, which judgues clusters by the means of clusters, the distance between clusters and the within cluster variance. Here, we find the ideal cluster size to be 7. Let's dive a litle further into our clustering results.

<img src="Figs/7 cluster performance-1.png" style="display: block; margin: auto;" />

-   While it seemed at first glance there is some structure measured from the clustering, cluster 2 may represent some of the less technical roles in data analysis and BI, and cluster 1 has a notable amount of DS & ML jobs, the bulk of the data is sucked up in Cluster 5, and the rest are selected as outliers.

-   In reality, these 7 clusters are really just 3.

-   K-means is sensitive to multi-dimensional outliers, which are hard to identify. With more work identifiying them and filtering them out, we could achieve more resolution between our clusters.
