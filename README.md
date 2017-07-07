# Log Analysis Report

## Problem 1:
What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

* Data is cleansed by removing entries with paths such as ```/```, ```/+++ATH0```, ```/spam-spam-spam-humbug``` and also
  by removing entries whose state is ```404 NOT FOUND```. Store these values in table `clean_log`
* Replace the path values of each entry in clean_log with its corresponding slug values using `regexp_repalce`
* Join tables `articles` and `clean_log` on `slug value`
* Group the above table by `title`
    
## Problem 2:
2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

* Use the table/view from step 3 of problem1 and join with `authors` and `group by author name`
     
## Problem 3:
On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer back to this lesson if you want to review the idea of HTTP status codes.)

* Create a table/view to find total num of requests per day
* Create a table/view to find number of error requests per day
* Join the above two tables/views on date and calculate percentage of errors for each day. Select the days with more than 1% error

## Tables and views created:
**Note**: The tables and views have to be created in the same order as below
     
###      Tables:
* **clean_log**: This table holds the values after removing the entries with error status and paths not pointing to articles. And after creating the table, the path entries are updated with slug values
*Creating table*:
`create table clean_log  as select  * from  log where status!='404 NOT FOUND' and path like ('/article/%');
`
*Updating table*:
`update clean_log set path = regexp_replace(path, '/article/(.*)', '\1', 'g');`

###     Views:
* **article_log_join**: This view is a join on `articles` and `clean_log` tables.
*Creating view*:
`create view article_log_join as select articles.title, articles.author from articles join clean_log on articles.slug=clean_log.path;`
    
* **date_status**: This view is created by grouping `status` and aggregating them for each day
*Creating view*:
`create view date_status as select date(time),count(*) from log group by date(time);`

* **date_error**: This view is created by grouping `status` with `404 NOT FOUND` entries and aggregating for each day
*Creating view*:
`create view date_error as select date(time),count(*) from log group by date(time),status having status like'40%';`

## Running the code
    
###     Assumptions:
* The database and data tables are preloaded into the database and tables and views mentioned above are created.
* Python pacakages used `psycopg2`
    
###     Usage:
Pass the name of the database with author, articles and log table as an argument. 
For a database named "news", run the code as below
    `./newsdatadb.py news`.
    
