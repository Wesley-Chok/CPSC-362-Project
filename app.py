from flask import Flask, render_template, request
from random import choice
import requests
import logging

API_URL = 'https://www.themealdb.com/api/json/v1/1/'

def random():
    url = 'https://www.themealdb.com/api/json/v1/1/random.php'
    response = requests.get(url)
    data = response.json()
    return data['meals']

app = Flask(__name__)
@app.route('/')
def home():
    random_recipes = random()
    random_recipes = []
    for i in range(15):
        recipe = random()
        if recipe:
            random_recipes.append(recipe[0])
    return render_template('base.html', random_recipes=random_recipes)

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        response = requests.get(f'{API_URL}search.php?s={query}')
        if response.ok:
            results = response.json().get('meals')
            logging.info(f'Successfully retrieved {len(results)} search results for query "{query}"')
        else:
            results = None
            error_message = f"Error: {response.status_code} - {response.reason}"
            logging.error(f'API call failed with error message: {error_message}')
            return render_template('search.html', query=query, results=results, error_message=error_message)
    else:
        results = None
    logging.info(f'Rendering search results template for query "{query}"')
    return render_template('search.html', query=query, results=results)

@app.route('/recipe/<id>')
def recipe(id):
    response = requests.get(f'{API_URL}lookup.php?i={id}')
    recipe = response.json().get('meals')[0]
    return render_template('recipe.html', recipe=recipe)
