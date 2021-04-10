from getDataBook import getDataBook
from toJson import to_json

def main():
    list_fields = ['LDR', '000', '001', '003', '005', '006', '007', '008', '009', '020', '031', '035', '036', '041',
                   '044', '050', '075', '076', '080', '082', '100', '110', '113', '116', '136', '138', '140', '152',
                   '154', '166', '168', '169', '175', '184', '189', '197', '204', '206', '216', '218', '223', '224',
                   '227', '229', '230', '232', '240', '244', '245', '250', '260', '269', '271', '273', '274', '276',
                   '281', '292', '294', '300', '304', '312', '318', '321', '336', '341', '344', '355', '356', '359',
                   '362', '366', '374', '382', '406', '408', '414', '428', '430', '448', '464', '483', '490', '500',
                   '504', '507', '511', '518', '546', '571', '587', '603', '608', '624', '650', '651', '658', '687',
                   '696', '700', '800', '802', '804', '807', '811', '852', '855', '857', '891', '911', '913']
    f = open("urlValid.txt", "r")
    id_uri = f.readlines()
    urlSursa = "http://opac.biblioteca.ase.ro/opac/bibliographic_view/"
    index = 1

    try:
        while True:
            mylist = []
            list = getDataBook(urlSursa + id_uri[index])
            a = list.split(' ')
            i = 1
            mylist.append(a[0])
            while i < (len(a)):

                value = ""
                while i < len(a):
                    if not a[i] in list_fields:
                        value += a[i]
                        i += 1
                    else:
                        break
                mylist.append(value)
                if (i < len(a)):
                    mylist.append(a[i])
                i += 1
            if not to_json(mylist,index):
                print("error")
            index += 1

    except KeyboardInterrupt:
        pass
    finally:
        pass
        # jsonFileTinread =open("../data/tinread.json", "a+")
        # jsonFileTinread.write(list)
        # jsonFileTinread.close()


if __name__ == '__main__':
    main()
