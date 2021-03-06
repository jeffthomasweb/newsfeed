from flask import Flask, jsonify
from flask.templating import render_template #Use flask.templating and render_template to display site as a html file
import feedparser #To Parse RSS Feeds
import re #Python Regular Expression Library

app = Flask(__name__)

#Write a general function to get RSS Data and use the function later in this file under @app.route("/")
#General function is named def rss(rss_address) 
#Gets RSS data using the function parameter rss_address

def rss(rss_address):
    #Use feedparser to get the RSS feed data and parse the story titles and summaries
    feedparser_parse = feedparser.parse(f"{rss_address}")
    #Create an empty list to add RSS feed story titles and summaries
    story_list = []
    #feedparser is a great library but it doesn't parse some html tags like <em> and </em>
    #Create an empty list clean_story_list1 to add RSS feed data cleaned of <em> tags 
    clean_story_list1 = []
    #Create an empty list clean_story_list2 to add RSS feed data cleaned of </em> tags
    clean_story_list2 = []
    #Append 15 story titles and summaries to story_list
    for i in range(0,15):
        story_list.append(feedparser_parse.entries[i].title + '. ' + feedparser_parse.entries[i].summary)
    
    #Clean items in story_list of <em> tags and append to clean_story_list1
    for cleantag in story_list:
        clean_story_list1.append(re.sub('<em>', '', cleantag))

    #Clean items in story_list1 of </em> tags and append to clean_story_list2
    for cleantag2 in clean_story_list1:
        clean_story_list2.append(re.sub('</em>', '', cleantag2))
    
    return clean_story_list2

#Use function for NPR RSS feed and save as npr_list
npr_list = rss("https://feeds.npr.org/1001/rss.xml")

#Use function for Ars Technica feed
ars_list = rss("https://feeds.arstechnica.com/arstechnica/index")

#Use function for local Buffalo news station feed
buffalo_list = rss("https://www.wgrz.com/feeds/syndication/rss/news/local")

#Visiting the main site URL will show the stories as a normal HTML site.
@app.route("/")
def home():
    return render_template("index.html", npr_list=npr_list, ars_list=ars_list, buffalo_list=buffalo_list)

#Create a /news route. Anyone visiting the website with a url ending in /news will 
#see a JSON version of the RSS data.
@app.route("/news")
def news():
    return jsonify(npr_list,ars_list,buffalo_list)

if __name__ == '__main__':
    app.run()
