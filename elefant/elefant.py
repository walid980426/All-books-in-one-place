from selenium import webdriver
import json

driver = webdriver.Firefox()
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i = 1
data = {}
data['price'] = []
data['details'] = []
try:
    while True:
        driver.get(urlSource+str(i))
        driver.implicitly_wait(3)
        for line in driver.find_elements_by_xpath('//div[@class="product-image-container"]'):
            browser = webdriver.Firefox()
            elem = line.find_element_by_tag_name("a")
            # driver.execute_script("arguments[0].setAttribute('target','_blank')", line.find_element_by_tag_name("a"))
            link = elem.get_attribute("href")
            browser.get(link)
            browser.implicitly_wait(3)
            pret_actual = browser.find_element_by_css_selector(".pdp-table-th > .current-price")

            print(pret_actual)
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
