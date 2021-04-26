from sqlalchemy import Column, Integer, String, JSON, BIGINT
from Database.database import Base


# Login ---- sign-up Check
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    school = Column(String)
    phone_no = Column(BIGINT)


# Verify ---- Signup --- login
class UserSignUp(Base):
    __tablename__ = 'UsersSignUp'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    verification = Column(JSON)

