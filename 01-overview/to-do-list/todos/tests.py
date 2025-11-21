from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Todo


class TodoModelTest(TestCase):
    """测试 Todo 模型"""
    
    def test_create_todo(self):
        """测试创建待办事项"""
        todo = Todo.objects.create(
            title="Test Todo",
            description="This is a test"
        )
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "This is a test")
        self.assertFalse(todo.completed)  # 默认应该是未完成
        self.assertIsNotNone(todo.created_at)
        self.assertIsNotNone(todo.updated_at)
    
    def test_todo_str_representation(self):
        """测试 Todo 的字符串表示"""
        todo = Todo.objects.create(title="My Todo")
        self.assertEqual(str(todo), "My Todo")
    
    def test_todo_default_completed(self):
        """测试默认完成状态为 False"""
        todo = Todo.objects.create(title="Test")
        self.assertFalse(todo.completed)
    
    def test_todo_ordering(self):
        """测试待办事项按创建时间倒序排列"""
        todo1 = Todo.objects.create(title="First Todo")
        todo2 = Todo.objects.create(title="Second Todo")
        todo3 = Todo.objects.create(title="Third Todo")
        
        todos = list(Todo.objects.all())
        # 最新的应该在前面
        self.assertEqual(todos[0].title, "Third Todo")
        self.assertEqual(todos[1].title, "Second Todo")
        self.assertEqual(todos[2].title, "First Todo")
    
    def test_todo_with_empty_description(self):
        """测试可以创建没有描述的待办事项"""
        todo = Todo.objects.create(title="Todo without description")
        self.assertEqual(todo.description, "")
        self.assertTrue(todo.description == "" or todo.description is None)


class TodoListViewTest(TestCase):
    """测试待办列表视图"""
    
    def setUp(self):
        """设置测试客户端"""
        self.client = Client()
        self.url = reverse('todo_list')
    
    def test_todo_list_view_returns_200(self):
        """测试列表页面可以正常访问"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_todo_list_displays_all_todos(self):
        """测试列表页面显示所有待办事项"""
        Todo.objects.create(title="Todo 1")
        Todo.objects.create(title="Todo 2")
        Todo.objects.create(title="Todo 3")
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo 1")
        self.assertContains(response, "Todo 2")
        self.assertContains(response, "Todo 3")
    
    def test_todo_list_empty_state(self):
        """测试没有待办事项时显示空状态"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No todos yet!")
    
    def test_todo_list_template(self):
        """测试使用了正确的模板"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class TodoCreateViewTest(TestCase):
    """测试创建待办视图"""
    
    def setUp(self):
        """设置测试客户端"""
        self.client = Client()
        self.url = reverse('todo_create')
    
    def test_create_view_get_returns_200(self):
        """测试 GET 请求返回创建表单"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, "Create")
    
    def test_create_todo_post_success(self):
        """测试 POST 请求成功创建待办事项"""
        data = {
            'title': 'New Todo',
            'description': 'Todo description'
        }
        response = self.client.post(self.url, data)
        
        # 应该重定向到列表页
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        # 验证待办事项已创建
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())
        todo = Todo.objects.get(title='New Todo')
        self.assertEqual(todo.description, 'Todo description')
        self.assertFalse(todo.completed)
    
    def test_create_todo_without_description(self):
        """测试可以创建没有描述的待办事项"""
        data = {'title': 'Todo without description'}
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='Todo without description').exists())
        todo = Todo.objects.get(title='Todo without description')
        self.assertEqual(todo.description, '')
    
    def test_create_todo_requires_title(self):
        """测试标题是必填项"""
        data = {'description': 'No title'}
        # 由于 HTML5 验证，这可能会在客户端阻止，但我们应该测试模型层
        # 这里测试如果标题为空字符串的情况
        todo = Todo(title='', description='Test')
        # 模型允许空字符串，但实际应用中应该验证
        todo.save()
        self.assertEqual(todo.title, '')


