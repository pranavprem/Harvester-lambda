import math

class SMMRY:
    def __init__(self, sentences, matrix):
        self.matrix = matrix
        self.distances = self.make_distance_vector()
        self.sentences = sentences

    def distance(self,list1,list2):
        numerator=0
        denominator=0
        s1=s2=0
        for i in range(0,len(list1)):
            numerator+=list1[i]*list2[i]
            s1+=list1[i]*list1[i]
            s2+=list2[i]*list2[i]
        s1=math.sqrt(s1)
        s2=math.sqrt(s2)
        denominator=s1*s2
        if denominator==0.0:
            return 0
        return numerator/denominator
    
    def make_distance_vector(self):
        distances=[]
        for row1 in self.matrix:
            temp=0
            for row2 in self.matrix:
                temp+=self.distance(row1,row2)
            distances.append(temp)
        return distances

    def get_important_sentences(self):
        sentence_map = dict()
        print len(self.sentences)
        print len(self.distances)
        for i in range(0, len(self.sentences)):
            sentence_map[self.sentences[i]]=self.distances[i]
        sentence_map = sorted(sentence_map.iteritems(),key=lambda kv:kv[1],reverse=True)
        important_sentences=[]
        prev=0
        for sentence in sentence_map[:10]:
            for i in range(0,len(sentence[0])):
                if not sentence[0][i].isalpha() and sentence[0][i]!=' ':
                    important_sentences.append(sentence[0][prev:i])
                    prev = i
            important_sentences.append(sentence[0][prev:])
        important_sentences = [sentence for sentence in important_sentences if len(sentence)>30]
        return important_sentences