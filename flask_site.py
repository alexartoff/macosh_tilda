from flask import Flask, render_template
from flask import request, flash, redirect, url_for
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename


import db
from prepare_data import decode_images, allowed_file


load_dotenv(find_dotenv())
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SERVER_NAME'] = os.environ.get('SERVER_NAME')
SITE_URL = 'https://ma-cosh.ru'
SITE_TITLE = 'МаКошь'
PHONE = '+7 (951) 456-21-19'
FORM_ID = '#rec624966349'


@app.route('/')
async def main():
    context = {
        'title': SITE_TITLE,
        'h1_tag': SITE_TITLE,
        'h1_descr': '''
            Здесь всё для тебя ❤ чтобы тебе помочь
            <br>
            <br>Браслеты по дате рождения, аксессуары
            <br>Расчёты по дате рождения, таро, МАК
            <br>Психологическое консультирование
        ''',
        'meta_description': '''
            Здесь всё для тебя ❤ чтобы тебе помочь
            Браслеты по дате рождения, аксессуары
            Расчёты по дате рождения, таро, МАК
            Психологическое консультирование
        ''',
        'meta_keywords': '''
            МаКошь, Браслеты, Браслеты по дате рождения, аксессуары, куклы-обереги, 
            Расчёты по дате рождения, таро, МАК, Психологическое консультирование
        ''',
        'meta_url': SITE_URL,
        'phone': PHONE,
    }
    return render_template('index.html', context=context)


@app.route('/decor', methods=('GET', 'POST'))
async def decor():
    date = datetime.now()
    images = {
        'braslet_img': await decode_images('braslet_card', decode=False),
        'svechi_img': await decode_images('svechi_card', decode=False),
        'kukli_img': await decode_images('kukli_card', decode=False),
        'slider': await decode_images('slider', decode=False),
    }
    context = {
        'title': SITE_TITLE + ' - Браслеты - Свечи - Куклы',
        'decor_descr': '''
            Мы создаем <strong>браслеты и аксессуары ручной работы</strong>.
            <br>Все предметы сделаны с любовью и вдохновением 
            <strong>из качественных натуральных материалов</strong>.
            <br>Выберите цвет, размер и стиль и носите их с удовольствием.
        ''',
        'meta_description': '''
            Мы создаем браслеты и аксессуары ручной работы.
            Все предметы сделаны с любовью и вдохновением 
            из качественных натуральных материалов.
            Выберите цвет, размер и стиль и носите их с удовольствием.
        ''',
        'meta_keywords': 'МаКошь, Браслеты, Браслеты по дате рождения, аксессуары, куклы-обереги',
        'meta_url': SITE_URL,
        'phone': PHONE,
        'braslet_text': await db.get_texts('braslet_card'),
        'svechi_text': await db.get_texts('svechi_card'),
        'kukli_text': await db.get_texts('kukli_card'),
    }
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_request = request.form['user_request']
        user_contact = request.form['user_contact']

        if not user_name or not user_request or not user_contact:
            flash('Пожалуйста, заполните все поля формы', category='danger')
            return redirect(url_for('decor')+"#rec624966349")
        else:
            await db.add_request('decor', user_name, user_contact, user_request)
            flash(f'<strong>{user_name}!</strong></br>Ваш запрос успешно отправлен', category='success')
            return redirect(url_for('decor'))

    if request.method == 'GET':
        return render_template(
            'decor.html',
            date=date,
            images=images,
            context=context
        )


@app.route('/neopsy', methods=('GET', 'POST'))
async def neopsy():
    date = datetime.now()
    images = {
        'neopsy_img': await decode_images('neopsy_card', decode=False),
    }
    context = {
        'title': SITE_TITLE + ' - Нетрадиционная психология',
        'meta_description': '''
            Помощь в сложных ситуациях. Разбор вашей личности, поиск ответов на тревожащие вопросы. 
            Здесь нет хороших и плохих. Нет нудных советов и копания в душе. 
            Полтора часа работы в лайтовом режиме
        ''',
        'meta_keywords': 'МаКошь, Расчёты по дате рождения, таро, МАК, Разбор личности',
        'meta_url': SITE_URL,
        'phone': PHONE,
        'neopsy_text': await db.get_texts('neopsy_card'),
    }
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_request = request.form['user_request']
        user_contact = request.form['user_contact']

        if not user_name or not user_request or not user_contact:
            flash('Пожалуйста, заполните все поля формы', category='danger')
            return redirect(url_for('neopsy')+"#rec624966349")
        else:
            await db.add_request('neopsy', user_name, user_contact, user_request)
            flash(f'<strong>{user_name}!</strong></br>Ваш запрос успешно отправлен', category='success')
            return redirect(url_for('neopsy'))

    if request.method == 'GET':
        return render_template(
            'neopsy.html',
            date=date,
            images=images,
            context=context
        )


