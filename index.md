-   This document was rendered last on 2017-10-03

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

files <- paste(searches,".feather",sep="")

#read and collapse to data frame
datalist <- lapply(as.list(files),function(x){read_feather(x)})
data <- bind_rows(datalist,.id="search")

#fix quotations in column names
names(data) <- c("search","company","text","titles","urls")

#check if we have redundant jobs
sum(duplicated(data[,2:4]))
```

    ## [1] 21

``` r
#reduce to distinct jobs and clean up search column
data <- data[!duplicated(data[,2:4]),]
data$search <- plyr::mapvalues(data$search,
                               from=unique(data$search),
                               to=searches)

head(data)
```

    ## # A tibble: 6 × 5
    ##      search                       company
    ##       <chr>                         <chr>
    ## 1 analytics \n\nToronto Wildlife Centre\n
    ## 2 analytics    \n\nPurdue Pharma Canada\n
    ## 3 analytics                \n\n\nLoblaw\n
    ## 4 analytics            \n\n\nScotiabank\n
    ## 5 analytics  \n\n\nGovernment of Canada\n
    ## 6 analytics                   \n\n\nRBC\n
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
    ## 1             analytics         20
    ## 2   analytics reporting         14
    ## 3    analytics strategy         18
    ## 4 business intelligence         19
    ## 5          data analyst         20
    ## 6         data insights         17
    ## 7        data scientist         20
    ## 8      machine learning         14
    ## 9   marketing analytics         17

``` r
#what words to avoid
stops <- stopwords("en")

data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     group_by(tokens) %>%
     filter(!tokens %in% stops) %>%
     summarize(count=n()) %>%
     arrange(desc(count))
```

    ## # A tibble: 9,385 × 2
    ##        tokens count
    ##         <chr> <int>
    ## 1        data  1447
    ## 2         job   773
    ## 3    business   752
    ## 4  experience   624
    ## 5       apply   513
    ## 6        will   510
    ## 7           s   475
    ## 8   analytics   460
    ## 9         new   438
    ## 10          3   401
    ## # ... with 9,375 more rows

``` r
#look a bi-grams
data %>%
     unnest_tokens(token="ngrams",n=2,output="tokens",input=text) %>%
     separate(col=tokens,into=c("word1","word2"),sep=" ") %>%
     filter(!word1 %in% stops, !word2 %in% stops) %>%
     unite(tokens,word1,word2,sep=" ") %>%
     count(tokens,sort=TRUE)
```

    ## # A tibble: 29,715 × 2
    ##                   tokens     n
    ##                    <chr> <int>
    ## 1              apply now   160
    ## 2               days ago   146
    ## 3         data scientist   136
    ## 4       machine learning   128
    ## 5                    3 3   106
    ## 6        job description   103
    ## 7             ago easily    97
    ## 8  business intelligence    97
    ## 9           data analyst    97
    ## 10          easily apply    97
    ## # ... with 29,705 more rows

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
data_tdm <- TermDocumentMatrix(data_corpus)
```

``` r
#convert TDM into matrix
data_m <- as.matrix(data_tdm)

#count term frequencies and sort in descending order
term_frequency <- sort(rowSums(data_m),decreasing = TRUE)
term_frequency[1:15]
```

    ##        and        the       data       with        for        you 
    ##       5341       2648       1416       1266       1152        946 
    ##        job   business        our experience       your        are 
    ##        758        735        677        598        595        552 
    ##       will      apply  analytics 
    ##        509        502        444

``` r
#create data frame of different word frequencies
words <- data.frame(term = names(term_frequency),num=term_frequency)

#create word cloud
wordcloud(words$term,words$num,max.words = 75, colors = "blue")
```

![](Figs/Word%20Cloud-1.png)
