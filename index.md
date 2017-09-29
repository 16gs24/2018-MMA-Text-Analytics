-   This document was rendered last on 2017-09-29

*THIS PROJECT IS STILL UNDER CONSTRUCTION*
------------------------------------------

The intention will be to mask the code as the project approaches completion.

Executive Summary
-----------------

-   This project was produced for the Text Analytics Workshop for the Winter 2018 Masters of Management Analytics Cohort at Queen's University
-   The goal from the outset was to use text analytics techniques developed in class to examine jobs companies have posted on Indeed in Toronto and employ techniques discussed in class including document clustering, topic modelling, and visualization.

``` r
library(feather)
library(tidyverse)
library(tidytext)
library(tm)
```

``` r
clean_corpus <- function(corpus,dropwords){
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, content_transformer(replace_abbreviation))
  corpus <- tm_map(corpus, stripWhitespace)
  corpus <- tm_map(corpus, removeNumbers)
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removeWords, 
                   c(stopwords("en"), dropwords))
  return(corpus)
}

#cleaner but needs testing
clean_corpus <- function(Corpus,DropWordVector){
     Corpus <- Corpus %>%
          tm_map(removePunctuation) %>%
          tm_map(content_transformer(replace_abbreviation)) %>%
          tm_map(stripWhitespace) %>%
          tm_map(removeNumbers) %>%
          tm_map(content_transformer(tolower)) %>%
          tm_map(removeWords,c(stopwords("english"),DropWordVector))
     return(Corpus)
}
```

Gathering Data
--------------

-   Beautiful Soup & Selenium were used in Python to access [Indeed](https://www.indeed.ca/jobs?q=analytics&l=Toronto&start=10 "Indeed:Analytics Jobs in Toronto") and scrape unsponsored job titles, companies, and postings
-   `later number` unique jobs were scraped from the search terms: `analytics`,`etc`....
-   Jobs were passed from Python to R using [Feather](https://blog.rstudio.com/2016/03/29/feather/ "Feather: A Fast On-Disk Format for Data Frames for R and Python, powered by Apache Arrow")

``` r
#list our data files
searches <- c("BI","analytics")
files <- list("results_Business Intelligence_Toronto+ON.feather",
              "results_analytics_Toronto+ON.feather")

#read and collapse to data frame
datalist <- lapply(files,function(x){read_feather(x)})
data <- bind_rows(datalist,.id="search")

#fix quotations in column names
names(data)
```

    ## [1] "search" "text"   "titles" "urls"

``` r
names(data) <- c("search","text","titles","urls")

#check if we have redundant jobs
sum(duplicated(data[,2:4]))
```

    ## [1] 1

``` r
#reduce to distinct jobs and clean up search column
data <- data[!duplicated(data[,2:4]),]
data$search <- plyr::mapvalues(data$search,from=c("1","2"),to=searches)
head(data)
```

    ## # A tibble: 6 × 4
    ##   search
    ##    <chr>
    ## 1     BI
    ## 2     BI
    ## 3     BI
    ## 4     BI
    ## 5     BI
    ## 6     BI
    ## # ... with 3 more variables: text <chr>, titles <chr>, urls <chr>

``` r
#word analysis
data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     group_by(tokens) %>%
     filter(!tokens %in% stopwords("en")) %>%
     summarize(count=n()) %>%
     arrange(desc(count))
```

    ## # A tibble: 4,843 × 2
    ##        tokens count
    ##         <chr> <int>
    ## 1        data   342
    ## 2         job   296
    ## 3    business   291
    ## 4     english   224
    ## 5        will   222
    ## 6  experience   211
    ## 7           s   174
    ## 8      skills   164
    ## 9    required   158
    ## 10      apply   154
    ## # ... with 4,833 more rows

``` r
data %>%
     unnest_tokens(token="ngrams",n=2,output="tokens",input=text) %>%
     group_by(tokens) %>%
     filter(!tokens %in% stopwords("en")) %>%
     summarize(count=n()) %>%
     arrange(desc(count))
```

    ## # A tibble: 20,904 × 2
    ##                   tokens count
    ##                    <chr> <int>
    ## 1                 of the   131
    ## 2                   in a    82
    ## 3             ability to    78
    ## 4                 to the    77
    ## 5                will be    75
    ## 6  business intelligence    74
    ## 7                 in the    74
    ## 8           knowledge of    69
    ## 9              apply now    60
    ## 10               sign in    51
    ## # ... with 20,894 more rows
