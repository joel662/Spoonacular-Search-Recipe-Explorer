from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(__name__)

API_KEY = "API_KEY"

@app.route('/home', methods=['GET'])
def home():
    # Perform a search for recipes with the given query
    return render_template('index.html', recipes=[], search_query='')

# Define the main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  
        query = request.form.get('search_query', '')  
        recipes = search_recipes(query)
        return render_template('index.html', recipes=recipes, search_query=query)
    
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)
def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }


    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['results']

    return []

# Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    # Get the search query from the URL query parameters
    search_query = request.args.get('search_query', '')
    # Build the URL to get information about the specific recipe ID from Spoonacular API
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404

if __name__ == '__main__':
    app.run(debug=True)