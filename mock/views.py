from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from mock import service
import constants
import json
import os

with open(constants.FILE_NAME, 'w') as file:
    pass


@csrf_exempt
def index(request):
    return HttpResponse("Welcome to the mock server")


@csrf_exempt
def entity(request, entity):
    if request.method == "GET":
        a = request.GET
        x = {}
        for i in a:
            b = a.getlist(i)[0]
            x[i] = b
        _sort = request.GET.get('_sort')
        _order = request.GET.get('_order')
        q = request.GET.get('q')
        if os.stat(constants.FILE_NAME).st_size == 0:
            response = []
        else:
            response = service.get_entity(x, entity, _sort, _order, q)
        return JsonResponse(response, safe=False)
    elif request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))
        service.post_entity(req, entity)
        return redirect("/" + entity)
    else:
        return HttpResponse("This is not a valid request")


@csrf_exempt
def entity_by_id(request, entity, id):
    if request.method == "GET":
        if os.stat(constants.FILE_NAME).st_size == 0:
            return JsonResponse([], safe=False)
        else:
            data = service.get_contents_of_file()
            if entity in data:
                response = data[entity]
                for i in response:
                    if i["id"] == int(id):
                        return JsonResponse(i, safe=False)
                    else:
                        return HttpResponse("This data does not exist")
            else:
                return HttpResponse("This data does not exist")
    elif request.method == "DELETE":
        if os.stat(constants.FILE_NAME).st_size == 0:
            return JsonResponse([], safe=False)
        else:
            data = service.get_contents_of_file()
            if entity in data:
                response = data[entity]
                for i in response:
                    if i["id"] == int(id):
                        data[entity].remove(i)
                        if len(data[entity]) == 0:
                            del data[entity]
                        service.write_to_file(data)
                        return HttpResponse("This data is deleted")
                    else:
                        return HttpResponse("This data does not exist")
            else:
                return HttpResponse("This data does not exist")
    elif request.method == "PUT":
        if os.stat(constants.FILE_NAME).st_size == 0:
            return JsonResponse([], safe=False)
        else:
            data = service.get_contents_of_file()
            if entity in data:
                response = data[entity]
                for i in response:
                    if i["id"] == int(id):
                        data[entity].remove(i)
                        req = json.loads(request.body.decode('utf-8'))
                        req["id"] = int(id)
                        data[entity].append(req)
                        service.write_to_file(data)
                        return HttpResponse("This data is updated")
                    else:
                        return HttpResponse("This data does not exist")
            else:
                return HttpResponse("This data does not exist")
    else:
        return HttpResponse("This is not a valid request")
