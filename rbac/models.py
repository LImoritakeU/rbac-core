# coding: utf-8
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, DateTime, ForeignKey, Integer, String, Table,
    Text, desc, )
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

__all__ = (
    "db",
    "User",
    "Role",
    "Permission",
    "Operation",
    "Resource",
    "Session",
)

Base = declarative_base()
metadata = Base.metadata
URL = 'postgres://postgres:password@127.0.0.1:5432/rbac'


class DataAccessLayer:

    url = None
    sess = None

    def __init__(self, url=None):
        self.url = url
        self.engine = create_engine(url)
        Session = sessionmaker(bind=self.engine)
        self.sess = Session()

    def create_all(self):
        metadata.create_all(self.engine)
        self._prepare_default_column()

    def drop_all(self):
        # make sure session commit, or It will be hanging.
        db.sess.commit()
        metadata.drop_all(self.engine)

    def _prepare_default_column(self):
        r1_name = "anonymous"
        r1 = self.sess.query(Role).get(1)
        if not r1:
            r1 = Role(name=r1_name)
        elif r1.name != r1_name:
            r1.name = r1_name

        self.sess.add(r1)
        self.sess.commit()


db = DataAccessLayer(url=URL)


class CommonMixin:
    """make id auto_increment and use sequence type"""
    __slots__ = ()

    @declared_attr
    def id(cls):
        return Column(
            Integer,
            Sequence(f'{cls.__tablename__.lower()}_id_seq', 1, 1),
            primary_key=True
        )

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"(name={getattr(self, 'name')})"


class AuditMixin:
    __slots__ = ()

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Resource(CommonMixin, Base):
    __tablename__ = 'resource'

    name = Column(Text, nullable=False, unique=True)
    permission = relationship('Permission')


class Operation(CommonMixin, Base):
    __tablename__ = 'operation'

    name = Column(Text, nullable=False, unique=True)
    permission = relationship('Permission')


t_permission_roles = Table(
    'permission_roles', metadata,
    Column('role', ForeignKey('role.id'), primary_key=True, nullable=False),
    Column('permission', ForeignKey('permission.id'), primary_key=True, nullable=False, index=True)
)


class Permission(AuditMixin, CommonMixin, Base):
    __tablename__ = 'permission'

    name = Column(Text, nullable=False, unique=True)
    operation_id = Column(ForeignKey('operation.id'), nullable=False, index=True)
    resource_id = Column(ForeignKey('resource.id'), nullable=False, index=True)
    role = relationship('Role', secondary=t_permission_roles)
    operation = relationship('Operation')
    resource = relationship('Resource')

    def __init__(self, operation, resource, name=None):
        super().__init__()
        self.operation = operation
        self.resource = resource
        self.name = name if name else f"{operation.name}_{resource.name}"


t_role_sessions = Table(
    'role_sessions', metadata,
    Column('role', ForeignKey('role.id'), primary_key=True, nullable=False),
    Column('session', ForeignKey('session.id'), primary_key=True, nullable=False, index=True)
)

t_role_users = Table(
    'role_users', metadata,
    Column('user', ForeignKey('user.id'), primary_key=True, nullable=False),
    Column('role', ForeignKey('role.id'), primary_key=True, nullable=False, index=True)
)


class Role(AuditMixin, CommonMixin, Base):
    __tablename__ = 'role'

    name = Column(String(255), nullable=False, unique=True)
    user = relationship('User', secondary=t_role_users)
    session = relationship('Session', secondary=t_role_sessions)
    permission = relationship('Permission', secondary=t_permission_roles)

    def add_permission(self):
        pass

    def remove_permission(self):
        pass

    def is_permitted(self, permission):
        if permission in self.permission:
            return True
        return False


class Session(AuditMixin, CommonMixin, Base):
    __tablename__ = 'session'

    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    user = relationship('User')
    roles = relationship('Role', secondary=t_role_sessions)

    def __repr__(self):
        return f"id={self.id}"


class User(AuditMixin, CommonMixin, Base):
    __tablename__ = 'user'

    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    roles = relationship('Role', secondary=t_role_users)

    def __init__(self, name=None, password=None, roles=None):
        self.name = name
        self.password = password
        self.roles = roles

    @property
    def _session(self):
        if not self.roles:
            return None
        return (
            db.sess.query(Session)
            .filter(Session.user_id == self.id)
            .order_by(desc(Session.created_at))
            .first()
        )

    @property
    def current_roles(self):
        if not self._session or not hasattr(self._session, 'roles'):
            return []
        return self._session.roles

    def _add_session(self, roles=None):
        s = Session(user=self, roles=roles)
        db.sess.add(s)
        db.sess.commit()

    def activate_role(self, role):
        if (role in self.roles) and (role not in self.current_roles):

            if self.current_roles:
                new_roles = [r for r in self.current_roles].append(role)
            else:
                new_roles = [role, ]
            self._add_session(new_roles)
            return True
        return False

    def deactivate_role(self, role):
        if (role in self.roles) and (role in self._session.roles):
            new_roles = [r for r in self._session.roles if not role]
            self._add_session(new_roles)

    def is_allowed(self, permission):
        if self.current_roles:
            for role in self.current_roles:
                if role.is_permitted(permission):
                    return True
        return False

