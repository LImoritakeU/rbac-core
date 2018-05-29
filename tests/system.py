from .testbase import SystemTestBase
from rbac.models import *


class TestUser(SystemTestBase):
    def test_user_is_allowed(self):
        adam = db.sess.query(User).filter_by(name='Adam').first()

        p_r = db.sess.query(Permission).filter_by(name="retrieve_L1").first()
        p_c = db.sess.query(Permission).filter_by(name="create_L1").first()

        self.assertFalse(adam.is_allowed(p_r))
        self.assertFalse(adam.is_allowed(p_c))

        adam.activate_role(adam.roles[0])

        self.assertTrue(adam.is_allowed(p_r))
        self.assertFalse(adam.is_allowed(p_c))

        adam.deactivate_role(adam.roles[0])
        self.assertFalse(adam.is_allowed(p_r))
        self.assertFalse(adam.is_allowed(p_c))
