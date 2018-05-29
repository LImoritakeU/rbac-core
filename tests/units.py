import time
from datetime import datetime
from unittest import TestCase

from sqlalchemy import and_

from .testbase import TestBase
from rbac.models import *


class TestUser(TestBase):
    def test_can(self):
        self.fail()


class TestSession(TestBase):
    pass


class TestRole(TestBase):
    def test_add_permission(self):
        self.fail()

    def test_remove_permission(self):
        self.fail()


class TestPermission(TestBase):

    def test_name(self):
        create = Operation(name='create')
        L1_data = Resource(name='L1_data')
        p = Permission(operation=create, resource=L1_data)
        self.assertEqual("create_L1_data", p.name)


class TestCommonMixin(TestBase):
    user = User(name="test", password="test")

    def test_id(self):
        self.assertIsNone(self.user.id)
        db.sess.add(self.user)
        db.sess.commit()

        self.assertIsNotNone(self.user.id)

    def test_repr(self):
        self.assertEqual("User(name=test)", self.user.__repr__())


class TestAuditMixin(TestBase):
    user = User(name="test", password="test")

    def test_create_at(self):
        self.assertIsNone(self.user.created_at)
        db.sess.add(self.user)
        db.sess.commit()
        self.assertIsNotNone(self.user.created_at)
        self.assertIsInstance(self.user.created_at, datetime)

    def test_update_at(self):
        u = User(name="new", password="d")
        db.sess.add(u)
        db.sess.commit()
        self.assertIsNotNone(u.updated_at)
        dt1 = u.updated_at
        u.name = "update_user"
        db.sess.commit()
        dt2 = u.updated_at

        self.assertNotEqual(dt1, dt2)


class TestDataAccessLayer(TestCase):

    def test_init(self):
        db.init()
        self.assertIsNotNone(db.sess)

    def test_drop_all(self):
        db.init()
        self.assertTrue(
            db.engine.dialect.has_table(db.engine, 'role')
        )

        db.drop_all()
        self.assertFalse(
            db.engine.dialect.has_table(db.engine, 'role')
        )



    def test_setup_default_column(self):
        db.init()
        self.assertIsNotNone(
            db.sess.query(Role).filter(and_(
                Role.name == "anonymous",
                Role.id == 1,
            )).first()
        )
