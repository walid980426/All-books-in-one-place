from selenium import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options
from ToJson import to_json

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
urlSource = "https://www.elefant.ro/list/carti/carte?pag="
i, id = (open("index.txt", 'r').readline().split(" "))
i = int(i)
id = int(id)

def navigare(driver, i):
    while True:
        driver.get(urlSource + str(i))
        driver.implicitly_wait(3)
        sleep(6)
        lista = driver.find_elements_by_xpath(
            '//div[@class="product-list-item col-lg-3 col-md-4 col-sm-4 col-xs-6 grid-view lazy"]')
        for j in range(id, 60):
            line = lista[j]
            browser = webdriver.Firefox(options=options)
            elem = line.find_element_by_tag_name("a")
            link = elem.get_attribute("href")
            browser.get(link)
            browser.implicitly_wait(3)
            sleep(2)
            '''mai_mult = browser.find_element_by_xpath('//div[2]/a[2]/span')
            mai_mult.click()'''
            sleep(2)
            extragere(browser, i)
            browser.quit()
        i += 1
        if len(driver.find_elements_by_xpath("//div[2]/div[5]/div")) > 0:
            continue
        else:
            break
    driver.close()


def extragere(browser, i):
    global id
    list =[]
    pret_actual = browser.find_element_by_css_selector(".pdp-table-th > .current-price")
    pret_actual = pret_actual.text
    list.append('Pret')
    list.append(pret_actual)
    image_link = browser.find_element_by_css_selector('.product-thumb-set > .product-image')
    image_link = image_link.get_attribute('src')
    list.append('Imagine')
    list.append(image_link)
    detalii = browser.find_element_by_xpath('//*[@id]/div/dl')
    # detalii = browser.find_element_by_xpath('//dl[@class="ish-productAttributes"]')
    detalii = detalii.text
    detalii = detalii.split("\n")
    for j in range(0, len(detalii)):
        list.append(detalii[j])
    title = browser.find_element_by_xpath('//h1')
    title = title.text.split(" - ", 1)[0]
    list.append("Titlu")
    list.append(title)
    k = id + 1
    if not to_json(list, k):
        print("error")
    print(list)
    id = id + 1
    open("index.txt", 'w').write(str(i) + ' ' + str(id))



if __name__ == "__main__":
    try:
        navigare(driver, i)
    except KeyboardInterrupt:
        pass
#div class="cc-window cc-banner cc-type-info cc-theme-block cc-bottom cc-color-override-1827372716
