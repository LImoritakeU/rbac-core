from sqlalchemy import and_

from .testbase import IntegrateTestBase
from rbac.models import *


class TestSession(IntegrateTestBase):
    pass


class TestRole(IntegrateTestBase):
    def test_add_permission(self):
        self.fail()

    def test_remove_permission(self):
        self.fail()


class TestPermission(IntegrateTestBase):
    pass
