from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

def to_json(lst):
    # specificatiile se introduc in fisierul carti.json
    new_object = {str(lst[0]): lst}
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
    # 
    driver.find_element_by_xpath("//span[contains(@id,'xClose')]").click()

    if driver.find_elements_by_xpath('//a[@class="back-to-site-link"]'):
        driver.get(driver.find_element_by_xpath('//a[@class="back-to-site-link"]').get_attribute("href"))

    x = driver.find_elements_by_xpath('//div[@class="tab-pane tab-pane-header tab-subcategorie"]')
    categorii = []

    for i in range(1, len(x) + 1):
        y = driver.find_elements_by_xpath(
            '//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(i) + ']/div/div[@class="col-md-3"]')
        for j in range(1, len(y) + 1):
            z = driver.find_elements_by_xpath('//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(
                i) + ']/div/div[@class="col-md-3"][' + str(j) + ']/ul/li[@class="menuTitleSubCateg"]')
            for k in range(1, len(z) + 1):
                xpath_val = driver.find_element_by_xpath(
                    '//div[@class="tab-pane tab-pane-header tab-subcategorie"][' + str(
                        i) + ']/div/div[@class="col-md-3"][' + str(j) + ']/ul/li[@class="menuTitleSubCateg"][' + str(
                        k) + ']/a')
                val = xpath_val.get_attribute("href")
                categorii.append(val)
    for i in range(0, len(categorii)):  # !!!!!!
        driver.get(categorii[i] + '?pgn=100')
        j = 1
        while len(driver.find_elements_by_xpath('//div[@class="col-md-7 text-right paginatie-top"]/ul/li[last()]/a//i[@class="fa fa-angle-right"]')) == 1:
            driver.get(categorii[i] + '?pgn=100&pg=' + str(j))
            carti = []
            for k in range(len(driver.find_elements_by_xpath('//div[@class="container-produs-singur border-box-ct-sg border-box-categ"]/a[@class="linkNumeProd"]'))):
                xpath = driver.find_element_by_xpath('//div[@class="container-produs-singur border-box-ct-sg border-box-categ"]['+str(k+1)+']/a[@class="linkNumeProd"]')
                carti.append(xpath.get_attribute("href"))
            j += 1
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            for k in carti:
                driver.get(k)
                carte = []
                carte.append(driver.find_element_by_xpath('//h1[@id="product_title rating"]').get_attribute('textContent'))
                print(carte[0], '\n')
                for l in range(1, len(driver.find_elements_by_xpath('//div[@id="text_container"]/p'))+1):
                    informatie = driver.find_element_by_xpath('//div[@id="text_container"]/p['+str(l)+']').get_attribute('textContent')
                    carte.append(informatie)
                    print(informatie)
                to_json(carte)
                print('\n')
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            for k in carti:
                print(carti)
    driver.close()


if __name__ == "__main__":
    main()
