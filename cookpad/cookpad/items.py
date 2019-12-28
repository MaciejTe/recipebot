from scrapy.item import Item, Field


class Ingredient(Item):
    name = Field()
    quantity = Field()


class Recipe(Item):
    """
    Class containing all possible recipe fields.
    """
    id = Field()
    name = Field()
    author = Field()
    description = Field()
    ingredients = Field()
    instructions = Field()
    servings = Field()
    published_date = Field()
    updated_date = Field()
    link = Field()
    duration = Field()


class CookpadRecipe(Recipe):
    """
    Custom Cookpad recipe fields.
    """
    category = Field()  # Stores only the main category
    categories = Field()  # Stores all of the relevant categories, including parents
    image_main = Field()
    images_instruction = Field()
    related_keywords = Field()
