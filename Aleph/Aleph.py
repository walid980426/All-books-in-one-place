from selenium import webdriver
from time import sleep
driver = webdriver.Firefox()

i=1
while True:
    driver.get("http://aleph.bcucluj.ro:8991/F/U37IYB6QYV145YC3L2RLHFD699HAK9UK768M46UDUA8H5QDBDC-36579?func=find-c-0")
    driver.find_element_by_xpath("//input[@name='ccl_term']").send_keys("SYS="+str(i))
    driver.find_element_by_xpath("//input[@type='image']").click()
    try:
        driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[4]/td[1]/img") #eroare

        sleep(5)
    except:
        sleep(2)
        driver.find_element_by_xpath("/html/body/table[4]/tbody/tr[2]/td[4]/a").click() #carte
        sleep(2)
        driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[5]/a").click() #etichete
        sleep(2)
        data = driver.find_element_by_xpath("//tbody[contains(., '001')]")#elemnte unimarc
        for line in data.find_elements_by_xpath('//td'):
            print(line.get_attribute('innerHTML'))

    finally:
        i=i+1



