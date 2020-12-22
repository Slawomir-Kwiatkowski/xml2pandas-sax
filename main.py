'''
:description: This program reads data from xml file and creates pandas DataFrame object 
:author: Sławomir Kwiatkowski
:date: 2020-12-22 
'''
import xml.sax
from collections import defaultdict
import pandas as pd

class PersonsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.persons = defaultdict(list)
    def startElement(self, tag, attr):
        self.tag = tag
        if tag == 'person':
            self.persons['id'].append(attr['id'])
            
    def characters(self, content):
        if content.strip():
            if self.tag == 'position': self.position = content
            elif self.tag == 'first_name': self.first_name = content
            elif self.tag == 'last_name': self.last_name = content
            elif self.tag == 'email': self.email = content
            elif self.tag == 'salary': self.salary = content
    
    def endElement(self, tag):
        if tag == 'position': self.persons['position'].append(self.position)
        elif tag == 'first_name': self.persons['first_name'].append(self.first_name)
        elif tag == 'last_name': self.persons['last_name'].append(self.last_name)
        elif tag == 'email': self.persons['email'].append(self.email)
        elif tag == 'salary': self.persons['salary'].append(self.salary)

parser = xml.sax.make_parser()
parser.setContentHandler(PersonsHandler())
parser.parse(open('persons.xml'))
persons = parser.getContentHandler().persons


df = pd.DataFrame(persons, columns=persons.keys()).set_index('id')
df['salary'] = df['salary'].astype(float)
print(df.sort_values(by='salary', ascending=False))

