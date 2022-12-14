import sys
import pandas as pd
from sqlalchemy import create_engine
import re
from nltk.tokenize import word_tokenize

from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression

import pickle



def load_data(database_filepath):
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('categorized_messages', engine)
    X = df[ 'message' ].values
    Y = df.drop([ 'id', 'message', 'original', 'genre' ], axis=1).values
    category_names = df.columns[4:]
    return X, Y, category_names
#

def tokenize(text):
    # normalize case and remove punctuation
    text = re.sub( r"[^a-zA-Z0-9]", " ", text.lower() )

    # tokenize text
    tokens = word_tokenize(text)

    # lemmatize andremove stop words
    tokens = [ lemmatizer.lemmatize(t) for t in tokens if t not in stopwords.words("english")  ]

    return tokens
#

def build_model():
    # build pipeline
    pipeline = Pipeline( [
        ('vect',  CountVectorizer(tokenizer=tokenize) ),
        ('tfidf', TfidfTransformer() ),
        ('clf', MultiOutputClassifier(RandomForestClassifier()) )
        # ('clf', RandomForestClassifier() )
    ] )
    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    Y_pred = model.predict(X_test)
    print( classification_report(Y_test, Y_pred, target_names=category_names) )


def save_model(model, model_filepath):
    with open(model_filepath, 'wb') as f:
        pickle.dump(model, f)
    #


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        # evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()