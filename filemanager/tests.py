from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
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

    def _upload_video(self, file_name):
        video = SimpleUploadedFile(
            file_name,
            b"file_content",
            content_type="video/mp4"
        )
        return self.client.post(reverse('file_manager:file'), {'file': video})


class TestFileManagerViewRedirect(BaseFileManagerTestCase):

    def test_redirect(self):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],
            reverse('login') + '?next=/file_manager/'
        )


class TestFileManagerView(BaseFileManagerTestCaseWithUser):

    def _displaying_the_upload_file_in_file_list(self, file_name):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(
            response.status_code,
            200
        )
        response_redirect_html = response.content.decode('utf-8')
        self.assertIn(
            file_name,
            response_redirect_html
        )

    def test_get(self):
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(
            response.status_code,
            200
        )

        response_html = response.content.decode('utf-8')
        self.assertIn(
            'Upload file',
            response_html
        )
        self.assertIn(
            'Sort by category',
            response_html
        )

    def test_upload_video(self):
        response = self._upload_video("file.mp4")
        self.assertEquals(
            response.status_code,
            302
        )
        self._displaying_the_upload_file_in_file_list("file.mp4")


class TestFileDownloadView(BaseFileManagerTestCaseWithUser):

    def test_download_video(self):
        self._upload_video("file.mp4")
        file = UploadedFiles.objects.filter(name="file.mp4").first()
        response = self.client.post(
            reverse(
                'file_manager:download',
                kwargs={'file_id': file.id}
            )
        )
        self.assertEquals(
            response.status_code,
            200
        )
        self.assertEquals(
            response.headers['Content-Length'],
            file.size
        )


# from django.contrib import auth
# user = auth.get_user(self.client)
# print('.....', user.is_authenticated)










