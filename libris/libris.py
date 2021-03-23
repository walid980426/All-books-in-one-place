from selenium import webdriver


driver = webdriver.Firefox()
urlSource = "https://www.libris.ro/carti?pg="
i = 1
while True:
    driver.get(urlSource+str(i))
    url = '//div[@class="container-produs-singur border-box-ct-sg border-box-categ"][' + str(i) + ']/a[3]/h2'
    i += 1
    lista = []

    for j in range(1,40):
        driver.implicitly_wait(3)
        url2 = '//div[@class="container-produs-singur border-box-ct-sg border-box-categ"]['+ str(j) +']/a[3]'
        j.click()
        lista.append(url2.get_attribute("href"))
    for j in lista:
        driver.get(j)
driver.close()