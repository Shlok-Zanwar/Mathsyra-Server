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



class QuizContent(Base):
    __tablename__ = 'QuizContent'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    course = Column(String)
    name = Column(String)
    url = Column(String)
    filename = Column(String)



class BlogContent(Base):
    __tablename__ = 'BlogContent'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    course = Column(String)
    name = Column(String)
    url = Column(String)
    filename = Column(String)