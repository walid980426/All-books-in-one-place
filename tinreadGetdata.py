from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import re
"""regularExpression = r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)'
s = open("test.txt", 'r').read()
print(s)
result =re.sub(regularExpression,' ',s)
print(result)
"""
dateTinread={
"LDR": "00616nam a2200169 i 450",
"001": "200013",
"006": "a ||00 0",
"007": "ta",
"008": "141111b 000 0 ||",
"041": "0 # $a  rum",
"082": "00 4 $a  331.120 94",
"100": "$6  191073 $a  Predonu, Andreea-Monica",
"245": "1 0 $a  Implicatii regionale ale viitorului pietei unice europene a fortei de munca $c  Predonu Andreea-Monica",
"260": "# # $a  Bucuresti $L  s10556 $b  ASE $c  2014",
"300": "# # $a  X, 289, [62] f. $b  fig., graf., tab. partial color $c  31 cm",
"500": "$a  Teza este si pe CD",
"502": "$a  Teza de doctorat sustinuta la Academia de Studii Economice din Bucuresti, RO. C.S.U.D. Scoala Doctorala - Economie I, 2014",
"504": "# # $a  f. 275-289",
"650": "$2  ASE $6  171753 $a  teze de doctorat",
"651": "$6  172488 $a  Europa",
"700": "0 $6  155958 $a  Iovitu, Mariana, cond. st. $u  Academia de Studii Economice din Bucuresti. Facultatea de Economie Teoretica si Aplicata, Departamentul de Economie si Politici Economice",
"852": "# # $j  137026"
}
def main():
    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    data=""
    f =open("sursa/urlValid.txt","r")
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
        for line in driver.find_element_by_xpath("//li[contains(., 'LDR')]").find_elements_by_xpath('//b'):
            print(line.get_attribute('innerHTML'))
    except KeyboardInterrupt:
        pass
    finally:
        jsonFileTinread =open("data/tinread.json","a+")
        jsonFileTinread.write(data)
        jsonFileTinread.close()
        driver.quit()
if __name__ == '__main__':
    main()
