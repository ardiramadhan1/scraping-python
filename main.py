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
driver = webdriver.Chrome(PATH)


@app.route('/bandung')
def bandung():
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
                    article.find_element(By.CSS_SELECTOR, 'a .articles--iridescent-list--text-item__category').text
            except Exception as e:
                category = None

            rows.append({
                'url': url,
                'image': image,
                'category': category
            })
        driver.quit()
    except Exception as e:
        return e
    return jsonify({
        'data': rows
    })


if __name__ == '__main__':
    app.run()
