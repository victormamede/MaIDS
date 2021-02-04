import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

from src.app import build_app
from unittest import TestCase

from .mock_app import create_mock_app
from .mocks.permission_mocker import PermissionMocker
from .mocks.mock_user import MockUserClient


class AppTestCase(TestCase):
    def setUp(self):
        self.app = build_app(create_mock_app())
        self.app.testing = True
        self.client = self.app.test_client()

        self.master_token = os.getenv("MASTER_TOKEN")
        self.master_header = {"auth-token": self.master_token}

    def assertNeedsPermission(self, roles):
        return PermissionMocker(roles, self)

    def mockUserClient(self, roles):
        return MockUserClient(roles, self)
