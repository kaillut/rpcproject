import sys
import xml.etree.ElementTree as ET
import rpyc
from datetime import datetime as d
import requests as rq
#get connection details
print("address:")
adr = input()
print("port:")
port = input()
#Name is only for loggin purposes
print("name:")
name = input()
##get connection to the server
connection = rpyc.connect(adr,int(port))
r = connection.root


#main loop
while 1==1:
    #prints help and waits for input
    print("commands:\nexit\t-exits\nadd\t-add or append a topic\nread\t-read a topic\nsearch\t-search a topic in wikipedia\ntopics\t-show topics on server\nchoice:")
    choice =input()
    ##checks the input
    if choice == "exit":
        sys.exit()
    elif choice == "add":
        ##asks for the information about note
        print("What topic would you like to add/append to?")
        Topic = input()
        print("What would you like to name the note?")
        Nname = input()
        print("What text would you like to add?")
        Text = input()
        ##sends the information to server
        r.add_topic(name,Topic,Nname,Text,d.now().strftime("%d/%m/%Y - %H:%M:%S"))
        pass
    elif choice == "read":
        ##asks what topic you would like to read
        print("What topic would you like to read?")
        topicN = input()
        ##gets the topic from server
        topic = r.get_topic(name,topicN)
        ##checks if the response actually contains topic
        if topic==0:
            print("No such topic found")
        else:
            ##loops through the notes
            for i in topic:
                print(i.attrib["name"])
                ##loops through the link, text and timestamp fields
                for ii in i:
                    print(ii.text.strip())
        pass
    elif choice == "search":
        #https://www.mediawiki.org/wiki/API:Opensearch
        ##asks for input
        print("what would you like to search wikipedia for?")
        search = input()
        ##makes request to the wikipedia
        Session = rq.Session()
        endpoint = "https://en.wikipedia.org/w/api.php"
        parameters = {"action":"opensearch","namespace":"0","search":search,"limit":"3","format":"json"}
        R = Session.get(url=endpoint, params=parameters)
        ##gets the json response
        data = R.json()
        ##checks if articles found
        if not data[1]:
            print("no articles found")
        else:
            ##prints the first 3 articles
            print("1."+data[1][0]+" : "+data[3][0])
            print("2."+data[1][1]+" : "+data[3][1])
            print("3."+data[1][2]+" : "+data[3][2])
        pass
    elif choice == "topics":
        ##request topics from the server
        topics = r.get_topics(name)
        ##loops trough the topics and prints them
        for tname in topics:
            print(tname)
        pass
    else:
        print("command not recognised")
        
