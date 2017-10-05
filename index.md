-   This document was rendered last on 2017-10-05

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
test <- datalist[[1]]
data <- bind_rows(datalist,.id="search")
rm(datalist)

#fix quotations in column names
names(data) <- c("search","company","text","titles","urls")

#check if we have redundant jobs
sum(duplicated(data[,2:4]))
```

    ## [1] 966

``` r
#examine the uniqueness of our data
#lapply(data,function(x){length(unique(x))})
NumJobs <- length(unique(data$urls))

#reduce to distinct jobs and clean up search column
data <- data[!duplicated(data$urls),]
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
RemovePattern <- function(vector,pattern){gsub(pattern=pattern,replacement="",vector)}
#data <- map(data,RemovePattern,"\n")
```

``` r
#investigate redundant jobs. Should return 200/each if they are all unique.

rollup <- data %>%
     group_by(search) %>%
     summarize(NumberUniquePostings=n()) 

#sort by search order
left_join(data.frame(search=searches),rollup,by="search")
```

    ##                  search NumberUniquePostings
    ## 1             analytics                  100
    ## 2          data analyst                   82
    ## 3        data scientist                   90
    ## 4    analytics strategy                   65
    ## 5         data insights                   50
    ## 6   marketing analytics                   71
    ## 7   analytics reporting                   47
    ## 8      machine learning                   57
    ## 9 business intelligence                   74

-   We expect 200 jobs for each result, and removing the duplicate jobs in the order they were searched.
-   Interestingly, searching 200 jobs in analytics returns only 113 unique jobs, some redundancy exists.
-   As we search overlapping terms, data sciencist, data insights, fewer and fewer unique jobs are returned
-   Interestingly, each additional search term returns a surprising amount of new jobs. 75 jobs are shown for machine learning that were not found for data scientist, a fairly similar field.
-   Business Intelligence seems to be fairly lateral to other search terms, returning many unique jobs

``` r
#what words to avoid
stops <- stopwords("en")

#process n-grams
unigrams <- data %>%
     unnest_tokens(token="words",output="unigrams",input=text) %>%
     group_by(unigrams) %>%
     filter(!unigrams %in% stops) %>%
     count(unigrams,sort=TRUE)

#visualize
wordcloud(unigrams$unigrams,unigrams$n,max.words=100)
```

![](Figs/Process%20unigrams%20Data-1.png)

-   Looking at a simple word frequency, we see out of the box our data is very messy
-   The boiler plate at the end of each job posting, encouraging people to apply, discussing company acolades and culture distort our analysis. Let's spend some time cleaning up 0-value words.

``` r
#look a bi-grams
bigrams_totals <- data %>%
     unnest_tokens(token="ngrams",n=2,output="tokens",input=text) %>%
     separate(col=tokens,into=c("word1","word2"),sep=" ") %>%
     filter(!word1 %in% stops, !word2 %in% stops) %>%
     unite(tokens,word1,word2,sep=" ") %>%
     count(tokens,sort=TRUE)

head(bigrams_totals,20)
```

    ## # A tibble: 20 × 2
    ##                   tokens     n
    ##                    <chr> <int>
    ## 1              apply now   699
    ## 2               days ago   559
    ## 3  business intelligence   442
    ## 4       machine learning   435
    ## 5        job description   414
    ## 6             ago easily   409
    ## 7           easily apply   409
    ## 8     style display:none   382
    ## 9           social media   334
    ## 10        data scientist   330
    ## 11               1 style   329
    ## 12      talent community   313
    ## 13          new password   300
    ## 14             full time   270
    ## 15             now start   270
    ## 16          data analyst   261
    ## 17        required field   253
    ## 18       password forgot   251
    ## 19       forgot password   250
    ## 20            contact us   233

``` r
wordcloud(bigrams_totals$tokens,bigrams_totals$n,max.words=20)
```

![](Figs/Process%20bigrams-1.png)

``` r
#determine how frequent each word occurs across job postings. Don't skip stop words yet.
unigrams_freq <- data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     select(urls,tokens) %>%
     distinct() %>%
     group_by(tokens) %>%
     count(tokens,sort=TRUE) %>%
     ungroup() %>%
     mutate(frequency=n/NumJobs)

