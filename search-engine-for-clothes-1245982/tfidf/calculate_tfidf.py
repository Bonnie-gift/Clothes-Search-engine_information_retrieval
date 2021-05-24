import nltk
import string
import os
from flask import Flask, render_template, flash, redirect, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql://root:@localhost:3306/wardrobe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'a random string'

app.config.from_object('config')
db = SQLAlchemy(app)

class wardrobe(db.Model):
    """ 新闻模型 """
    __tablename__ = 'private_wardrobe_for_bonnie'
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.Enum('Sweaters', 'Denim', 'Blazers', 'Pants','Shirts','Blousers'))
    color = db.Column(db.String(200), nullable=False)
    brand= db.Column(db.String(200), nullable=False)
    year_to_buy = db.Column(db.String(4),nullable=False)
    location= db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(300),nullable=False)
    description = db.Column(db.String(300),nullable=False)
    tf_idf=db.Column(db.String(300),nullable=True)
    def __repr__(self):
        return '<Wardrobe %r>' % self.classification

path = 'Data'
token_dict = {}
stemmer = PorterStemmer()

def get_data():
    query = wardrobe.query.all()
    query_list=list(query)
    return query_list
def get_description(docs_list):
    """ 
    get only content of document 
    and format it to lower case and remove all special chars
    """
    contents = []

    for doc in docs_list:
        text = doc[7]
        contents.append(text)

    return contents

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def update(pk,value):
    obj = wardrobe.query.get(pk)
    if obj is None:
        abort(404)
    obj.tf_idf = value
        
def get_result(id):
    query_list=get_data()
    contents=get_description(query_list)
    for text in contents:
        lowers = text.lower()
        # no_punctuation = lowers.translate(None, string.punctuation)
        no_punctuation = lowers.translate(str.maketrans('','',string.punctuation))
        token_dict[text] = no_punctuation
        
    #this can take some time
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_dict.values())
    print(tfs)
    # compressed sparse row matrix (type of sparse matrix with fast row slicing)
    sparse_row_matrix = tfs.tocsr()
    #print("Sparse matrix")
    #print(sparse_row_matrix.toarray()) # convert to array
    # compute similarity between each pair of documents
    similarities = cosine_similarity(sparse_row_matrix)

    #print("Similarity matrix")
    print(similarities)
    scores={}
    simi_list=similarities[id-1]
    i=0
    for col in simi_list:
        scores[i]=col
        i=i+1
    # sort according to the value
    a = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for items in a:
        pk=items[0]
        value=items[1]
        update(pk,value)


    