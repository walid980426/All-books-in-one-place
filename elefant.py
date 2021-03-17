from selenium import webdriver

driver = webdriver.Firefox()
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i = 1
while True:
    driver.get(urlSource+str(i))
    for line in driver.find_elements_by_xpath('//div[5]/div/div/div/a'):
        line.click()
        driver.implicitly_wait(3)
    i += 1
    if len(driver.find_elements_by_xpath("//div[2]/div[5]/div")) > 0:
        continue
    else:
        break
driver.close()

