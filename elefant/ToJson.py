import json
import copy


def to_json(data: list, id: int) -> bool:
    dict = {id: []}
    fild ={
        "fld": {
            "fld_name": "fld_name",
            "val": ""
        }
    }
    index = 0
    try:
        for i in range(0, len(data), 2):

            dict[id].append(copy.deepcopy(fild))
            dict[id][index]["fld"]["fld_name"] = data[i]
            dict[id][i//2]["fld"]["val"] = data[i+1]
            index += 1
        with open("../data/elefant.json") as file:
            data = list(json.load(file))
            data.append(dict)

        with open("../data/elefant.json", 'w') as file:
            json.dump(data, file)
        return True
    except:
        print("error")
        return False

