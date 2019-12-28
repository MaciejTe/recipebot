# Recipebot

[![License](https://img.shields.io/github/license/MaciejTe/recipebot.svg?maxAge=2592000)](https://github.com/MaciejTe/recipebot/LICENSE)

Python web scraper based on Scrapy framework for obtaining recipe data from most popular cooking websites.


## Supported websites
1. https://cookpad.com/

## How to run

 1. Create Python virtualenv
 
    ```bash
    python3 -m venv recipevenv 
    ```
 
 2. Activate Python virtualenv
    
    ```bash
    source recipevenv/bin/activate

    ```
 
 3. Install Linux dependencies (for proper SQLAlchemy functioning)
 
    ```bash
    sudo apt install libpq-dev libffi-dev python3-dev libxml2 libxml2-dev libxslt-dev

    ```
    
 4. Install Python libraries
 
    ```bash
    python setup.py install

    ```
 
 5. Launch scrapy
    
    - Save recipes to postgreSQL database :
    
    ```bash
    scrapy crawl cookpadbot -a category=vegan
    ```
    
    - Save recipes to JSON file (if you want to disable saving to postgreSQL DB, 
    comment ITEM_PIPELINES variable in cookpad/cookpad/settings.py file):
    
    ```bash
    scrapy crawl cookpadbot -o vegetarian.json -a category=vegetarian
    ```
 
 6. To deactivate virtual environment:
    
    ```bash
    deactivate
    ```


## Sample recipes
    
    Sample recipes available in cookpad/cookpad/sample_recipes directory.