tail(unigrams_freq,20)
```

    ## # A tibble: 20 × 3
    ##                                                       tokens     n
    ##                                                        <chr> <int>
    ## 1                                                youtubefind     1
    ## 2                                                    youwill     1
    ## 3                                                     youyou     1
    ## 4                                                         yp     1
    ## 5                                                        yui     1
    ## 6                                                      yukon     1
    ## 7                                                     yummly     1
    ## 8                                                       yuzu     1
    ## 9                                                     z299.3     1
    ## 10                                                      z795     1
    ## 11                                  zdbrtvigjurnvorcmgdwo4ld     1
    ## 12                                    zdirectoriesmapssearch     1
    ## 13 zealandpakistanpanamaperuphilippinespolandportugalrussian     1
    ## 14                                                  zerobug2     1
    ## 15                                       ziffdavis.icims.com     1
    ## 16                                                     zones     1
    ## 17                                       zonesqualifications     1
    ## 18                                                   zooming     1
    ## 19                                                    zoomoo     1
    ## 20                    zwehzuaeckqfwhfbvl5ljgjisgxycvxlu0paha     1
    ## # ... with 1 more variables: frequency <dbl>

``` r
#determine how frequent each bigram is across job postings. Don't skip stop words yet.
bigrams_freq <- data %>%
     unnest_tokens(token="ngrams",n=2,output="tokens",input=text) %>%
     select(urls,tokens) %>%
     distinct() %>%
     group_by(tokens) %>%
     count(tokens,sort=TRUE) %>%
     ungroup() %>%
     mutate(frequency=n/NumJobs)

head(bigrams_freq,20)
```

    ## # A tibble: 20 × 3
    ##             tokens     n frequency
    ##              <chr> <int>     <dbl>
    ## 1           of the   442 0.6949686
    ## 2             in a   377 0.5927673
    ## 3           in the   367 0.5770440
    ## 4           to the   362 0.5691824
    ## 5          will be   351 0.5518868
    ## 6       ability to   332 0.5220126
    ## 7    experience in   308 0.4842767
    ## 8         with the   307 0.4827044
    ## 9  job description   276 0.4339623
    ## 10         to work   275 0.4323899
    ## 11          we are   267 0.4198113
    ## 12        for this   264 0.4150943
    ## 13       apply now   263 0.4135220
    ## 14         for the   257 0.4040881
    ## 15    knowledge of   253 0.3977987
    ## 16          with a   250 0.3930818
    ## 17            is a   248 0.3899371
    ## 18         and the   245 0.3852201
    ## 19         you are   242 0.3805031
    ## 20         sign in   239 0.3757862

``` r
skills <- c("sas","python","excel","powerpoint","sql",
                          "r","hadoop","spark","java","scala","aws",
                          "tableau","microstrategy","spss","c++")

data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     filter(tokens %in% skills) %>%
     pairwise_count(tokens,urls,sort=TRUE)
```

    ## # A tibble: 182 × 3
    ##         item1      item2     n
    ##         <chr>      <chr> <dbl>
    ## 1      python          r    85
    ## 2           r     python    85
    ## 3      python        sql    76
    ## 4         sql     python    76
    ## 5       excel powerpoint    68
    ## 6  powerpoint      excel    68
    ## 7           r        sql    66
    ## 8         sql          r    66
    ## 9       excel        sql    63
    ## 10        sql      excel    63
    ## # ... with 172 more rows

``` r
#pairwise correlation
data %>%
     unnest_tokens(token="words",output="tokens",input=text) %>%
     filter(tokens %in% skills) %>%
     pairwise_cor(tokens,urls,sort=TRUE) %>%
     filter(correlation > .1) %>%
     graph_from_data_frame() %>%
     ggraph(layout = "fr") +
     geom_edge_link(aes(edge_alpha = correlation), show.legend = FALSE) +
     geom_node_point(color = "lightblue", size = 5) +
     geom_node_text(aes(label = name), repel = TRUE) +
     theme_void()
```

![](Figs/pairwise%20correlation-1.png)
