from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os


def to_json(lst: list):
    """
    functie pentru introducerea informatiilor in fisierul json
    :param lst: lista cu nume, pret, isbn, etc
    """

    for i in range(3, len(lst)):  # in cazul in care apar caractere cum ar fi tab, new line ele sunt elimintae
        for j in ["\t", "\n", "\u00a0"]:
            lst[i] = lst[i].replace(j, '')

    new_object = {str(lst[0]): {"Titlu": lst[0], "Sursa": lst[1], "Poza": lst[2], "Pret: ": lst[3], "Pret redus: ": lst[4],
                                "Stoc: ": lst[5], "Cod: ": "-", "An aparitie: ": "-", "Autor: ": "-",  "Categorie: ": "-",
                                "Editura: ": "-", "Format: ": "-", "Nr. pagini: ": "-", "Alte detalii: ": "-"}}

    for i in range(6, len(lst)):
        # verificam daca lsta contine informatii cum ar fi cod carte, autor , etc regasite in dictionar
        # daca da atuci actualizam dictionarul creat.
        # daca apare o specificatie mai speciala care nu se regaseste in cheia dictionarului
        # informatia este adaugata in "Alte detalii: "
        if lst[6].startswith('Cod'):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Cod: "] = x[x.find(':') + 2:]
        elif lst[6].startswith('An aparitie: '):
            x = (lst.pop(6))
            new_object[str(lst[0])]['An aparitie: '] = x[x.find(':') + 2:]
        elif lst[6].startswith('Autor: '):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Autor: "] = x[x.find(':') + 2:] if new_object[str(lst[0])]["Autor: "] == '-' \
                                                                     else new_object[str(lst[0])]["Autor: "] + x[x.find(':') + 2]
        elif lst[6].startswith('Categorie: '):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Categorie: "] = x[x.find(':') + 2:] if new_object[str(lst[0])]["Categorie: "] == '-' \
                                                                        else new_object[str(lst[0])]["Categorie: "] + x[x.find(':') + 2]
        elif lst[6].startswith('Editura: '):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Editura: "] = x[x.find(':') + 2:]
        elif lst[6].startswith("Format: "):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Format: "] = x[x.find(':') + 2:]
        elif lst[6].startswith("Nr. pagini: "):
            x = (lst.pop(6))
            new_object[str(lst[0])]["Nr. pagini: "] = x[x.find(':') + 2:]
        else:
            new_object[str(lst[0])]["Alte detalii: "] = (lst.pop(6))

    with open("../data/libris.json", 'r+', encoding="utf-8") as file:
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

                if not os.path.isfile("../data/libris coperta/" + str(carte[0]) + ".png"):

                    img = driver.find_element_by_xpath('//img[@class="imgProdus"]')  # se preia coperta fiecarei carti
                    driver.execute_script("arguments[0].scrollIntoView();", img)
                    img.screenshot("../data/libris coperta/" + str(carte[0]) + ".png")
                carte.append("./data/libris coperta/" + str(carte[0]) + ".png")

                pret = driver.find_element_by_xpath('//div[@id="text_container"]/p[1]').get_attribute('textContent')
                if pret.count('Lei') == 1:
                    carte.append('Pret: ' + pret)
                    carte.append('Pret redus: -')
                else:
                    carte.append("Pret: " + pret[:pret.find("Lei", 2) + 3])
                    carte.append("Pret redus: " + pret[pret.find("Lei", 2) + 3:])

                carte.append('Stoc: ' + driver.find_element_by_xpath('//div[@id="text_container"]/p[3]').get_attribute(
                    'textContent'))
                for l in range(4, len(driver.find_elements_by_xpath('//div[@id="text_container"]/p')) + 1):
                    # adaugam in lista celelate informatii cum ar fi ISBN, descriere ator
                    informatie = driver.find_element_by_xpath(
                        '//div[@id="text_container"]/p[' + str(l) + ']').get_attribute('textContent')
                    carte.append(informatie)

                to_json(carte)  # adaugam continutul listei in fisierul json
            # dupa ce am preluat informatiile de la toate cartile inchidem tab-ul
            # si continuam cu urmatoarea pagina

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    driver.close()


if __name__ == "__main__":
    main()