@app.route('/psy', methods=('GET', 'POST'))
async def psy():
    date = datetime.now()
    images = {
        'psy_img': await decode_images('psy_card', decode=False),
    }
    team_images = {
        'team': await decode_images('psy_spec', decode=False),
    }
    context = {
        'title': SITE_TITLE + ' - Психологическое консультирование',
        'meta_description': '''
            Работа с профессиональным и опытным психологом.
            Решение вопросов, мешающих жить. Вместе проще решать проблемы
        ''',
        'meta_keywords': 'МаКошь, Психологическое консультирование, Решение вопросов',
        'meta_url': SITE_URL,
        'phone': PHONE,
        'psy': await db.get_texts('psy_card'),
        'psy_team': await db.get_psypholog(),
    }
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_request = request.form['user_request']
        user_contact = request.form['user_contact']

        if not user_name or not user_request or not user_contact:
            flash('Пожалуйста, заполните все поля формы', category='danger')
            return redirect(url_for('psy')+"#rec624966349")
        else:
            await db.add_request('psy', user_name, user_contact, user_request)
            flash(f'<strong>{user_name}!</strong></br>Ваш запрос успешно отправлен', category='success')
            return redirect(url_for('psy'))

    if request.method == 'GET':
        return render_template(
            'psy.html',
            date=date,
            images=images,
            team_images=team_images,
            context=context
        )


@app.route('/upload_img', methods=('GET', 'POST'))
async def upload_img():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        img_alt_text = request.form['img_alt'] or ''
        category = request.form['category'] or 'other'
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            img_filename = secure_filename(file.filename)
            img_file_bin = file.stream.read()
            await db.add_image(category, img_file_bin, img_filename, img_alt_text)
            return redirect(url_for('upload_img'))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name="file" style="width:300px;">
          <br/><br/>
          <label for="cat">image category:</label><br/>
          <input type=text name="category" id="cat" style="width:300px;">
          <br/><br/>
          <label for="alt">image alt text:</label><br/>
          <input type=text name="img_alt" id="alt" style="width:300px;">
          <br/>
          <input type=submit value=Upload>
        </form>
        '''


@app.route('/upload_text', methods=('GET', 'POST'))
async def upload_text():
    if request.method == 'POST':
        category = request.form['category'] or 'other'
        service_title = request.form['service_title'] or ''
        service_price = request.form['service_price'] or '0'
        service_old_price = request.form['service_old_price'] or '0'
        service_description = request.form['service_description'] or ''
        await db.add_text(category, service_title, service_price, service_old_price, service_description)
        return redirect(url_for('upload_text'))
    return '''
        <!doctype html>
        <title>Upload new service</title>
        <h1>Upload new service</h1>
        <form method=post enctype=multipart/form-data>
          <label for="category">category:</label><br/>
          <input type=text name="category" id="category" style="width:300px;">
          <br/><br/>
          <label for="service_title">service_title:</label><br/>
          <input type=text name="service_title" id="service_title" style="width:300px;">
          <br/><br/>
          <label for="service_price">service price:</label><br/>
          <input type=text name="service_price" id="service_price" style="width:300px;">
          <br/><br/>
          <label for="service_old_price">service old price:</label><br/>
          <input type=text name="service_old_price" id="service_old_price" style="width:300px;">
          <br/><br/>
          <label for="service_description">service description:</label><br/>
          <textarea type=text name="service_description" id="service_description" rows="5" style="width:300px;"></textarea>
          <br/>
          <input type=submit value=Upload>
        </form>
        '''


# @app.route('/check', methods=('GET', 'POST'))
# async def check():
#     if request.method == 'GET':
#         data = await db.get_images('braslet_card')
#         context = []  # category, image_file, image_name, image_alt
#         for item in data:
#             _ = {
#                 # 'category': item[0],
#                 'image_file': b64encode(bytes(item[0])).decode(),
#                 'image_name': item[1],
#                 'image_alt': item[2]
#             }
#             context.append(_)
#         return render_template('check.html', context=context)


@app.route('/macosh-orders-page', methods=('GET', 'POST'))
async def get_orders():
    if request.method == 'GET':
        context = {
            'title': SITE_TITLE,
            'h1_tag': SITE_TITLE,
            'h1_descr': '''
                    Здесь всё для тебя ❤ чтобы тебе помочь
                    <br>
                    <br>Браслеты по дате рождения, аксессуары
                    <br>Расчёты по дате рождения, таро, МАК
                    <br>Психологическое консультирование
                ''',
            'meta_description': '''
                    Здесь всё для тебя ❤ чтобы тебе помочь
                    Браслеты по дате рождения, аксессуары
                    Расчёты по дате рождения, таро, МАК
                    Психологическое консультирование
                ''',
            'meta_keywords': '''
                    МаКошь, Браслеты, Браслеты по дате рождения, аксессуары, куклы-обереги, 
                    Расчёты по дате рождения, таро, МАК, Психологическое консультирование
                ''',
            'meta_url': SITE_URL,
            'phone': PHONE,
        }
        orders = await db.get_requests()
        return render_template('orders.html', context=context, orders=orders)


@app.errorhandler(404)
def page_not_found(e):
    # print(f'404 - {e}')
    context = {
        'title': SITE_TITLE,
        'h1_tag': SITE_TITLE,
        'h1_descr': '''
            Здесь всё для тебя ❤ чтобы тебе помочь
            <br>
            <br>Браслеты по дате рождения, аксессуары
            <br>Расчёты по дате рождения, таро, МАК
            <br>Психологическое консультирование
        ''',
        'meta_description': '''
            Здесь всё для тебя ❤ чтобы тебе помочь
            Браслеты по дате рождения, аксессуары
            Расчёты по дате рождения, таро, МАК
            Психологическое консультирование
        ''',
        'meta_keywords': '''
            МаКошь, Браслеты, Браслеты по дате рождения, аксессуары, куклы-обереги, 
            Расчёты по дате рождения, таро, МАК, Психологическое консультирование
        ''',
        'meta_url': SITE_URL,
        'phone': PHONE,
    }
    return render_template('404.html', context=context), 404
