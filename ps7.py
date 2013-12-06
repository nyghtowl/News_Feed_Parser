# 6.00.1x Problem Set 7
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 7

#======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    '''
    Creates object to store rss content
    '''
    def __init__(self, guid, ns_title, ns_subject, ns_summary, link):
        self.guid = guid
        self.ns_title = ns_title
        self.ns_subject = ns_subject
        self.ns_summary = ns_summary
        self.link = link

    def getGuid(self):
        return self.guid

    def getTitle(self):
        return self.ns_title

    def getSubject(self):
        return self.ns_subject

    def getSummary(self):
        return self.ns_summary

    def getLink(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

def clean_text(text):
    """
    Returns text string with punctionation 
    replaced by space and all text lowercase
    """
    exclude = set(string.punctuation)
    text = str(text)
    for punc in exclude:
        text = text.replace(punc, ' ') 
    return text.lower()

# TODO: WordTrigger
class WordTrigger(Trigger):
    '''
    Creates object to manage whole word and creates 
    abstract for category specific triggers
    '''
    def __init__(self, word):
        self.word = word

    def isWordIn(self, text):
        text_revised = clean_text(text)
        text_list = text_revised.split()
        if self.word.lower() in text_list:
            return True
        return False

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    """
    Returns evaluation if word in news title
    """
    def evaluate(self, news):
        return self.isWordIn(news.getTitle())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    """
    Returns evaluation if word in news subject
    """
    def evaluate(self, news):
        return self.isWordIn(news.getSubject())

# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    """
    Returns evaluation if word in news summary
    """
    def evaluate(self, news):
        return self.isWordIn(news.getSummary())



# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    """
    Returns opposite trigger evaluation
    """
    def __init__(self, subTrigger):
        self.subTrigger = subTrigger

    def evaluate(self, news):
        return not self.subTrigger.evaluate(news)

# TODO: AndTrigger
class AndTrigger(Trigger):
    """
    Returns if both tiggers activated
    """
    def __init__(self, subTrigger1, subTrigger2):
        self.subTrigger1 = subTrigger1
        self.subTrigger2 = subTrigger2

    def evaluate(self, news):
        return self.subTrigger1.evaluate(news) and self.subTrigger2.evaluate(news)

# TODO: OrTrigger
class OrTrigger(Trigger):
    """
    Returns if one or the other tiggers are activated
    """
    def __init__(self, subTrigger1, subTrigger2):
        self.subTrigger1 = subTrigger1
        self.subTrigger2 = subTrigger2

    def evaluate(self, news):
        return self.subTrigger1.evaluate(news) or self.subTrigger2.evaluate(news)


# Phrase Trigger
# Question 9
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    """
    Returns if phase in news title, subject or summary
    """

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, news):
        return self.phrase in (news.getTitle() + news.getSummary() + news.getSubject())

#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    stories_result = set()
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                stories_result.add(story)
    return stories_result

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns a new instance of a trigger (ex: TitleTrigger, AndTrigger).
    """

    def createWord(subc, params):
        return subc(''.join(params))

    def createPhrase(subc, params):
        return subc(' '.join(params))

    def lookup(subc, params):
        return subc(triggerMap[params[0]])

    def applyTwoParams(subc, params):
        return subc(triggerMap[params[0]],triggerMap[params[1]])

    trigger_dict = {
            'TITLE': (createWord, TitleTrigger),
            'SUBJECT': (createWord, SubjectTrigger),
            'SUMMARY': (createWord, SummaryTrigger),
            'NOT': (lookup, NotTrigger),
            'AND': (applyTwoParams, AndTrigger),
            'OR': (applyTwoParams, OrTrigger),
            'PHRASE': (createPhrase, PhraseTrigger)
            }
    
    constructor, subclass = trigger_dict[triggerType]


    triggerMap[name] = constructor(subclass, params) 
    return triggerMap[name]



def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    triggerMap = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Obama")
        t2 = SubjectTrigger("Romney")
        t3 = PhraseTrigger("Election")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:
        # triggerlist = readTriggerConfig("triggers.txt")

        # **** from here down is about drawing ****
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)

        # Gather stories
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            # Process the stories
            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()

