# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()


        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()



        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)


        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])



        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)


        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5


        return item
    

import psycopg2

class SaveToPosgreSQLPipeline:
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        db_name = "scrapy"
        db_user = "postgres"
        db_password = "kothbiro"
        db_host = "localhost"
        db_port = "5432"

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS books_data (
        id SERIAL PRIMARY KEY,
        url VARCHAR(255),
        title TEXT,
        upc VARCHAR(12),
        product_type TEXT,
        price_excl_tax NUMERIC,
        price_incl_tax NUMERIC,
        tax NUMERIC,
        availability INTEGER,
        num_reviews INTEGER,
        stars INTEGER,
        category TEXT,
        description TEXT,
        price NUMERIC
        );
        '''

        try:
            self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
            self.cur = self.conn.cursor()
            self.cur.execute(create_table_sql)
            self.conn.commit()
            print("Table created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def process_item(self, item, spider):
        try:
            self.cur.execute(""" 
            INSERT INTO books_data (
                url, title, upc, product_type, price_excl_tax,
                price_incl_tax, tax, price, availability,
                num_reviews, stars, category, description
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """, (
                item["url"], item["title"], item["upc"], item["product_type"],
                item["price_excl_tax"], item["price_incl_tax"], item["tax"],
                item["price"], item["availability"], item["num_reviews"],
                item["stars"], item["category"], str(item["description"][0])
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting item: {e}")
        return item

    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

