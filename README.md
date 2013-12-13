News Feed Parser (MIT Comp Sci Project)
================

In problem set 7, you will build a program to monitor news feeds over the Internet. Your program will filter the news, alerting the user when it notices a news story that matches that user's interests (for example, the user may be interested in a notification whenever a story related to the Red Sox is posted).


Objectives
===
The goal of this problem set is to help you become familiar and comfortable with the following topics:

* Many facets of object oriented programming, specifically:

* Implementing new classes and their attributes.

* Understanding class methods.

* Understanding inheritance.

* Telling the difference between a class and an instance of that class - recall that a class is a blueprint of an object, whilst an instance is a single, unique unit of a class.

* Utilizing libraries as black boxes.

RSS Overview
===
Many websites have content that is updated on an unpredictable schedule. News sites, such as Google News, are a good example of this. One tedious way to keep track of this changing content is to load the website up in your browser, and periodically hit the refresh button. Fortunately, this process can be streamlined and automated by connecting to the website's RSS feed, using an RSS feed reader instead of a web browser (e.g. Sage). An RSS reader will periodically collect and draw your attention to updated content.

RSS stands for "Really Simple Syndication". An RSS feed consists of (periodically changing) data stored in an XML-format file residing on a web-server.