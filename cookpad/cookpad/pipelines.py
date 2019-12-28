from sqlalchemy.orm import sessionmaker
from cookpad.models import RecipesRaw, db_connect, create_recipes_raw_table
import json


class PostgresqlPipeline(object):
    """PostgresqlPipeline pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates recipes_raw table.
        """
        engine = db_connect()
        create_recipes_raw_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save recipes in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()

        for section_key, json_list in item.items():
            if section_key == "ingredients":
                item["ingredients"] = [json.dumps(dict(value)) for value in json_list]

        raw_recipe = RecipesRaw(**item)

        try:
            session.add(raw_recipe)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

        return item