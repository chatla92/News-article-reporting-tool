#!/usr/bin/python2.7

import psycopg2
import sys


def print_queries(c):
    for entry in c.fetchall():
        print(str(entry[0]) + " -- " + str(entry[1]))
    print("\n")


DBNAME = sys.argv[1]
db = psycopg2.connect(database=DBNAME)
cur = db.cursor()

# problem 1
# group by article title as sum
cur.execute(
    """select title, count(*) as num
       from article_log_join group by title order by num desc limit 3;""")

print_queries(cur)
# problem 2
# Join authors article_log_join with authors on author id and group by
# author name

cur.execute(
    """select name, count(*) as num
       from article_log_join join authors
       on article_log_join.author=authors.id
       group by name order by num desc;""")

print_queries(cur)
# problem 3
# Join date_error and date_status views and calculate the error percentages

cur.execute(
    """select to_char(date_status.date,'FMMonth FMDD, YYYY'),
       round(cast(date_error.count/date_status.count::float*100 as numeric),2)
       from date_error join date_status on date_status.date=date_error.date
       where  (date_error.count/date_status.count::float)>=0.01;""")

print_queries(cur)

db.close()
