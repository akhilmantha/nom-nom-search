# Nom-Nom Search!
It is  a search engine to search gourmet food reviews data and return the top K
reviews with respect to the given input query.

# Stacks used
django, django restframework

## Dataset
Use the dataset available at ​ [http://snap.stanford.edu/data/web​](http://snap.stanford.edu/data/web​) FineFoods.html​ .

# project setup
1. git clone
```html
https://github.com/akhilmantha/nom-nom-search.git
```
2. go to tasty_search directory by: cd tasty_search
3. create a virtualenv using: python3 -m venv . (install python3 on your machine if not already installed) or virtualenv venv (for python 2)
4. activate environment using: source bin/activate or source venv/bin/activate(for python 2)
5. upgrade pip using: pip install --upgrade pip
6. install requirements using: pip install -r requirements.txt
7. create database schema using: python manage.py migrate
8. Generate small sample of dataset by using command:
```html
python manage.py get_small_sample --input_file=assets/foods.txt
```
Possible Options:
* input_file(required): Path of file for foods reviews data.(Default: assets/foods.txt)
* output_file: Path of file for small sample  dataset.(Default: assets/revies_data.json)
* count: Size of sample data required.(Default: 100K)
10. Generate indexed data of sample dataset by using command:
```html
python manage.py get_indexed_data --input_file=assets/reviews_data.json
```
11. run: python manage.py runserver
