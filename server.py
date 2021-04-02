import rpyc
import xml.etree.ElementTree as ET
import requests as rq

#start the database
tree = ET.parse("db.xml")
root = tree.getroot()
#partly taken from:
#https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
class server(rpyc.Service):

    
    #what gets done when connection starts
    def on_connect(self,conn):
        pass

    
    #what gets done when connection closes
    def on_disconnect(self,conn):
        pass

    
    #returns list of topics
    def exposed_get_topics(self,user):
        #log on console
        print(user+": Topics requested")
        #make an empty list
        ret = []
        #add all topics to list
        for topic in root:
            ret.append(topic.attrib["name"])
        #send the list to client 
        return ret

    
    #returns topic
    def exposed_get_topic(self,user,topicName):
        #log
        print(user+": "+topicName+" requested")
        #checks if the topic exist Case sensitive and propably there there is method that would be better
        for topic in root:
            #if topic found returns the element of the tree
            if topic.attrib["name"] == topicName:
                return topic
        #if no topic found returns 0
        return 0

    
    #adds a topic or appends a topic if already created
    def exposed_add_topic(self,user,topic,noteName,note,date):
        
        topicExists = False
        #checks if topic exists
        for itopic in root:
            if itopic.attrib["name"] == topic:
                ##set the variable to the topic if found
                topicExists = itopic
        ##create elements
        Note = ET.Element("note",{"name" : noteName})
        Tele = ET.Element("text")
        
        #https://www.mediawiki.org/wiki/API:Opensearch

        ##creates request to the wikipedia
        try:
            Session = rq.Session()
            endpoint = "https://en.wikipedia.org/w/api.php"
            parameters = {"action":"opensearch","namespace":"0","search":noteName,"limit":"1","format":"json"}
            R = Session.get(url=endpoint, params=parameters)
        ##takes the json
            data = R.json()
        ##checks if the json contains link
            if data[1]:
            ##makes link element if link found (sometimes not accurate)
                link = ET.Element("link")
                link.text = "possible wikipedia topic: " + data[1][0] + " : " + data[3][0]
                Note.append(link)
        ##creates text and date element
        except:
            print("something went wrong when getting link for \""+noteName+"\"")
        Tele.text = note
        Dele = ET.Element("timestamp")
        Dele.text = date
        Note.append(Tele)
        Note.append(Dele)
        ##checks if earlier search found topic
        if topicExists != False:
            ##appends the topic if found
            topicExists.append(Note)
        else:
            ##creates new topic element and appends it to the data node
            Topic = ET.Element("topic",{"name":topic})
            Topic.append(Note)
            root.append(Topic)
        #log
        print(user+": Topic add requested\ntopic: " + topic+"\nnote:"+note+"\ndate:"+date)
        pass


#taken from:
#https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html
if __name__ == "__main__":
    #import and start server on port 1234
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(server, port=1234, protocol_config={"allow_public_attrs":True,})
    print("server start")
    t.start()
    ##writes the data back to the file when server stops (for example ctrl+c) method creates acceptable xml but misses new lines
    tree.write("db.xml")
