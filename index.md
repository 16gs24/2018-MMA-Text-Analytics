-   This document was rendered last on 2017-10-20

Authors
-------

-   To shower praise for ingenuity on the project, contact [Melody Liu](https://www.linkedin.com/in/meifei-melody-liu/)
-   For criticism of avenues we couldn't investigate in 4 weeks contact [Gage Sonntag](https://www.linkedin.com/in/gage-sonntag/)

Executive Summary
-----------------

-   This project was produced for the Text Analytics Workshop for the Winter 2018 Masters of Management Analytics Cohort at Queen's University
-   The goal from the outset was to use text analytics techniques developed in class to examine jobs companies have posted on Indeed in Toronto and employ techniques discussed in class including some of tokenization, data cleaning, document clustering, topic modelling, and visualization.

Project Rationale
-----------------

-   A open sourced project working with real world data was desired
-   Other projects can be found scraping DS/Analytics jobs from Indeed. Typically word frequencies for keywords like Python or Hadoop are calculated
-   Moving beyond that, we were interested in clustering and how the choice of words signals relationships between roles, as well as how skills relate, not just their frequency
-   Job postings fit the 'bag of words' or ngram approach taught in class. Not many employers say *"We don't want someone who knows Python"*

Gathering Data
--------------

-   Beautiful Soup & Selenium were used in Python to access [Indeed](https://www.indeed.ca/jobs?q=analytics&l=Toronto&start=10 "Indeed:Analytics Jobs in Toronto") and scrape unsponsored job titles, companies, and postings
-   1800 jobs were scraped from 9 search terms we believed captured the jobs most MMA students are pursuing.
-   Jobs were passed from Python to R using [Feather](https://blog.rstudio.com/2016/03/29/feather/ "Feather: A Fast On-Disk Format for Data Frames for R and Python, powered by Apache Arrow")

-   Our data returned 636 unique jobs within our search.
-   Considerable data cleaning is required to get to something easy to analyze. This includes stripping remaining HTML from our text, removing custom low value words, and words too common in job postings.

Exploratory Data Analysis
-------------------------

<img src="Figs/unique postings by search-1.png" style="display: block; margin: auto;" />

-   We expect 200 jobs for each result, and removing the duplicate jobs in the order they were searched.
-   Interestingly, searching 200 jobs in analytics returns only about half unique jobs, so by the time you reach page 10, you are seeing very little new things.
-   As we search overlapping terms, data sciencist, data insights, fewer and fewer unique jobs are returned
-   Interestingly, each additional search term returns a surprising amount of new jobs. A reasonable amount are shown for machine learning that were not found for data scientist or analytics, an overlapping field.
-   Business Intelligence and marketing analytics seems to be orthogonal to other search terms, returning relatively more unique jobs

<img src="Figs/most frequent titles-1.png" style="display: block; margin: auto;" /> - The job search is currently dominated by data scientists, which have become a catch all word. But it's encouraging to see machine learning engineers and developer roles begin to be fleshed out. - Analytics is surprisingly absent, but is likely wrapped into titles like "Manager, Analytics" which is more inconsistently titled. Let's take a closer look at where our Analytics jobs are.

<img src="Figs/most frequent analytics titles-1.png" style="display: block; margin: auto;" />

-   These searches appear less consistent than job titles like Data Scientist.

<img src="Figs/most frequent companies-1.png" style="display: block; margin: auto;" />

-   This seems to resonate with what the Toronto Job environment is as a whole: Consulting, Banking, Telecom and a splattering of retail.

A Word Frequency Approach
-------------------------

-   The boiler plate at the end of each job posting, encouraging people to apply, discussing company acolades and culture distort our analysis. Let's spend some time cleaning up *job specific words* and *html related language*

<img src="Figs/unigrams count-1.png" style="display: block; margin: auto;" /> - We've removed most of the job specific language, apply, description and words that don't signal much about what the job is. We see from a frequency approach, there isn't alot to be gleaned. - Some words are mentioned in every posting. Analytics as a search term appeared to have proportionally more management oriented positions. - Let's see if our bi-grams have more signal. <img src="Figs/bigrams count-1.png" style="display: block; margin: auto;" /> - This is more encouraging than our Unigrams. We have some domain specific phrases, like mental health and real estate. But also *communication skills* and *problem solving* which straddle the hard and soft skills often critical to success in analytics and data science. - Some of these phrases may be loaded in a small number of job postings. For example, *digital marketing* being mentioned many times in 1 posting referring to the job title, department, and responsibilities. Let's remove phrases mentioned more than once and see more of the breadth of mentions.

<img src="Figs/distinct bigrams count-1.png" style="display: block; margin: auto;" /> - This begins to get a bit more accurate of a assessment of what employers mention. Some of these highlight more useful skills that were drowned out by more freqent mentions. These are things like *project management* or *software engineering*, useful skills for data scientists and analysts.

A Skills Based Approach
=======================

-   Typically when you see projects like this done, people look for some Analytics or Data Science skills, and count the occurences. We want to go beyond that, but lets examine the landscape for analytical skills in Toronto. <img src="Figs/skills mentioned-1.png" style="display: block; margin: auto;" />
-   Our list is a few dozen unigram skills that we believe capture the technologies worked in across analytics and data science. Broadly they'll get classified as Big Data, Data Analysis and Visualization to capture the analysis and communication of results, as well as the unique tools for cloud & distributed computing.
-   This seems to suggest excel, R and SQL are in high demand. Let's examine how inter related these concepts are.
-   Are the same jobs looking for R excel and SQL?
-   How many of these skills are required for different jobs?

<img src="Figs/histogram of skills-1.png" style="display: block; margin: auto;" /> - For the skills we have selected, analytics and data scientists have long tails. These are likely associated with the similarity between the big data tools we selected: hive, scala, spark etc, but also suggest companies are casting a wide net in terms of people's experience. - For the words we selected, many jobs in marketing analysis and business intelligence don't seem to leverage them as much as other positions. - Let's see how theses skills get mentioned together.

A Network Diagram of Skills
===========================

<img src="Figs/pairwise correlation-1.png" style="display: block; margin: auto;" /> - The network analysis shown shows a few interesting groupings with darker lines representing more frequently correlated words. A line between two words representing a likelihood to be mentioned together in the same job. - Excel and powerpoint don't seem correlated with the rest of our tech stack, despite the frequent mentions of excel (which presumably are the noun and not the verb) - Traditional Analytics - R, SAS, and SPSS seem inter-related. - Big Data - Python leveraging Hadoop, AWS, Scala and spark. Interestingly R is not the language of big data despite some support from spark. - BI/Data Viz - Tableau, microstrategy and qlik supported by SQL. - The most freqent words, R, SQL, and excel no longer seem as inter-related. - Let's look at clustering our data set, to see if these groups are also represented when we cluster on all the words in the posting.

Clustering
==========

-   An initial pass using hierarchical clustering revealed a half dozen outlier jobs, which were removed, the dendrogram will be omitted due to it's size and for the sake of brevity.
-   Let's instead see how K-means clustering performs, this being a semi-supervised problem. We would expect some of the search terms to load together in the same cluster if they are similar jobs. Perhaps Data Scientist and Machine learning in 1 cluster, with marketing analytics in another.

<img src="Figs/30 clusters-1.png" style="display: block; margin: auto;" /> - Plotting the within cluster sum of squares vs number of clusters produces a scree plot. Here, good clustering would be judged by a sharp "elbow" in the data. We don't see that here. - Evaluating instead by Dunn's Metric, which judgues clusters by the means of clusters, the distance between clusters and the within cluster variance. Here, we find the ideal cluster size to be 7. Let's dive a litle further into our clustering results.

<img src="Figs/7 cluster performance-1.png" style="display: block; margin: auto;" /> - Words were stemmed and unigrams and bigrams that occur in between 10% and 80% of postings were used. - In reality, these 7 clusters are really just 3. Most of our jobs are loading in clusters 4,5 and 6. - Even these clusters don't seem to represent sensible structure, cluster 4 has jobs in data science, data analyst and marketing analytics highly loaded, which don't seem interrelated at first glance. - Clusters 1,2,3 and 7 are just outliers, and don't seem to measure anything. - K-means is sensitive to multi-dimensional outliers, which are hard to identify. With more work identifiying them and filtering them out, we could achieve more resolution between our clusters. But wasn't achievable in 4 weeks.

Conclusion
----------

-   While employers demand a variety of technical skills, it's measurable that softer skills are also important. Not only to generate insight but also to communicate it.
-   R, SQL and excel are demanded tools in Toronto, but not in the same roles.
-   Distinct groupings could be seen for technical skillsets in conventional analytics, data visualization, and the big data tech stack.
-   Sizing of the clusters was attempted with K-means clustering but the dataset had too many outliers remaining.
