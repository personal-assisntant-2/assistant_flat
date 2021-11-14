from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse
from .models import UploadedFiles


class BaseFileManagerTestCase(TestCase):
    ...


class BaseFileManagerTestCaseWithUser(BaseFileManagerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = 'test'
        cls.password = 'test'
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user)

    # @classmethod
    # def tearDownClass(cls):
    #     super().tearDownClass()
    #     User.objects.all().delete()
    #     cls.user = None


class TestFileManagerViewRedirect(BaseFileManagerTestCase):
    def test_redirect(self):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],
            reverse('login') + '?next=/file_manager/'
        )


class TestFileManagerView(BaseFileManagerTestCaseWithUser):
    # def _login_user(self, username, password):
    #     response = self.client.post(
    #         reverse('login'),
    #         data=dict(username=username, password=password)
    #     )
    def displaying_the_upload_file_in_file_list(self, file_name):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(response.status_code, 200)
        response_redirect_html = response.content.decode('utf-8')
        self.assertIn(file_name, response_redirect_html)

    def test_get(self):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(response.status_code, 200)
        # user = auth.get_user(self.client)
        # print('.....', user.is_authenticated)
        response_html = response.content.decode('utf-8')
        self.assertIn('Upload file', response_html)
        self.assertIn('Sort by category', response_html)

    def test_upload_video(self):
        file_name = "file.mp4"
        video = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        response = self.client.post(reverse('file_manager:file'), {'file': video})
        self.assertEquals(response.status_code, 302)
        self.displaying_the_upload_file_in_file_list(file_name)


# class TestFileDownloadView(BaseFileManagerTestCaseWithUser):
#
#     def setUp(self):
#         super().setUp()
#         self.file = ContentFile('text', 'name')
#         print('.........self.file', vars(self.file))
#         # self.f = b''
#         # # Reading file
#         # for chunk in file.chunks():
#         #     self.f += chunk
#         UploadedFiles.objects.create(file=self.file)
#
#     def test_download_video(self):
#         pass













