#!/usr/bin/env python3
"""Analyzing and report module

This module provides methods that could connect to database,
fetch required information, such as top article, top authors,
date that error appear more than 1%.

This program depends on psycopg2 and interact with existing
PostgreSQL Database.
"""


import psycopg2

DBNAME = "news"


def connect(dbname=DBNAME):
    """
    This method connect to PostgreSQL database
    returns database connection and cursor
    """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def top_n_articles(n=3):
    """
    This method returns top n popular articles of all time.
    Most viewed ariticles.
    """
    db, c = connect()
    query = """
            SELECT articles.title, count(log.id) AS views
            FROM articles, log
            WHERE log.path = ('/article/' || articles.slug)
            GROUP BY articles.title
            ORDER BY views DESC
            LIMIT (%s);
            """
    c.execute(query, [n, ])
    results = c.fetchall()
    db.close()
    return results


def top_viewed_authors():
    """
    This method returns top authors and their total views in sorted list
    """
    db, c = connect()
    query = """
            SELECT authors.name, COUNT(log.id) AS views
            FROM authors, articles, log
            WHERE articles.author = authors.id 
            AND log.path = ('/article/' || articles.slug)
            GROUP BY authors.id
            ORDER BY views DESC;
            """
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def alert_days():
    """
    Date more than 1% of requests lead to errors
    """
    db, c = connect()
    query = """
            SELECT day, (error*100.0/total*1.0) AS percent FROM
            (
                SELECT date(time) AS day,
                COUNT(status) AS total,
                SUM(CASE
                    WHEN (status LIKE '4%' OR status LIKE '5%')
                    THEN 1
                    ELSE 0
                    END) AS error
                FROM log GROUP BY day
            ) AS result
            WHERE (error*100.0/total) > 1.0
            ORDER BY percent DESC;
            """
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


if __name__ == '__main__':
    print("Top Articles:")
    top_articles = top_n_articles(3)
    for i, (title, views) in enumerate(top_articles, 1):
        print('{}. {} -- {} views'.format(i, title, views))

    print("")
    print("Top Authors:")
    top_authors = top_viewed_authors()
    for i, (name, views) in enumerate(top_authors, 1):
        print('{}. {} -- {} views'.format(i, name, views))

    print("")
    print("Days error more than 1%:")
    error_dates = alert_days()
    for date, rate in error_dates:
        print('{} -- {}% errors.'.format(str(date), str(round(rate, 2))))
