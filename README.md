# Disaster response app

The present code uses an ETL and machine learning pipeline to categorize responses during a disaster. The dataset was provided by Figure Eight (now acquired by [Appen](https://appen.com) and contains pre-labeled tweets and text messages from real-life disasters. This code cleans and reorganizes the dataset to build a machine learning model. The model can tag a tweet or message with an appropriate response organization to help during an ongoing disaster. During such threatening events, help organizations lack the required capacity to filter the millions of tweets to focus on the real important ones. The machine learning model provided here can speed up the work of delivering medical supplies, and water, or attending to blocked roads.

## Quick start
Clone the repo: `git clone https://github.com/chinchay/disaster-response-app.git`

## How to use it

This code is organized in 3 directories:
* app/
    * `run.py`
    * templates/
        * `go.html`
        * `master.html`
* data/
    * `disaster_messages.csv`
    * `disaster_categories.csv`
    * `etl_pipeline.py`
* models/
    * `train_classifier.py`


### ETL pipeline

The code provided follows an ETL pipeline. The pipeline loads the `*.csv` datasets, merge and cleans them, and stores the result information in an SQLite database `*.db`. To start the process, the user needs to enter into the `data/` folder and type the following:

```ShellSession
$ python etl_pipeline.py disaster_messages.csv disaster_categories.csv DisasterResponse.db
```

### Machine learning pipeline

A machine learning pipeline loads the SQLite dataset, splits it into training and test sets, builds a machine learning model to process the text and train on it using GridSearchCV, and outputs the result on the test set. The `run.py` script exports the model as a pickle file `*.pkl`. The job is initiated by typing the following:

```ShellSession
$ cd ../models/
$ python train_classifier.py "../data/DisasterResponse.db" classifier.pkl
```

### Flask Web App

The `*.pkl` file created in the previous step is loaded by the application:

```ShellSession
$ python run.py
```

The model is working and ready for visualization on `http://127.0.0.1:3000` in your local machine.


![](imgs/app.png)
**Fig 1**. App screenshot. The "We are thirsty" tweet is channeled to the appropriate aid organization.

## Copyright and license
Code released under the MIT License