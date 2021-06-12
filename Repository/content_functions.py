from sqlalchemy.orm import Session
from Database import models
import json
from fastapi import HTTPException, status
import random

# With respect to Course name
def getAllBlogsAndQuizes(course, db: Session):
    blogs = db.query(models.BlogContent).filter(models.BlogContent.course == course)
    myJson = {}
    blogArr = []
    for blog in blogs:
        oneBlog = {
            "id": blog.id,
            "name": blog.name,
            "link": "/course?content=" + blog.url
        }
        blogArr.append(oneBlog)

    quizes = db.query(models.QuizContent).filter(models.QuizContent.course == course)
    # if(quizes === )
    print(quizes)
    quizArr = []
    for quiz in quizes:
        oneQuiz = {
            "id": quiz.id,
            "name": quiz.name,
            "link": "/quiz?content=" + quiz.url
        }
        quizArr.append(oneQuiz)

    myJson = {
        "courses": blogArr,
        "quizes": quizArr
    }

    return myJson

# With respect to blog url
def getBlog(url, db: Session):
    content = db.query(models.BlogContent).filter(models.BlogContent.url == url).first()

    try:
        file = open("Blogs/" + content.filename, 'r+')
        data = json.load(file)
        return ({"blogDetail": json.dumps(data)})
    except:
        # e = sys.exc_info()[0]
        # print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# With respect to blog url
def getQuiz(url, db: Session):
    content = db.query(models.QuizContent).filter(models.QuizContent.url == url).first()
    print(content)
    try:
        file = open("Quizes/" + content.filename, 'r+')
        data = json.load(file)

        myIndexes = random.sample(range(0, len(data)), 10)
        myQues = []

        for index in myIndexes:
            myQues.append(data[index])

        print(myQues)
        return ({"name": content.name, "questions": json.dumps(myQues)})
    except:
        # e = sys.exc_info()[0]
        # print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)