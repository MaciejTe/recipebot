from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from cookpad.items import CookpadRecipe, Ingredient

from re import findall


class CookpadSpider(CrawlSpider):
    """
    Cookpad.com Crawl spider.
    """
    name = 'cookpad.com'
    allowed_domains = ['cookpad.com']
    rules = (
        # Follow pagination
        Rule(LinkExtractor(allow=(r"uk/search/\w+\?page=\d+",)), follow=True),

        # Extract recipes
        Rule(LinkExtractor(allow=(r"recipes/\d+(\-\w+)+",)), callback='parse_recipe')
    )

    # custom_settings = {
    #     "LOG_FILE": "cookpad.log",
    # }

    # scrapy crawl cookpad.com -o out.json -a category=vegan
    def __init__(self, category=None, *args, **kwargs):
        """ Initialize CookpadSpider object with all necessary options.

        Args:
            category (str): category of recipes to crawl.
            *args: other positional arguments
            **kwargs: other keyword arguments
        """
        super(CookpadSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.start_urls = [
            "https://cookpad.com/uk/search/{}".format(self.category)
        ]

    def parse_recipe(self, response):
        """ Parse recipe from given HTTP response.

        Args:
            response (scrapy.http.response.html.HtmlResponse): HTTP response

        Returns:
            recipe (CookpadRecipe): recipe data object
        """
        recipe = CookpadRecipe()

        recipe["category"] = self.category

        # link
        recipe["link"] = response.url

        # id
        recipe["id"] = int(findall(r'recipes/(\d+)', response.url)[0])

        # name
        recipe["name"] = response.selector.xpath("//title/text()").get().strip()

        # author
        recipe["author"] = response.selector.xpath("//span[@itemprop='name']/text()").get().strip()

        recipe["description"] = response.selector.xpath("//meta[@name='description']/@content").get()

        # ingredients
        ingredients = list()
        ingredient_basepath = "//li[@class='ingredient ']"
        ingredient_nodes = response.selector.xpath(ingredient_basepath)
        for ingredient_node in ingredient_nodes:
            ingredient_name = ingredient_node.xpath(".//div[@itemprop='ingredients']/text()").getall()
            quantity = ingredient_node.xpath(".//div[@itemprop='ingredients']/bdi[@class='ingredient__quantity']/text()").get()

            ingredient = Ingredient()
            try:
                ingredient["name"] = ingredient_name[1].strip().strip(",")
            except Exception as err:
                self.logger.warning("There might be problem with ingredient "
                                    "name! Error details: {}".format(err))
            ingredient["quantity"] = quantity
            ingredients.append(ingredient)
        recipe["ingredients"] = ingredients

        # servings & duration
        servings_duration = response.selector.xpath("//div[@class='subtle']/text()").getall()
        try:
            recipe["servings"] = servings_duration[0].strip()
        except Exception as err:
            self.logger.error("Cannot retrieve servings number! "
                              "Error details: {}".format(err))
            recipe["servings"] = None

        recipe["duration"] = servings_duration[1].strip()

        # steps/instructions
        steps = list()
        steps_basepath = "//div[@class='step__description']"
        steps_nodes = response.selector.xpath(steps_basepath)
        for step_node in steps_nodes:
            step = step_node.xpath(".//div[@itemprop='recipeInstructions']//p/text()").get()
            steps.append(step)

        recipe["instructions"] = steps

        yield recipe
