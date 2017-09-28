Work in Progress
----------------

-   This will serve as our landing page for the Text Analytics for Team Summerhill

``` r
library(feather)
library(tidyverse)
data <- read_feather("results_analytics_Toronto+ON.feather")
head(data,1)
```

    ## # A tibble: 1 × 3
    ##                                                                          text
    ##                                                                         <chr>
    ## 1 Analyst  Customer Analytics job   SIRIUS XM CANADA INC.   Toronto  ON   Ind
    ## # ... with 2 more variables: titles <chr>, urls <chr>

``` r
library(jsonlite)
data2 <- fromJSON("indeed_search_analytics_Toronto+ON.json")
```
