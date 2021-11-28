import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
import joblib

from sqlalchemy import create_engine



app = Flask(__name__)

# def tokenize(text):
#     tokens = word_tokenize(text)
#     lemmatizer = WordNetLemmatizer()

#     clean_tokens = []
#     for tok in tokens:
#         clean_tok = lemmatizer.lemmatize(tok).lower().strip()
#         clean_tokens.append(clean_tok)

#     return clean_tokens

# load data
engine = create_engine('sqlite:///InsertDatabaseNamemovies_plotly.db')
print("connected ")
df = pd.read_sql_table('moviesplotly', engine)

# load model
model = joblib.load(r"C:\Users\atefi\Downloads\Mostafa FR\Udacity-Data-Scientist-Nanodegree-main\Project 2 - Copy\models\classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    
    genre_counts = df.groupby('title').max()['vote_count']
    genre_names = list(genre_counts.index)
#     'movie_id','budget','popularity','runtime','vote_average','vote_count','revenue'
    
    df1 = df.drop(['movie_id','title','popularity','runtime'], axis=1)
    category_counts=df1.agg("max",axis=1)
    category_names = df1.columns
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        
        
        
         {
            'data': [
                Bar(
                    x=category_names,
                    y=category_counts
                )
            ],

            'layout': {
                'title': 'Distribution Of Movies  ',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Movies - Column"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Max Count-Vote With title',
                'yaxis': {
                    'title': "Max Count-Vote"
                },
                'xaxis': {
                    'title': "Title"
                }
            }
        }
       
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[7]
    classification_results = dict(zip(df.columns[:, :-1], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='127.0.0.1', port=3001, debug=True)


if __name__ == '__main__':
    main()
