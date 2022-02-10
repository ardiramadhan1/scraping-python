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


@app.route('/bandung')
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


@app.route('/content')
def bandung_content():
    url = "https://www.liputan6.com/regional/read/4883330/tamu-hotel-di-bandung-meninggal-terperosok-dari-lantai-3"
    driver = webdriver.Chrome(PATH)
    driver.get(url)
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


if __name__ == '__main__':
    app.run()
