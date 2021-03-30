from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from base64 import b64encode
import time
import json


def to_json(lst: list):
    """
    functie pentru introducerea informatiilor in fisierul json
    :param lst: lista cu nume, pret, isbn, etc
    """
    new_object = {str(lst[0]): {"titlu": lst[0], "sursa": lst[1], "poza": lst[2]}}

    for i in lst[3:]:  # in cazul in care apar caractere cum ar fi tab, new line ele sunt elimintae
        for j in ["\t", "\n", "\u00a0"]:
            i.replace(j, i)

        if i.find(':') == -1:
            continue
        obj = {str(i[0: i.find(':')]): str(i[i.find(':') + 1: len(i)])}
        new_object[lst[0]].update(obj)

    with open("carti.json", 'r+', encoding="utf-8") as file:
        data = file.read().strip()
        json_file = json.loads(data or '{}')
        json_file.update(new_object)
        file.seek(0)
        json.dump(json_file, file)
        file.truncate()


def main():
    driver = webdriver.Firefox()

    driver.get("https://www.libris.ro/")
    time.sleep(5)

    if driver.find_elements_by_xpath("//span[contains(@id,'xClose')]"):
        # daca apare popup-ul cu abonari se incearca inchiderea lui
        driver.find_element_by_xpath("//span[contains(@id,'xClose')]").click()

    if driver.find_elements_by_xpath('//a[@class="back-to-site-link"]'):
        driver.get(driver.find_element_by_xpath('//a[@class="back-to-site-link"]').get_attribute("href"))

    if driver.find_elements_by_xpath('//button[@class ="btn btn-primary btn-sm acceptcookiesLibris"]'):
        time.sleep(3)
        driver.find_element_by_xpath('//button[@class ="btn btn-primary btn-sm acceptcookiesLibris"]').click()

    # numarul categoriilor
    x = driver.find_elements_by_xpath('//div[@class="tab-pane tab-pane-header tab-subcategorie"]')
    categorii = []

    for i in range(1, len(x) + 1):
        y = driver.find_elements_by_xpath(  # numarul de coloane din fiecare categorie
            '//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(i) + ']/div/div[@class="col-md-3"]')
        for j in range(1, len(y) + 1):
            z = driver.find_elements_by_xpath(  # numarul subcategoriilor
                '//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(
                    i) + ']/div/div[@class="col-md-3"][' + str(j) + ']/ul/li[@class="menuTitleSubCateg"]')

            for k in range(1, len(z) + 1):  # preluam link-ul fiecarei subcategorii si o inseram in lista categorii
                xpath_val = driver.find_element_by_xpath(
                    '//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(
                        i) + ']/div/div[@class="col-md-3"][' + str(j) + ']/ul/li[@class="menuTitleSubCateg"][' + str(
                        k) + ']/a')
                val = xpath_val.get_attribute("href")
                categorii.append(val)

    for i in range(0, len(categorii)):
        driver.get(categorii[i] + '?pgn=100')  # accesam fiecare subcategorie
        # '?pgn=100'  -  se vor afisa 100 de carti in pagina
        j = 1
        while len(driver.find_elements_by_xpath(
                '//div[@class="col-md-7 text-right paginatie-top"]/ul/li[last()]/a//i[@class="fa fa-angle-right"]')) == 1:
            # cat timp gasim in pagina curenta un link catre pagina urmatoare
            # preluam date despre carti

            driver.get(categorii[i] + '?pgn=100&pg=' + str(j))
            carti = []

            for k in range(len(driver.find_elements_by_xpath(
                    '//div[@class="container-produs-singur border-box-ct-sg border-box-categ"]/a[@class="linkNumeProd"]'))):
                # preluam linkul de la fiecare carte din pagina
                xpath = driver.find_element_by_xpath(
                    '//div[@class="container-produs-singur border-box-ct-sg border-box-categ"][' + str(
                        k + 1) + ']/a[@class="linkNumeProd"]')
                carti.append(xpath.get_attribute("href"))
            j += 1

            # deschidem un tab nou in care vom accesa linkul de la fiecare carte is vom prelua informatii in legatura
            # cu titlu, pret, etc
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

            for k in carti:
                driver.get(k)
                carte = []
                carte.append(  # adaugam in lista numele cartii
                    driver.find_element_by_xpath('//h1[@id="product_title rating"]').get_attribute('textContent'))
                carte.append(k)  # adaugam in lista linkul de la fiecare carte
                print(carte[0], '\n', carte[1], '\n')

                img = driver.find_element_by_xpath('//img[@class="imgProdus"]')  # se preia coperta fiecarei carti
                driver.execute_script("arguments[0].scrollIntoView();", img)
                img.screenshot("coperta.png")

                with open("coperta.png", "rb") as f:
                    b_img = f.read()
                b64_img = b64encode(b_img).decode('utf-8')
                carte.append(b64_img)

                for l in range(1, len(driver.find_elements_by_xpath('//div[@id="text_container"]/p')) + 1):
                    # adaugam in lista celelate informatii cum ar fi ISBN, descriere ator
                    informatie = driver.find_element_by_xpath(
                        '//div[@id="text_container"]/p[' + str(l) + ']').get_attribute('textContent')
                    carte.append(informatie)
                    print(informatie)

                to_json(carte)  # adaugam continutul listei in fisierul json
                print('\n')
            # dupa ce am preluat informatiile de la toate cartile inchidem tab-ul
            # si continuam cu urmatoarea pagina

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            for k in carti:
                print(carti)
    driver.close()


if __name__ == "__main__":
    main()
