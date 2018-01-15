
# Logs Analysis
This is a demo project uses __python__ modules to analyze and report information of a running database.

## Scenario
You've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, your code will answer questions about the site's user activity.

## What is currently analyzing and reporting?
- What are the most popular three articles of all time? Which articles have been accessed the most?
- Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?
- On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.


## Prepare & Run
 - [ ] Install [VirtualBox](https://www.virtualbox.org/)
- [ ] Install [Vagrant](https://www.vagrantup.com/downloads.html)
- [ ] Configure and start virtual machine
	- Clone this repository to your local machine
	- In shell, cd to `/vagrant` folder where `Vagrantfile` lies
	- Run `vagrant up` to configure virtual machine
	- Run `vagrant ssh` to connect to your local machine
	- Change directory to `/vagrant` in your virtual machine
- [ ] Download [news data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), move newsdata.sql to `/vagrant` shared folder
- [ ] Setup Database, execute following command in your virtual machine
	```sql
	psql -d news -f newsdata.sql
	```
- [ ] Run Analysis
	```python
	python analyze.py
	```
## Data set
 __authors table__<br/>
The authors table includes information about the authors of articles.
```sql
CREATE TABLE authors (
    name text NOT NULL,
    bio text,
    id integer NOT NULL
);
```
 __articles table__<br/>
```sql
CREATE TABLE articles (
    author integer NOT NULL,
    title text NOT NULL,
    slug text NOT NULL,
    lead text,
    body text,
    "time" timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);
```
 __log table__<br/>
```sql
CREATE TABLE log (
    path text,
    ip inet,
    method text,
    status text,
    "time" timestamp with time zone DEFAULT now(),
    id integer NOT NULL
);
```
