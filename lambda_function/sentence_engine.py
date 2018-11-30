"""Class that takes a URL and returns list of sentences.
"""
import html2text
import urllib2
import string
import math
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

class sentence_engine:
    """Sentence Engine class definition
    """

    """Constructor
    Takes URL as argument and uses html2text to obtain text version of the html
    """
    def __init__(self, url):
        nltk.download('stopwords')
        nltk.download('punkt')
        self.html = self.get_html(url)
        self.text = ""
        self.get_text()

    """Function to return true if html tag is visible on screen when page loads
    """
    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    """Function converts html to text
    """
    def get_text(self):
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = True
        text_maker.escape_snob = 1
        self.text = text_maker.handle(self.html)


    """Method takes url and returns html on the page.
    """
    def get_html(self, url):
        response = urllib2.urlopen(url)
        html = response.read()
        encoded_html = html.decode('utf-8')
        decoded_html = encoded_html.encode('ascii','ignore')
        return decoded_html

    
    def filter(self, lines):
        stop_words = set(stopwords.words('english'))
        toks = []
        token_map = dict()
        sentences = dict()
        matrix = []
        bag=set()
        #Get bag of words
        for line in lines:
            if len(line)>5:
                tokens= word_tokenize(line)
                tokens = [w.lower() for w in tokens]
                tokens = [word for word in tokens if word.isalpha()]
                tokens = [w for w in tokens if w not in stop_words]
                toks.extend(tokens)
                sentences[line]=tokens
        for token in set(toks):
            if toks.count(token)>5:
                token_map[token] = toks.count(token)
        token_map = sorted(token_map.iteritems(),key=lambda kv:kv[1],reverse=True)
        if len(token_map)>20:
            token_map = token_map[:20]
        for (key, value) in token_map:
            bag.add(key)
        #return bag


        for line in sentences:
            temp = []
            for word in bag:
                temp.append(sentences[line].count(word))
            matrix.append(temp)
        return sentences, matrix
        
        
        
        


    """Method that iterates over text version of html, prunes and returns a list of sentences
    """
    def get_sentences(self):
        lines = self.text.encode('ascii','ignore').split("\n")
        return self.filter(lines)
        
    
