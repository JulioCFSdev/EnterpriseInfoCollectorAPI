from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
import json

s = Service(r'C:\\edgedriver_win64\\msedgedriver.exe')
driver = webdriver.Edge(service=s)

# Abre a página inicial
driver.get('https://br.investing.com/')

# Encontra a barra de pesquisa, insere texto e submete o formulário
cookies_buttom = driver.find_element(By.CSS_SELECTOR, 'button.onetrust-close-btn-handler')
cookies_buttom.click()

driver.maximize_window()

def search_companies_from_url(driver, company_name):
    basic_search_url = "https://br.investing.com/search/?q="
    try:
        url = basic_search_url + company_name
        driver.get(url)
    except WebDriverException as e:
        print("Ocorreu um erro no WebDriver:", e)
        print("Search company page error from {} param".format(company_name))
        driver.quit()

def extract_and_save(driver, index, current_url) -> dict:
    try:
        news_texts = {}
        a_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="article-title-link"]')
        
        # Verifica se o índice está dentro dos limites
        if index >= len(a_elements):
            print(f"Índice {index} fora do intervalo")
            return []
        
        a_elements[index].click()

        title_element = driver.find_element(By.CSS_SELECTOR, "div.mx-0.mt-1 h1")
        news_texts["news_title"] = title_element.text
        print(news_texts["news_title"])
        
        # Encontra o div com a classe 'caas-body' e extrai todos os elementos <p>
        paragraphs = driver.find_elements(By.CSS_SELECTOR, '.article_WYSIWYG__O0uhw p')
        news_texts["text"] = [p.text for p in paragraphs if p.text.strip() != '']
        print(news_texts["text"])
        
        # Retorna para a página anterior
        driver.get(current_url)
        
        # Retorna os textos
        return news_texts
    except:
        driver.get(current_url)
        time.sleep(1)
        return {}

companies_list = ["Casas Bahia", "Petrobras", "Magazine Luisa", "Bemol", "Americanas"]

for company in companies_list:
    search_companies_from_url(driver, company)

    news_data = {}

    # Clica no botão específico na página de resultados
    search = driver.find_elements(By.CSS_SELECTOR, 'div.js-inner-all-results-quotes-wrapper.newResultsContainer.quatesTable a.js-inner-all-results-quote-item')
    if search != []:
        search[0].click()

        url = driver.current_url
        url_news = url + "-news"
        old_url_news = url_news
        driver.get(url_news)

        a_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="article-title-link"]')

        index_pags = 1
        news_index = 0
        while(index_pags < 10):
            for index in range(len(a_elements)):
                news_texts = extract_and_save(driver, index, url_news)
                news_index = news_index + 1
                news_data[f"news{news_index}"] = news_texts
            index_pags = index_pags + 1
            url_news = old_url_news + "/" + str(index_pags)
            driver.get(url_news)

        # Salvar o dicionário em um arquivo JSON
        json_file_path = 'noticias{}.json'.format(company)
        with open(json_file_path, 'w', encoding='utf-8') as jsonf:
            json.dump(news_data, jsonf, ensure_ascii=False, indent=4)

    # Fecha o navegador
driver.quit()


class Scrapper():
    def __init__(self):
        self.path_
