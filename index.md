Examining the Analytics Job Market in Toronto
---------------------------------------------

Executive Summary
=================

-   This project was produced for the Text Analytics Workshop for the Winter 2018 Masters of Management Analytics Cohort at Queen's University
-   The goal from the outset was to use text analytics techniques developed in class to examine jobs companies have posted on Indeed in Toronto and employ techniques covered in class including document clustering, topic modelling/LDA,
-   This document was rendered last on 2017-09-28

Gathering Data
==============

-   Beautiful Soup & Selenium were used in Python to access [Indeed](https://www.indeed.ca/jobs?q=analytics&l=Toronto&start=10) and scrape unsponsored jobs
-   ### unique jobs were scraped from the search terms: `analytics`,`etc`....

-   Jobs were passed from Python to R using [Feather](https://blog.rstudio.com/2016/03/29/feather/) to analyze

``` r
data <- read_feather("results_analytics_Toronto+ON.feather")
head(data,1)
```

    ## # A tibble: 1 × 3
    ##                                                                          text
    ##                                                                         <chr>
    ## 1 Analyst  Customer Analytics job   SIRIUS XM CANADA INC.   Toronto  ON   Ind
    ## # ... with 2 more variables: titles <chr>, urls <chr>

    ## [1] "Hello World"
