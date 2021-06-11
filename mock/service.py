import constants
import json
import os


def write_to_file(response):
    with open(constants.FILE_NAME, 'w') as json_file:
        json_file.seek(0)
        json.dump(response, json_file, indent=4)


def post_entity(req, entity):
    if os.stat(constants.FILE_NAME).st_size == 0:
        response = {}
    else:
        response = get_contents_of_file()
    if entity in response:
        a = response[entity]
        length = len(a)
        id = a[length - 1]["id"] + 1
    else:
        id = 1
    req["id"] = id
    if entity in response:
        response[entity].append(req)
    else:
        response[entity] = [req]
    write_to_file(response)


def get_entity(z, entity, _sort, _order, q):
    response = get_contents_of_file()
    if response == {}:
        return response
    else:
        if entity in response:
            response = response[entity]
        else:
            return []
    for i, j in z.items():
        response = list(filter(lambda x: x[i] == j, response))
    if _sort:
        if _order is None or _order == "asc":
            response = sorted(response, key=lambda x: x[_sort])
        elif _order == "dsc":
            response = sorted(response, key=lambda x: x[_sort], reverse=True)
        # else:
        #     print("as")
    return response


def get_contents_of_file():
    f = open(constants.FILE_NAME, )
    data = json.load(f)
    return data
