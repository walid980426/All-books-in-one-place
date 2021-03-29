import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
"""
"""
dateTinread={
"LDR": " ",
"001": " ",
"003":" ",
"005":" ",
"006": " ",
"007": " ",
"008": " ",
"009": " ",
"020":{
    "$a":" ",
    "$c":" ",
    "$q":" ",
    "$z":" ",
    "$6":" ",
    "$8":" "
},
"041": " ",
"082": " ",
"100": " ",
"245": " ",
"260": " ",
"300": " ",
"490": " ",
"500": " ",
"502": " ",
"504": " ",
"650": " ",
"651": " ",
"700": " ",
"852": " ",
"891": " "
}
marc650={
    "$a"
}
def main():
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    data=""
    f =open("urlValid.txt", "r")
    id_uri= f.readlines()

    urlSursa="http://opac.biblioteca.ase.ro/opac/bibliographic_view/"
    index =1
    try:
        #while True:
        url =urlSursa+id_uri[index]
        driver.get(url)
        dateForOneId=driver.find_element_by_xpath("//li[contains(., 'LDR')]").get_attribute('innerHTML')
        print()
        i=0
        data =driver.find_element_by_xpath("//li[contains(., 'LDR')]").get_attribute('innerHTML')
        regularExpression = r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)'
        data =re.sub(regularExpression,' ',data)
        data= re.sub(r"[ +]+",' ',data)
        data= re.sub(r"\n",'',data)

        print(data)
    except KeyboardInterrupt:
        pass
    finally:
        driver.quit()
if __name__ == '__main__':
    main()