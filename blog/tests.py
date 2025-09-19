from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import CustomUser
from blog.models import Post, Category, Comment


class TestBlog(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username='test_user', password='12345678Aa!', is_staff=True)
        cls.category = Category.objects.create(name='test_category', slug='test-category')
        cls.category_2 = Category.objects.create(name='test_category2', slug='test-category2')
        cls.post = Post.objects.create(
            title='test title',
            slug='test-title',
            author=cls.user,
            status='published',
            category=cls.category
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            content='test content',
            is_approved=True
        )

    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_api_posts(self):
        response = self.client.get(reverse('posts_api'))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['title'], 'test title')

    def test_api_category(self):
        response = self.client.get(reverse('category_api'))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['name'], self.category.name)

    def test_api_posts_category(self):
        response = self.client.get(reverse('posts_api'), query_params={'category': self.category.pk})
        data = response.json()
        response_2 = self.client.get(reverse('posts_api'), query_params={'category': self.category_2.pk})
        data_2 = response_2.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["results"][0]["title"], 'test title')
        self.assertEqual(data_2["results"], [])

    def test_api_get_comments(self):
        response = self.client.get(reverse('post_api_comment', kwargs={'pk':self.post.pk}))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['author'], self.user.username)

    def test_api_profile(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile_api'))
        data = response.json()
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['is_staff'], True)
