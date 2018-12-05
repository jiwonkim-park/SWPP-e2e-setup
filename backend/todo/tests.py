from django.test import TestCase, Client
from .models import Todo
import json
'''
class TodoTestCase(TestCase):
    def test_index(self):
        client = Client()
        response = client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'Hello World!')
'''
class TodoTestCase(TestCase):
    def setUp(self):
        self.todo1 = Todo.objects.create(content='Project 1', done=False)
        self.todo2 = Todo.objects.create(content='Portion Homework', done=False)

    def test_todo_list(self):
        client = Client()
        response = client.get('/api/todo/')
        self.assertJSONEqual(response.content, [{"id": 1, "content": "Project 1", "done": False}, {"id": 2, "content": "Portion Homework", "done": False}])

        response = client.post('/api/todo/', json.dumps({
            'content': 'History Exam'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(response.content, {'id': 3, 'content': 'History Exam', 'done': False})

        response = client.post('/api/todo/', json.dumps({
            'wrong': 'something wrong'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = client.put('/api/todo/')
        self.assertEqual(response.status_code, 405)
        response = client.delete('/api/todo/')
        self.assertEqual(response.status_code, 405)
        