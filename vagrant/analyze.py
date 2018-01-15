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
    except:
        print("Error: Fail to connect to database.")


def top_n_articles(n=3):
    """
    This method returns top n popular articles of all time.
    Most viewed ariticles.
    """
    db, c = connect()
    query = "select articles.title, count(log.id) as views\
            from articles, log\
            where log.path = ('/article/' || articles.slug)\
            group by articles.title\
            order by views desc\
            limit {};".format(n)
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def top_viewed_authors():
    """
    This method returns top authors and their total views in sorted list
    """
    db, c = connect()
    query = "select authors.name, count(log.id) as views from authors, articles, log\
            where articles.author = authors.id and\
            log.path = ('/article/' || articles.slug)\
            group by authors.id\
            order by views desc;"
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def alert_days():
    """
    Date more than 1% of requests lead to errors
    """
    db, c = connect()
    query = "\
        select day, (error*100.0/total*1.0) as percent from\
        (\
            select date(time) as day,\
            count(status) as total,\
            sum(case\
                when (status like '4%' or status like '5%')\
                then 1 else 0 end\
                ) as error\
            from log group by day\
        ) as result\
        where (error*100.0/total) > 1.0\
        order by percent desc;"
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results

if __name__ == '__main__':
    print("Top Articles:")
    top_articles = top_n_articles(3)
    for i in range(len(top_articles)):
        line = str(i+1) + ". " + top_articles[i][0]\
            + " -- " + str(top_articles[i][1]) + " views."
        print (line)

    print("")
    print("Top Authors:")
    top_authors = top_viewed_authors()
    for i in range(len(top_authors)):
        line = str(i+1) + ". " + top_authors[i][0]\
            + " -- " + str(top_authors[i][1]) + " views."
        print(line)

    print("")
    print("Days error more than 1%:")
    error_dates = alert_days()
    for i in range(len(error_dates)):
        line = str(error_dates[i][0]) + " -- "\
            + str(round(error_dates[i][1], 2)) + "% errors."
        print(line)
