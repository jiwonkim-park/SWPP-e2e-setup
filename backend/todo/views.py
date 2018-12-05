from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import json
from json.decoder import JSONDecodeError
from .models import Todo

@csrf_exempt
def todo_list(request):
    if request.method == 'GET':
        todo_list = []
        for todo in Todo.objects.all().values():
            todo_list.append(todo)
        return JsonResponse(todo_list, safe=False)
    elif request.method == 'POST':
        try:
            req_data = json.loads(request.body.decode())
            content = req_data['content']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()
        
        todo = Todo.objects.create(content=content)
        response_dict = {
            'id': todo.id,
            'content': todo.content,
            'done': todo.done,
        }
        return JsonResponse(response_dict, status=201)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def target_todo(request, id):
    if request.method == 'GET':
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return HttpResponseNotFound()
        response_dict = {
            'id': todo.id,
            'content': todo.content,
            'done': todo.done
        }
        return JsonResponse(response_dict, safe=False)
    elif request.method == 'PUT':
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return HttpResponseNotFound()
        
        try:
            req_data = json.loads(request.body.decode())
            todo_content = req_data['content']
            todo_done = req_data['done']
        except (KeyError, JSONDecodeError) as e:
            return HttpResponseBadRequest()

        todo.content = todo_content
        todo.done = todo_done
        todo.save()
        return HttpResponse(status=204)
    elif request.method == 'DELETE':
        try:
            todo = Todo.objects.get(id=id)
        except Todo.DoesNotExist:
            return HttpResponseNotFound()
        
        todo.delete()
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])



        