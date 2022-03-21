import re

from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
PATH = r"C:\Users\user\Downloads\chromedriver.exe"


@app.route('/detik/list')
def detik():
    query = 'Bandung'
    page = 1
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.detik.com/search/searchall?query={}&sortby=time&page={}".format(query, page))
    try:
        news = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'list-berita'))
        )
        articles = news.find_elements(By.TAG_NAME, 'article')
        rows = []
        for article in articles:
            url = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            image = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            title = article.find_element(By.CLASS_NAME, 'title').text
            try:
                category = article.find_element(By.CSS_SELECTOR, 'span .category').text
            except Exception as e:
                category = None
            try:
                date = article.find_element(By.CSS_SELECTOR, 'span .date').text
                date = date.partition(', ')[2]
            except Exception as e:
                date = None

            rows.append({
                "url": url,
                "image": image,
                "title": title,
                "category": category,
                "date": date,
            })
        driver.quit()
        return jsonify({
            'data': rows
        })
    except Exception as e:
        return e


@app.route('/detik/content')
def detik_content():
    url = "https://news.detik.com/berita-jawa-barat/d-5900237/jelang-kedatangan-jokowi-ke-bandung-1421-personel-gabungan-disiagakan"
    driver = webdriver.Chrome(PATH)
    driver.get("{}?single=1".format(url))
    try:
        wraper = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'detail'))
        )
        js = """
            var paralax=document.getElementById('parallax1');
            paralax.parentNode.removeChild(paralax);
            var linksisip=document.getElementsByClassName('linksisip');
            for (element of linksisip) {
              element.parentNode.removeChild(element);
            }
        """
        driver.execute_script(js)
        title = wraper.find_element(By.CLASS_NAME, 'detail__title').text
        author = wraper.find_element(By.CLASS_NAME, 'detail__author').text
        date = wraper.find_element(By.CLASS_NAME, 'detail__date').text
        content = wraper.find_element(By.CLASS_NAME, 'itp_bodycontent').get_attribute('innerHTML')
        content = re.sub(' +', ' ', content)
        driver.quit()
        return jsonify({
            'data': {
                "title": title,
                "author": author,
                "date": date,
                "content": content
            }
        })
    except Exception as e:
        return e


@app.route('/liputan6/list')
def bandung():
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.liputan6.com")
    search = driver.find_element(By.NAME, "q")
    search.send_keys("Bandung")
    search.send_keys(Keys.RETURN)
    try:
        news = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'articles--iridescent-list'))
        )
        articles = news.find_elements(By.TAG_NAME, 'article')
        rows = []
        for article in articles:
            url = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            image = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            try:
                category = \
                    article.find_element(By.CLASS_NAME, 'articles--iridescent-list--text-item__category').text
            except Exception as e:
                category = None
            try:
                waktu = \
                    article.find_element(By.CLASS_NAME, 'articles--iridescent-list--text-item__datetime').text
            except Exception as e:
                waktu = None
            try:
                title = \
                    article.find_element(By.CLASS_NAME, 'articles--iridescent-list--text-item__title-link-text').text
            except Exception as e:
                title = None

            rows.append({
                'url': url,
                'title': title,
                'image': image,
                'category': category,
                'time': waktu
            })
        driver.quit()
        return jsonify({
            'data': rows
        })
    except Exception as e:
        return e


@app.route('/liputan6/content')
def bandung_content():
    url = "https://www.liputan6.com/regional/read/4883330/tamu-hotel-di-bandung-meninggal-terperosok-dari-lantai-3"
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    driver.execute_script("window.scrollBy(0,3000)","")
    time.sleep(3)
    try:
        konten = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'read-page-upper'))
        )
        title = konten.find_element(By.CLASS_NAME, 'read-page--header--title').text
        author = konten.find_element(By.CLASS_NAME, 'read-page--header--author__name').text
        content = konten.find_element(By.CLASS_NAME, 'article-content-body__item-content').text
        date = konten.find_element(By.CLASS_NAME, 'read-page--header--author__datetime').text
        driver.quit()
        return jsonify({
            'data': {
                "title": title,
                "author": author,
                "content": content,
                "date": date
            }
        })
    except Exception as e:
        return e


@app.route('/cnn/list')
def cnn_scrape():
    query = 'Bandung'
    page = 1
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.cnnindonesia.com/search/?query={}&page={}".format(query, page))
    try:
        news = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'l_content'))
        )
        articles = news.find_elements(By.TAG_NAME, 'article')
        rows = []
        for article in articles:
            url = article.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            image = article.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            title = article.find_element(By.CLASS_NAME, 'title').text
            try:
                category = article.find_element(By.CSS_SELECTOR, 'span .kanal').text
            except Exception as e:
                category = None
            try:
                date = article.find_element(By.CSS_SELECTOR, 'span .date').text
            except Exception as e:
                date = None

            rows.append({
                "url": url,
                "image": image,
                "title": title,
                "category": category,
                "date": date
            })
        driver.quit()
        return jsonify({
            'data': rows
        })
    except Exception as e:
        return e


@app.route('/cnn/content')
def cnn_content():
    url = \
        "https://www.cnnindonesia.com/gaya-hidup/20220314125331-277-770863/viral-kisah-nafa-salvana-dari-warung-pecel-lele-ke-milan-fashion-week"
    driver = webdriver.Chrome(PATH)
    driver.get(format(url))
    try:
        konten = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'l_content'))
        )
        image = konten.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
        title = konten.find_element(By.CLASS_NAME, 'title').text
        author = konten.find_element(By.CLASS_NAME, 'author').text
        content = konten.find_element(By.ID, 'detikdetailtext').text
        date = konten.find_element(By.CLASS_NAME, 'date').text
        driver.quit()
        return jsonify({
            'data': {
                "title": title,
                "author": author,
                "content": content,
                "date": date,
                "image": image
            }
        })
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run()
