from selenium import webdriver

geckodriver = r'geckodriver.exe'
driver = webdriver.Firefox(executable_path=geckodriver)
driver.get("https://www.elefant.ro/list/carti/carte")
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i = 515
while True:
    driver.get(urlSource+str(i))
    for line in driver.find_element_by_xpath("//div[contains(., 'product-image-container')]").find_elements_by_xpath('//a'):
        '''page = driver.find_element_by_xpath('//*[@id="family-page"]/div/div[1]/div[2]/div[5]/div')'''
        pass
    i += 1
    if len(driver.find_elements_by_xpath("//div[2]/div[5]/div")) > 0:
        continue
    else:
        break
driver.close()

