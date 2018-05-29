import unittest

from rbac.models import db
from rbac.models import User, Role, Session, Operation, Resource, Permission


TEST_DB_URL = None



class TestBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if TEST_DB_URL:
            db.conn_string = TEST_DB_URL

    @classmethod
    def tearDownClass(cls):
        db.sess.close()


class IntegrateTestBase(TestBase):

    def setUp(self):
        if db.engine.dialect.has_table(db.engine, "user"):
            db.drop_all()
        db.create_all()
        prep_db(db)

    def tearDown(self):
        db.drop_all()


class SystemTestBase(TestBase):

    def setUp(self):
        if db.engine.dialect.has_table(db.engine, 'user'):
            db.drop_all()
        db.create_all()
        prep_db(db)


def prep_db(db):
    data_L1 = Resource(name="L1")
    data_L2 = Resource(name="L2")

    create = Operation(name="create")
    retrieve = Operation(name="retrieve")
    update = Operation(name="update")
    delete = Operation(name="delete")

    pm_c = Permission(operation=create, resource=data_L1)
    pm_r = Permission(operation=retrieve, resource=data_L1)
    pm_u = Permission(operation=update, resource=data_L1)
    pm_d = Permission(operation=delete, resource=data_L1)
    pm_c_l2 = Permission(operation=create, resource=data_L2)

    general = Role(name="general", permission=[pm_r, pm_c_l2])
    manager = Role(name="manager", permission=[pm_c, pm_r, pm_u])
    admin = Role(name="admin", permission=[pm_c_l2, pm_c, pm_d, pm_u, pm_r])

    adam = User(name="Adam", password="test", roles=[general])
    andy = User(name="Andy", password="test", roles=[manager])
    amy = User(name="Amy", password="test", roles=[admin])

    db.sess.add_all([
        adam, andy, amy, general, manager, data_L1, data_L2, create, retrieve,
        update, delete, pm_c, pm_r, pm_u, pm_d, pm_c_l2, admin
    ])
    db.sess.commit()
