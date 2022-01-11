import time
import spacy
from flask import Flask, render_template, request
from flask import url_for, redirect, render_template_string
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_paginate import Pagination, get_page_args
from flask_mongoengine import MongoEngine

import en_core_web_sm
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from stop_words import get_stop_words
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import spacy
import en_core_web_lg
import glob
import pandas as pd
from spacy.matcher import Matcher
from spacy import displacy
import visualise_spacy_tree
from IPython.display import Image, display
import os, pdb
import unidecode 
import string
from autocorrect import Speller
from bs4 import BeautifulSoup 
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import regex as re
from spacy.tokens import Doc
from spacy.vocab import Vocab
nltk.download('tagsets')
nltk.help.upenn_tagset('NN')
from nltk import pos_tag
from nltk.tokenize import PunktSentenceTokenizer
import json
from textblob import TextBlob 
nlp = spacy.load("en_core_web_sm")
nltk.download('words')

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['MONGO_URI'] = 'mongodb://localhost:27017/quiz'
mongo = PyMongo(app)

@app.route("/")
def index():
    try:        
        questions = mongo.db.questions.find()
        results_count = questions.count()        
        return render_template('index.html', quest = questions)
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/questions', methods=['POST', 'GET'])
def questions(): 
    msg = ''
    if request.method == 'POST' and 'question' in request.form and 'answer' in request.form :
        question = request.form['question']
        answer = request.form['answer']
        id = mongo.db.questions.insert({'question':question,'answer':answer})
        msg = 'Question successfully insert !'        
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('questions.html', msg = msg)


@app.route("/user")
def user():
    try:        
        questions = mongo.db.questions.find()
        results_count = questions.count()        
        return render_template('user.html', quest = questions)
    except Exception as e:
        return dumps({'error' : str(e)})


@app.route('/result',methods=['POST', 'GET'])
def result():
    msg = ''
    start = time.time()
    if request.method == 'POST':
        questions = mongo.db.questions.find()
        quest = mongo.db.questions.find()
        results_count = questions.count()
        
        #print(results_count)
        
        ques_id = request.form.getlist('id[]')
        ques = request.form.getlist('question[]')
        ques_ans = request.form.getlist('youranswer[]')   


        tmplist1 = []
        for uq in ques_ans:
            doc1 = nlp(uq)
            tmplist1.append(doc1) 
            #print(tmplist1)

        tmplist2 = []    
        for questions in questions:
            doc2 = nlp(questions['answer'])
            tmplist2.append(doc2)
            #print(tmplist2)

        tmplist3 = []    
        for x in range(results_count):
            print(x)
            doc3 = (tmplist1[x].similarity(tmplist2[x])*100,"%")
            tmplist3.append(doc3)
            #print(tmplist3)
        '''r = str(ques_ans)
        docx = nlp(r)
        custom_tokens = [token.text for token in docx ]
        custom_wordinfo = [(token.text,token.lemma_,token.is_stop) for token in docx ]
        lowered_text = ques_ans.lower()
        length_text = str(len(ques_ans))
        remove_punctuation = [token for token in docx if not token.is_punct]
        ' '.join(token.text for token in remove_punctuation)
        remove_whitespace = ques_ans.replace("   " , "").strip()
        custom_postagging = [(word.text,word.tag_,word.pos_,word.dep_) for word in docx]
        custom_namedentities = [(entity.text,entity.label_)for entity in docx.ents]
        blob = TextBlob(ques_ans)
        blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
		# allData = ['Token:{},Tag:{},POS:{},Dependency:{},Lemma:{},Shape:{},Alpha:{},IsStopword:{}'.format(token.text,token.tag_,token.pos_,token.dep_,token.lemma_,token.shape_,token.is_alpha,token.is_stop) for token in docx ]
        allData = [('"Token":"{}","Tag":"{}","POS":"{}","Dependency":"{}","IsStopword":"{}"'.format(token.text,token.tag_,token.pos_,token.dep_,token.is_stop)) for token in docx ]
        result_json = json.dumps(allData, sort_keys = False, indent = 2)
        end = time.time()
        final_time = end-start
        
    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'''
    return render_template('result.html', msg = msg, quest = quest, yourans = ques_ans, quesid = ques_id, resultscount = results_count,tmplist3=tmplist3)   






if __name__ == "__main__":
    app.run(debug=True)
