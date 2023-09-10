# Flask
from flask import Flask, render_template, request
# Data manipulation
import pandas as pd
# Matrices manipulation
import numpy as np
# Script logging
import logging
# ML model
import joblib
# JSON manipulation
import json
# Utilities
import sys
import os

# Current directory
#current_dir = os.path.dirname(__file__)
current_dir = os.path.dirname('C:/Users/PERFECTO/PROJET_7_avec_FLASK_TEST/')

#'C:/Users/User/'
#PROJET_7_avec_FLASK_Api


# Flask app
app = Flask(__name__, static_folder = 'static', template_folder = 'template')

# Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Function
def ValuePredictor(data = pd.DataFrame):
	# Model name
	model_name = 'bin/model_7_saved.pkl'
	# Directory where the model is stored
	# model_dir = os.path.join(current_dir, model_name)
	model_dir = 'model_7_saved.pkl'


	# Load the model
	loaded_model = joblib.load(open(model_dir, 'rb'))
	# Predict the data
	result = loaded_model.predict(data)
	return result[0]

# Home page
@app.route('/')
def home():
	return render_template('index.html')

# Prediction page
@app.route('/prediction', methods = ['POST'])
def predict():
	if request.method == 'POST':
		# Get the data from form
		name = request.form['name']
		genre = request.form['genre']
		statut_du_contrat = request.form['statut_du_contrat']
		nombre_enfants = request.form['nombre_enfants']
		nombre_famille_membre = request.form['nombre_famille_membre']
		type_de_client = request.form['type_de_client']
		jours_depuis_dernier_credit = request.form['jours_depuis_dernier_credit']
		situation_crédit = request.form['situation_crédit']
		possession_voiture = request.form['possession_voiture']
		montant_total_crédits = request.form['montant_total_crédits']
		revenu_total = request.form['revenu_total']
		rente_annuelle_crédit = request.form['rente_annuelle_crédit']
		prix_biens_achetés = request.form['prix_biens_achetés']
		durée_crédit_précédent = request.form['durée_crédit_précédent']


		
		# Load template of JSON file containing columns name
		# Schema name
		#schema_name = 'data/columns_set.json'
		schema_name = 'columns_set.json'
				
		# Directory where the schema is stored
		#schema_dir = os.path.join(current_dir, schema_name)
		#schema_cols = pd.read_json(schema_dir).to_dict()['data_columns']

		# absolute path to this file
		#FILE_DIR = os.path.dirname(os.path.abspath('columns_set.json'))
		# absolute path to this file's root directory
		#PARENT_DIR = os.path.join(FILE_DIR, os.pardir) 
		#schema_dir = os.path.join(PARENT_DIR, schema_name)




		reza = {
					"data_columns": {
					"CODE_GENDER": "",
					"CNT_CHILDREN": "",
					"CNT_FAM_MEMBERS": "",
					"NAME_FAMILY_STATUS": "",
					"NAME_EDUCATION_TYPE": "",
					"NAME_HOUSING_TYPE": "",
					"FLAG_OWN_REALTY": "",
					"FLAG_OWN_CAR": "",
					"AMT_CREDIT_SUM": "",
					"AMT_INCOME_TOTAL": "",
					"NAME_INCOME_TYPE": "",
					"NAME_CONTRACT_TYPE": "",
					"CNT_INSTALMENT_FUTURE": "",
					"CREDIT_ACTIVE": ""

					}
					}

		schema_colsSS = reza['data_columns']

		
		#current_dirO = os.path.dirname('C:/Users/PERFECTO/Documents')
		#schema_dir = os.path.join(current_dirO, schema_name)
		schema_dir = schema_name


		with open(schema_dir, 'r') as f:
			cols =  json.loads(f.read())
		schema_cols = cols['data_columns']

		
		

		# Parse the numerical columns
		schema_cols['CNT_CHILDREN'] = nombre_enfants
		schema_cols['CNT_FAM_MEMBERS'] = nombre_famille_membre
		schema_cols['NAME_CONTRACT_STATUS'] = statut_du_contrat
		schema_cols['CNT_PAYMENT'] = durée_crédit_précédent
		schema_cols['CODE_GENDER'] = genre
		schema_cols['CREDIT_ACTIVE'] = situation_crédit
		schema_cols['AMT_GOODS_PRICE'] = prix_biens_achetés
		schema_cols['AMT_ANNUITY_x'] = rente_annuelle_crédit
		schema_cols['FLAG_OWN_CAR'] = possession_voiture
		schema_cols['AMT_CREDIT_SUM'] = montant_total_crédits
		schema_cols['AMT_INCOME_TOTAL'] = revenu_total
		schema_cols['DAYS_CREDIT'] = jours_depuis_dernier_credit
		schema_cols['NAME_CLIENT_TYPE'] = type_de_client
		

		# Convert the JSON into data frame
		df = pd.DataFrame(
				data = {k: [v] for k, v in schema_cols.items()},
				dtype = float
			)

		# Create a prediction
		print(df.dtypes)
		result = ValuePredictor(data = df)

		# Determine the output
		if int(result) == 1:
			prediction = 'Cher Mr/Mrs/Ms {name}, votre demande de crédit est approuvée!'.format(name = name)
		else:
			prediction = 'Désolé Mr/Mrs/Ms {name}, votre demande de crédit est rejetée!'.format(name = name)

		# Return the prediction
		return render_template('prediction.html', prediction = prediction)
	
	# Something error
	else:
		# Return error
		return render_template('error.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug = True)