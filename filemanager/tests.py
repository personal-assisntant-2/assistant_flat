"""
Tests for filemanager.
"""
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import UploadedFiles


class BaseFileManagerTestCase(TestCase):
    ...


class BaseFileManagerTestCaseWithUser(BaseFileManagerTestCase):
    """
    Base class, creates a user before running tests.
    """
    @classmethod
    def setUpClass(cls):
        """
        A user will be created in each class that will inherit from the
        BaseFileManagerTestCaseWithUser class.
        """
        super().setUpClass()
        cls.username = 'test'
        cls.password = 'test'
        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )

    def setUp(self):
        """
        The user will be logged in before each test.
        """
        super().setUp()
        self.client.force_login(self.user)

    def _upload_video(self, file_name):
        """
        Generates a file and sends it to the server.
        """
        video = SimpleUploadedFile(
            file_name,
            b"file_content",
            content_type="video/mp4"
        )
        return self.client.post(reverse('file_manager:file'), {'file': video})


class TestFileManagerViewRedirect(BaseFileManagerTestCase):
    """
    Base class, has no registered user.
    """
    def test_redirect(self):
        """
        Checks the access of a non-logged in user to a resource,
        access to which is denied to non-logged in users
        """
        response = self.client.get(reverse('file_manager:file'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],
            reverse('login') + '?next=/file_manager/'
        )


class TestFileManagerView(BaseFileManagerTestCaseWithUser):
    """
    Test views.py file_manager_view
    """

    def _displaying_the_upload_file_in_file_list(self, file_name):
        """
        Checks the display of the uploaded file in the list of uploaded files of the given user.
        """
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
        """
        Checks the page renderer on a GET request to the address 'file manager: file'.
        """
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
        """
        Verifies file upload.
        """
        response = self._upload_video("file.mp4")
        self.assertEquals(
            response.status_code,
            302
        )
        self._displaying_the_upload_file_in_file_list("file.mp4")


class TestFileDownloadView(BaseFileManagerTestCaseWithUser):
    """
    Test views.py file_delete_view
    """
    def test_download_video(self):
        """
        Verifies file download.
        """
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
