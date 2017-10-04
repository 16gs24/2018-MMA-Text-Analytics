-   This document was rendered last on 2017-10-04

*THIS PROJECT IS STILL UNDER CONSTRUCTION*
------------------------------------------

The intention will be to mask the code as the project approaches completion.

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

``` r
library(feather)
library(tidyverse)
library(tidytext)
library(tm)
library(wordcloud)
library(widyr)
library(ggraph)
library(igraph)
```

Gathering Data
--------------

-   Beautiful Soup & Selenium were used in Python to access [Indeed](https://www.indeed.ca/jobs?q=analytics&l=Toronto&start=10 "Indeed:Analytics Jobs in Toronto") and scrape unsponsored job titles, companies, and postings
-   `later number` unique jobs were scraped from the search terms: `analytics`,`etc`....
-   Jobs were passed from Python to R using [Feather](https://blog.rstudio.com/2016/03/29/feather/ "Feather: A Fast On-Disk Format for Data Frames for R and Python, powered by Apache Arrow")

``` r
rm(list=ls())
#list our data files
searches <- c("analytics",
                 "data analyst",
                 "data scientist",
                 "analytics strategy",
                 "data insights",
                 "marketing analytics",
                 "analytics reporting",
                 "machine learning",
                 "business intelligence")

files <- paste("data/feather/",searches,".feather",sep="")

#read and collapse to data frame
datalist <- lapply(as.list(files),function(x){read_feather(x)})
data <- bind_rows(datalist,.id="search")
rm(datalist)

#fix quotations in column names
names(data) <- c("search","company","text","titles","urls")

#check if we have redundant jobs
sum(duplicated(data[,2:4]))
```

    ## [1] 966

``` r
#reduce to distinct jobs and clean up search column
data <- data[!duplicated(data[,2:4]),]
data$search <- plyr::mapvalues(data$search,
                               from=unique(data$search),
                               to=searches)

head(data)
```

    ## # A tibble: 6 × 5
    ##      search                          company
    ##       <chr>                            <chr>
    ## 1 analytics                 \n\n\nKPMG LLP\n
    ## 2 analytics       \n\n\nThe Globe and Mail\n
    ## 3 analytics          \n\n\nYork University\n
    ## 4 analytics \n\n\nCanadian Tire: Corporate\n
    ## 5 analytics         \n\n\nAmerican Express\n
    ## 6 analytics               \n\n\nScotiabank\n
    ## # ... with 3 more variables: text <chr>, titles <chr>, urls <chr>

``` r
unique(data$search)
```

    ## [1] "analytics"             "data analyst"          "data scientist"       
    ## [4] "analytics strategy"    "data insights"         "marketing analytics"  
    ## [7] "analytics reporting"   "machine learning"      "business intelligence"

``` r
#investigate redundant jobs. Should return 20/each if they are all unique.
data %>%
     group_by(search) %>%
     summarize(found_jobs=n())
```

    ## # A tibble: 9 × 2
    ##                  search found_jobs
    ##                   <chr>      <int>
    ## 1             analytics        113
    ## 2   analytics reporting         77
    ## 3    analytics strategy         79
    ## 4 business intelligence        107
    ## 5          data analyst        104
    ## 6         data insights         82
    ## 7        data scientist        101
    ## 8      machine learning         75
    ## 9   marketing analytics         96

We expect 200 jobs for each result, and removing the duplicate jobs we can begin to see some overlap. Analytics had more jobs since it was searched first, topics discussed later like BI still has alot of jobs, which suggests it may be a more distinct field.

``` r
#what words to avoid
stops <- stopwords("en")

unigrams <- data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     group_by(tokens) %>%
     filter(!tokens %in% stops) %>%
     count(tokens,sort=TRUE)

unigrams
```

    ## # A tibble: 25,988 × 2
    ##        tokens     n
    ##         <chr> <int>
    ## 1        data  6502
    ## 2         job  4267
    ## 3    business  3773
    ## 4  experience  3492
    ## 5        will  3199
    ## 6       apply  2768
    ## 7         new  2470
    ## 8        work  2377
    ## 9        team  2341
    ## 10          1  2048
    ## # ... with 25,978 more rows

``` r
#look a bi-grams
data %>%
     unnest_tokens(token="ngrams",n=2,output="tokens",input=text) %>%
     separate(col=tokens,into=c("word1","word2"),sep=" ") %>%
     filter(!word1 %in% stops, !word2 %in% stops) %>%
     unite(tokens,word1,word2,sep=" ") %>%
     count(tokens,sort=TRUE)
```

    ## # A tibble: 109,384 × 2
    ##                   tokens     n
    ##                    <chr> <int>
    ## 1              apply now   857
    ## 2               days ago   824
    ## 3  business intelligence   643
    ## 4        job description   641
    ## 5             ago easily   595
    ## 6           easily apply   595
    ## 7       machine learning   591
    ## 8     style display:none   560
    ## 9         data scientist   530
    ## 10               1 style   483
    ## # ... with 109,374 more rows

``` r
#Converting text column into VectorSource
data_source <- VectorSource(data$text)

#Creating a corpus out of the data
data_corpus <- VCorpus(data_source)

#clean data
#data_corpus <- clean_corpus(data_corpus)
```

``` r
#Converting corpus into TDM
#data_tdm <- TermDocumentMatrix(data_corpus)
```

``` r
# #convert TDM into matrix
# data_m <- as.matrix(data_tdm)
# 
# #count term frequencies and sort in descending order
# term_frequency <- sort(rowSums(data_m),decreasing = TRUE)
# term_frequency[1:15]
# 
# #create data frame of different word frequencies
# words <- data.frame(term = names(term_frequency),num=term_frequency)
# 
# #create word cloud
# wordcloud(words$term,words$num,max.words = 75, colors = "blue")

wordcloud(unigrams$tokens,unigrams$n,max.words=100)
```

![](Figs/Word%20Cloud-1.png)

``` r
data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     filter(tokens %in% c("sas","python","excel","powerpoint","sql",
                          "r","hadoop","spark","java","scala","aws","tableau","microstrategy")) %>%
     pairwise_count(tokens,urls,sort=TRUE)
```

    ## # A tibble: 156 × 3
    ##         item1      item2     n
    ##         <chr>      <chr> <dbl>
    ## 1      python          r    85
    ## 2           r     python    85
    ## 3      python        sql    76
    ## 4         sql     python    76
    ## 5       excel powerpoint    69
    ## 6  powerpoint      excel    69
    ## 7           r        sql    66
    ## 8         sql          r    66
    ## 9       excel        sql    63
    ## 10        sql      excel    63
    ## # ... with 146 more rows

``` r
#pairwise correlation
data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     filter(tokens %in% c("sas","python","excel","powerpoint","sql",
                          "r","hadoop","spark","java","scala","aws","tableau","microstrategy")) %>%
     pairwise_cor(tokens,urls,sort=TRUE)
```

    ## # A tibble: 156 × 3
    ##         item1      item2 correlation
    ##         <chr>      <chr>       <dbl>
    ## 1       spark     hadoop   0.6305199
    ## 2      hadoop      spark   0.6305199
    ## 3       excel powerpoint   0.5031618
    ## 4  powerpoint      excel   0.5031618
    ## 5      python          r   0.4789493
    ## 6           r     python   0.4789493
    ## 7       spark     python   0.4238287
    ## 8      python      spark   0.4238287
    ## 9         sas          r   0.3647545
    ## 10          r        sas   0.3647545
    ## # ... with 146 more rows
