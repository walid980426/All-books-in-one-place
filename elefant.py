from selenium import webdriver

driver = webdriver.Firefox()
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i = 1
try:
    while True:
        driver.get(urlSource+str(i))
        driver.implicitly_wait(3)
        for line in driver.find_elements_by_xpath('//div[@class="product-image-container"]'):
            driver.execute_script("arguments[0].setAttribute('target','_blank')",line.find_element_by_tag_name("a"))
            #

        i += 1
        if len(driver.find_elements_by_xpath("//div[2]/div[5]/div")) > 0:
            continue
        else:
            break
except KeyboardInterrupt:
    pass
#
driver.close()

