from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from ToJson import to_json
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
i=int(open('i.txt').readline())
id=1
while True:
    driver.get("http://aleph.bcucluj.ro:8991/F/U37IYB6QYV145YC3L2RLHFD699HAK9UK768M46UDUA8H5QDBDC-36579?func=find-c-0")
    driver.find_element_by_xpath("//input[@name='ccl_term']").send_keys("SYS="+str(i))
    driver.find_element_by_xpath("//input[@type='image']").click()
    try:
        driver.find_element_by_xpath("/html/body/table[1]/tbody/tr[4]/td[1]/img") #eroare

        sleep(5)
    except:
        list= []
        sleep(2)
        driver.find_element_by_xpath("/html/body/table[4]/tbody/tr[2]/td[4]/a").click() #carte
        sleep(2)
        driver.find_element_by_xpath("/html/body/table[3]/tbody/tr/td[5]/a").click() #etichete
        sleep(2)
        data = driver.find_element_by_xpath("//html//body//table[5]")#elemnte Etichete MARC
        for line in data.find_elements_by_xpath('//tbody//tr//td'):
            list.append(line.text)
        k=0
        for k in range (len(list)):
            if list[k]=="FMT":
                break
        list=list[k:]
        k=0
        for k in range (len(list)):
            if list[k]=="SYS":
                break
        list=list[:k+2]
        to_json(list,id)
        id=id+1
        open("i.txt","w").write(str(i))

    finally:
        i=i+1



