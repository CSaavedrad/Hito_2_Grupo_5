from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import os
import openai
import sys
import json
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
class WebScraper:
    def __init__(self):
        self.results = []

    def setup_driver(self):
        browser_options = ChromeOptions()
        browser_options.add_argument("--headless=new")
        self.driver = Chrome(options=browser_options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()

    def get_data(self, url):
        if not self.driver:
            self.setup_driver()

        self.driver.get(url)

        try:
            a_element = self.driver.find_element(By.XPATH, "//a[@id='alnkname' and @class='detlnkname']")
            name_url = a_element.get_attribute('href')
            names = name_url[48:-4].split("-")
            names = " ".join(n.capitalize() for n in names)
        except NoSuchElementException:
            try:
                nickname = self.driver.find_element(By.XPATH, "//span[@id='tutorname' and @class='fs15']")
                names = nickname.text
            except NoSuchElementException:
                return

        try:
            p_element = self.driver.find_element(By.XPATH, "//*[@id='pClasesde']")
            clase = p_element.find_element(By.TAG_NAME, 'b')
            clase_text = clase.text
        except NoSuchElementException:
            clase_text = "No disponible"

        try:
            en = self.driver.find_element(By.XPATH, "//p[@id='pProvincia' and @class='mgbottom0']")
            en_text = en.text
        except NoSuchElementException:
            en_text = "Locacion no disponible"

        try:
            div_element = self.driver.find_element(By.ID, 'dvPara')
            para = div_element.find_element(By.XPATH, ".//p[@class='bold']")
            para_text = para.text
        except NoSuchElementException:
            para_text = "No disponible"

        try:
            div_element = self.driver.find_element(By.ID, 'dvNiveles')
            niv = div_element.find_element(By.XPATH, ".//p[@class='bold']")
            niv_text = niv.text
        except NoSuchElementException:
            niv_text = "No disponible"

        try:
            div_element = self.driver.find_element(By.ID, 'dvMetodos')
            met = div_element.find_element(By.XPATH, ".//p[@class='bold']")
            met_text = met.text
        except NoSuchElementException:
            met_text = "No disponible"

        try:
            div_element = self.driver.find_element(By.ID, 'dvPrecio')
            precio = div_element.find_element(By.XPATH, ".//p[@class='bold']")
            precio_text = precio.text
        except NoSuchElementException:
            precio_text = "Precio no disponible"


        try:
            a_element = self.driver.find_element(By.XPATH, "//*[@id='detsubheader']/span/a")
            rating_count = int(a_element.find_element(By.CSS_SELECTOR, 'span[itemprop="ratingCount"]').text)
            star_y = a_element.find_elements(By.CSS_SELECTOR, '.spr-com.p_stars.star_y')
            star_m = a_element.find_elements(By.CSS_SELECTOR, '.spr-com.p_stars.star_m')
            rating = len(star_y) + len(star_m) / 2
            rtng = {"valor": rating, "resenas": rating_count}
        except NoSuchElementException:
            rtng = "rating no disponible"


        data_dict = {}

        data_dict["Nombre"] = strip_accents(names)
        data_dict["Clases de"] = strip_accents(clase_text)
        data_dict["Locacion"] = strip_accents(en_text)
        data_dict["Para"] = strip_accents(para_text)
        data_dict["Niveles"] = strip_accents(niv_text)
        data_dict["Metodos"] = strip_accents(met_text)
        data_dict["Precio"] = strip_accents(precio_text)
        data_dict["Rating"] = rtng
        data_dict["Contacto"] = strip_accents(url)

        self.results.append(data_dict)

    def append_results(self, a):
        self.results.append(a)

    def get_results(self):
    
        return self.results

class ChatGPT:
    def generate_response(self, description):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """Eres un sistema de búsqueda de profesores para talleres. En base a una descripción del taller
                    tienes que devolver la temática del taller y una ubicación para el taller.
                    La temática puede ser específica, no generalices tanto.
                    Si la temática es más de una palabra separa cada palabra con '%20'.
                    Si la ubicación es más de una palabra separa cada palabra con '%20'.
                    Retorna '0' si no encontraste la temática del taller y necesitas más información.
                    Retorna '1-temática' si encontraste solo la temática del taller.
                    Retorna '1-temática-ubicación' si encontraste la temática y una ubicación para el taller.
                    No retornes nada más de lo pedido.
                    Reemplaza 'á' 'é' 'í' 'ó' 'ú' 'ñ' por 'a' 'e' 'i' 'o' 'u' 'n' respectivamente."""},
                {"role": "user", "content": description}
            ]
        )

        return completion.choices[0].message.content


class Busqueda:
    def _init_(self):
        self.courses = []

    def scrape_courses(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table')
        column_data = table.find_all('tr')
        a = [tr.find('a') for tr in column_data[:-1]]

        if a == []:
            r = {"message": "tusclasesparticulares no ha encontrado profesores con esos criterios."}
            json_output = json.dumps(r, ensure_ascii=False)
            print(json_output)
            return

        href = []

        for b in a:
            if b is not None:
                href.append(b.get('href'))

        self.courses = ["https://www.tusclasesparticulares.cl/" + _ for _ in href]

    def get_courses(self):
        return self.courses

chat_gpt = ChatGPT()
Resultados_Busqueda = Busqueda()
web_scraper = WebScraper()

user_input = sys.argv[1]
prompt = user_input

response = chat_gpt.generate_response(prompt)

if response == '0':
    r = {"message": "ChatGPT no encontro la tematica del taller."}
    json_output = json.dumps(r, ensure_ascii=False)
    print(json_output)
    exit()

if response[0] == '1':
    split = response.split("-")
else:
    r = {"message": "ChatGPT no siguio el formato establecido."}
    json_output = json.dumps(r, ensure_ascii=False)
    print(json_output)
    exit()

split = response.split("-")
url = "https://www.tusclasesparticulares.cl/domicilio/?q=" + split[1]

if len(split) >= 3:
    i = 2
    while i < len(split):
        url += "%20" + split[i]
        i += 1

web_scraper.append_results(url)

Resultados_Busqueda.scrape_courses(url)
course_urls = Resultados_Busqueda.get_courses()

web_scraper.setup_driver()

for course_url in course_urls[0:10]:
    web_scraper.get_data(course_url)

results = web_scraper.get_results()
json_output = json.dumps(results, ensure_ascii=False)
print(json_output)

web_scraper.close_driver()