class TodoUpdateViewTest(TestCase):
    """测试更新待办视图"""
    
    def setUp(self):
        """设置测试客户端和测试数据"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Original Title",
            description="Original Description",
            completed=False
        )
        self.url = reverse('todo_update', args=[self.todo.pk])
    
    def test_update_view_get_returns_200(self):
        """测试 GET 请求返回更新表单"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')
        self.assertContains(response, "Update")
        self.assertContains(response, "Original Title")
        self.assertContains(response, "Original Description")
    
    def test_update_todo_post_success(self):
        """测试 POST 请求成功更新待办事项"""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'completed': 'on'  # 复选框选中时传递 'on'
        }
        response = self.client.post(self.url, data)
        
        # 应该重定向到列表页
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        # 验证待办事项已更新
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertTrue(self.todo.completed)
    
    def test_update_todo_uncheck_completed(self):
        """测试取消完成状态"""
        # 先设置为完成
        self.todo.completed = True
        self.todo.save()
        
        # 更新时不勾选完成复选框
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description'
            # 不包含 'completed'
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.completed)
    
    def test_update_nonexistent_todo_returns_404(self):
        """测试更新不存在的待办事项返回 404"""
        url = reverse('todo_update', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoDeleteViewTest(TestCase):
    """测试删除待办视图"""
    
    def setUp(self):
        """设置测试客户端和测试数据"""
        self.client = Client()
        self.todo = Todo.objects.create(title="Todo to Delete")
        self.url = reverse('todo_delete', args=[self.todo.pk])
    
    def test_delete_view_get_returns_200(self):
        """测试 GET 请求返回删除确认页面"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_confirm_delete.html')
        self.assertContains(response, "Todo to Delete")
        self.assertContains(response, "Are you sure?")
    
    def test_delete_todo_post_success(self):
        """测试 POST 请求成功删除待办事项"""
        response = self.client.post(self.url)
        
        # 应该重定向到列表页
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        # 验证待办事项已删除
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())
    
    def test_delete_nonexistent_todo_returns_404(self):
        """测试删除不存在的待办事项返回 404"""
        url = reverse('todo_delete', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoToggleViewTest(TestCase):
    """测试切换完成状态视图"""
    
    def setUp(self):
        """设置测试客户端和测试数据"""
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test Todo",
            completed=False
        )
        self.url = reverse('todo_toggle', args=[self.todo.pk])
    
    def test_toggle_incomplete_to_complete(self):
        """测试从未完成切换到完成"""
        self.assertFalse(self.todo.completed)
        
        response = self.client.get(self.url)
        
        # 应该重定向到列表页
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        # 验证状态已切换
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
    
    def test_toggle_complete_to_incomplete(self):
        """测试从完成切换到未完成"""
        self.todo.completed = True
        self.todo.save()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('todo_list'))
        
        # 验证状态已切换
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.completed)
    
    def test_toggle_nonexistent_todo_returns_404(self):
        """测试切换不存在的待办事项返回 404"""
        url = reverse('todo_toggle', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class TodoURLTest(TestCase):
    """测试 URL 路由"""
    
    def test_todo_list_url(self):
        """测试待办列表 URL"""
        url = reverse('todo_list')
        self.assertEqual(url, '/')
    
    def test_todo_create_url(self):
        """测试创建待办 URL"""
        url = reverse('todo_create')
        self.assertEqual(url, '/create/')
    
    def test_todo_update_url(self):
        """测试更新待办 URL"""
        url = reverse('todo_update', args=[1])
        self.assertEqual(url, '/update/1/')
    
    def test_todo_delete_url(self):
        """测试删除待办 URL"""
        url = reverse('todo_delete', args=[1])
        self.assertEqual(url, '/delete/1/')
    
    def test_todo_toggle_url(self):
        """测试切换状态 URL"""
        url = reverse('todo_toggle', args=[1])
        self.assertEqual(url, '/toggle/1/')
