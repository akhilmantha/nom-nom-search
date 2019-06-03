# Nom-Nom Search!
It is  a search engine to search gourmet food reviews data and return the top K
reviews with respect to the given input query.

# Frameworks used
django, django restframework

## Dataset
Use the dataset available at ​ [http://snap.stanford.edu/data/web​](http://snap.stanford.edu/data/web​) FineFoods.html​ .

# project setup
1. git clone
```html
https://github.com/akhilmantha/nom-nom-search.git
```
2. go to tasty_search directory by: cd tasty_search
3. create a virtualenv using: virtualenv venv (for python 2)
4. activate environment using: source venv/bin/activate(for python 2)
5. install django and djangorestfrawork using 
```html
pip install django
```
If you get an error saying 'No module named rest_framework' then you need to install
```html
sudo pip install djangorestframework
```
6. Generate small sample of dataset by using command:
```html
python manage.py get_small_sample --input_file=assets/foods.txt
```
Possible Options:
* input_file(required): Path of file for foods reviews data.(Default: assets/foods.txt)
* output_file: Path of file for small sample  dataset.(Default: assets/reviews_data.json)
* count: Size of sample data required.(Default: 100K, reduced:50k)

7. Generate indexed data of sample dataset by using command:
```html
python manage.py get_indexed_data --input_file=assets/reviews_data.json
```

8. run: python manage.py runserver. You will see something with your machine ip and port number
   ```html
    http://192.168.0.1:8000/
   ```
   api end-point:
    ```html
    /api/v1/search/
   ```
   
9. Query an input either in raw or html form, something like
    ```html
    cat, processed, bad, good 
   ```
   Query Result:
   ```html
    {
        "review/profileName": "delmartian",
        "review/time": "1303862400",
        "product/productId": "B001E4KFG0",
        "review/helpfulness": "1/1",
        "review/summary": "Good Quality Dog Food",
        "review/userId": "A3SGXH7AUHU8GW",
        "review/score": "5.0",
        "review/text": "I have bought several of the Vitality canned dog food products and have found them all to be of good quality. The         product looks more like a stew than a processed meat and it smells better. My Labrador is finicky and she appreciates this product          better than  most."
    },
    {
        "review/profileName": "Nah",
        "review/time": "1289174400",
        "product/productId": "B0083QJU72",
        "review/helpfulness": "1/1",
        "review/summary": "Great Syrup",
        "review/userId": "A298Q94MFT4VED",
        "review/score": "5.0",
        "review/text": "I have been using this syrup for over a year, and it is the tastiest I have ever had.  When out of it, I tried              some Grade A Dark Amber from Target (same price), and it just wasn't as good.  Full of maple flavor and none of the corn syrup            junk of the table brands, this syrup really brought breakfast to a whole new level of yummy!"
    },
    {
        "review/profileName": "ET Bride \"Shulamite\"",
        "review/time": "1289001600",
        "product/productId": "B0083QJU72",
        "review/helpfulness": "1/1",
        "review/summary": "Great Price!",
        "review/userId": "A219Y4VESH24S3",
        "review/score": "5.0",
        "review/text": "This is a great price for Grade B maple.  I bought it for the Lemonade Diet and found it to be good to the last           drop!"
    },
    {
        "review/profileName": "J. Beardsley",
        "review/time": "1277337600",
        "product/productId": "B0083QJU72",
        "review/helpfulness": "1/1",
        "review/summary": "The Best Maple Syrup I've Ever Tasted",
        "review/userId": "A1U1ALQQMB6J22",
        "review/score": "5.0",
        "review/text": "Half my family is from the Maple Syrup State of Vermont, so I've had a lot of good maple syrup in my time.  Coombs          Grade B Organic is the best I've ever had, full of rich taste and minerals!"
    },
   ```
