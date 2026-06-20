# Ans-To-Ans Similarity Matching

## Project Overview

Ans-To-Ans Similarity Matching is a web-based application that automatically evaluates a user's answer by comparing it with a predefined model answer. Instead of relying solely on keyword matching, the system uses Natural Language Processing (NLP) techniques to measure the semantic similarity between the two answers and generates a similarity score.

The project is designed as a prototype for automated subjective answer evaluation systems that can be used in online quizzes, educational platforms, and assessment tools.

## Tech Stack

### Backend

* Python
* Flask

### Database

* MongoDB
* Flask-PyMongo

### Natural Language Processing

* spaCy
* NLTK
* TextBlob

### Deployment

* Gunicorn
* Heroku

## Key Features

* Store questions and model answers in MongoDB.
* Submit answers through a web interface.
* Compare user answers with reference answers using NLP-based semantic similarity.
* Generate similarity scores automatically.
* Simple Flask-based architecture for easy deployment and extension.
