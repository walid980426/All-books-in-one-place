from selenium import webdriver
from time import sleep
import json

driver = webdriver.Firefox()
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i = 1
data = {'price': [], 'details': [], 'img': [], 'title': []}
try:
    while True:
        driver.get(urlSource+str(i))
        driver.implicitly_wait(3)
        sleep(2)
        for line in driver.find_elements_by_xpath('//div[@class="product-list-item col-lg-3 col-md-4 col-sm-4 col-xs-6 grid-view lazy"]'):
            browser = webdriver.Firefox()
            elem = line.find_element_by_tag_name("a")
            link = elem.get_attribute("href")
            browser.get(link)
            browser.implicitly_wait(3)
            sleep(6)
            pret_actual = browser.find_element_by_css_selector(".pdp-table-th > .current-price")
            pret_actual = pret_actual.text
            data['price'].append(pret_actual)
            image_link = browser.find_element_by_css_selector('.product-thumb-set > .product-image')
            image_link = image_link.get_attribute('src')
            data['img'].append(image_link)
            detalii = browser.find_element_by_xpath('//*[@id]/div/dl')
            detalii = detalii.text
            data['details'].append(detalii)
            title = browser.find_element_by_xpath('//h1')
            data['title'].append(title.text.split(" - ", 1)[0])
            print(data)
            browser.quit()
        i += 1
        if len(driver.find_elements_by_xpath("//div[2]/div[5]/div")) > 0:
            continue
        else:
            break
except KeyboardInterrupt:
    pass
#
driver.close()
