import os
import asyncpg
from datetime import datetime
import locale
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
PG_DB_HOST = os.environ.get('PG_DB_HOST')
PG_DB_NAME = os.environ.get('PG_DB_NAME')
PG_DB_USER = os.environ.get('PG_DB_USER')
PG_DB_PASS = os.environ.get('PG_DB_PASS')


async def add_image(category, image_file, image_name, image_alt):
    create_query = """
    CREATE TABLE IF NOT EXISTS category_images (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255), 
    image_file BYTEA, 
    image_name VARCHAR(255), 
    image_alt TEXT
    );
    """
    insert_query = """
    INSERT INTO category_images (category, image_file, image_name, image_alt) 
    VALUES ($1, $2, $3, $4);
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        await connection.execute(create_query)
        await connection.execute(insert_query, category, image_file, image_name, image_alt)
    except Exception as e:
        print(f'[ERROR] - add_image/Exception - {e}')


async def add_psypholog(psy_name, psy_skill, psy_description, work_request, psy_tel='', psy_vk='', psy_tlg=''):
    create_query = """
    CREATE TABLE IF NOT EXISTS psy_team (
    id SERIAL PRIMARY KEY,
    psy_name VARCHAR(100), 
    psy_skill VARCHAR(150), 
    psy_description TEXT, 
    work_request TEXT,
    psy_tel VARCHAR(20), 
    psy_vk VARCHAR(100), 
    psy_tlg VARCHAR(100)
    );
    """
    insert_query = """
    INSERT INTO psy_team (psy_name, psy_skill, psy_description, work_request, psy_tel, psy_vk, psy_tlg) 
    VALUES ($1, $2, $3, $4, $5, $6, $7);
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        await connection.execute(create_query)
        await connection.execute(insert_query, psy_name, psy_skill, psy_description, work_request, psy_tel, psy_vk, psy_tlg)
    except Exception as e:
        print(f'[ERROR] - add_psypholog/Exception - {e}')


async def add_request(category, user_name, user_contact, user_request):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    create_query = """
    CREATE TABLE IF NOT EXISTS site_orders (
    id SERIAL PRIMARY KEY,
    category VARCHAR(30), 
    user_name VARCHAR(100), 
    user_contact VARCHAR(255), 
    user_request TEXT,
    request_date TIMESTAMP
    );
    """
    insert_query = """
    INSERT INTO site_orders (category, user_name, user_contact, user_request, request_date) 
    VALUES ($1, $2, $3, $4, $5);
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        await connection.execute(create_query)
        await connection.execute(insert_query, category, user_name, user_contact, user_request, datetime.now())
    except Exception as e:
        print(f'[ERROR] - add_request/Exception - {e}')


async def add_text(category, title, price, old_price, description):
    create_query = """
    CREATE TABLE IF NOT EXISTS category_texts (
    id SERIAL PRIMARY KEY,
    category VARCHAR(100), 
    service_title VARCHAR(255), 
    service_price VARCHAR(10), 
    service_old_price VARCHAR(10),
    service_description TEXT
    );
    """
    insert_query = """
    INSERT INTO category_texts (category, service_title, service_price, service_old_price, service_description) 
    VALUES ($1, $2, $3, $4, $5);
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        await connection.execute(create_query)
        await connection.execute(insert_query, category, title, price, old_price, description)
    except Exception as e:
        print(f'[ERROR] - add_text/Exception - {e}')


async def get_images(category_name, with_bin=False):
    if with_bin:
        sql_req = f"""
        SELECT image_file, image_name, image_alt
        FROM category_images
        WHERE category='{category_name}';
        """
    else:
        sql_req = f"""
        SELECT image_name, image_alt
        FROM category_images
        WHERE category='{category_name}';
        """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        res = await connection.fetch(sql_req)
        await connection.close()
        return res
    except Exception as e:
        print(f'[ERROR] - get_images/Exception - {e}')
        return ['landing.jpg', ]


async def get_psypholog():
    sql_req = f"""
    SELECT psy_name, psy_skill, psy_description, work_request, psy_tel, psy_vk, psy_tlg
    FROM psy_team;
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        res = await connection.fetch(sql_req)
        await connection.close()
        return res
    except Exception as e:
        print(f'[ERROR] - get_psypholog/Exception - {e}')
        return [{
            'psy_name': 'Unknown name',
            'psy_skill': 'None-psy_skill',
            'psy_description': 'None-psy_description',
            'work_request': 'None-work_request',
            'psy_tel': 'tel',
            'psy_vk': 'vk',
            'psy_tlg': 'tlg'
        }, ]


async def get_requests(category='all'):
    if category == 'all':
        sql_req = """
        SELECT category, user_name, user_contact, user_request, request_date FROM site_orders;
        """
    else:
        sql_req = f"""
        SELECT category, user_name, user_contact, user_request, request_date FROM site_orders
        WHERE category='{category}';
        """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        res = await connection.fetch(sql_req)
        await connection.close()
        return res
    except Exception as e:
        print(f'[ERROR] - get_requests/Exception - {e}')
        return ['no data']


async def get_texts(category_name):
    sql_req = f"""
    SELECT service_title, service_price, service_old_price, service_description
    FROM category_texts
    WHERE category='{category_name}';
    """

    try:
        connection = await asyncpg.connect(
            host=PG_DB_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=30)
        res = await connection.fetch(sql_req)
        await connection.close()
        return res[0]
    except Exception as e:
        print(f'[ERROR] - get_texts/Exception - {e}')
        return ['unknown service', '0', '0', 'service description']
