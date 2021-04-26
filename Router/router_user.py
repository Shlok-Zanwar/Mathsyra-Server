from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from Database import database, models
from Repository import repo_user, hashing, token, OAuth2
from Router import schemas
from fastapi import HTTPException, status
import json


router = APIRouter(
    tags=['Users']
)

get_db = database.get_db



cards = [
    {
        "id":1,
        "title": "Vedic Maths",
        "description": "Vedic Mathematics is a collection of Techniques/Sutras to solve mathematical arithmetics in easy and faster way.",
        "button_text": "Explore",
        "image": "https://i.ibb.co/kh08LcK/vedic-maths-card-image.jpg",
        "link": "/vedic-maths"
    },
    {
        "id":2,
        "title": "Trigonometry",
        "description": "In Indian astronomy, the study of trigonometric functions flourished in the Gupta period, especially due to Aryabhata (sixth century CE), who discovered the sine function.",
        "button_text": "Explore",
        "image": "https://d2gg9evh47fn9z.cloudfront.net/800px_COLOURBOX28495134.jpg",
        "link": "/Trigonometry"
    },
    {
        "id":3,
        "title": "Algebra",
        "description": "By the time of Aryabhata (499 AD) and Brahmagupta (628 AD), symbolic algebra had evolved in India into a distinct branch of mathematics and became one of its central pillars.",
        "button_text": "Explore",
        "image": "https://i.ibb.co/pyD6mmT/algebra-2.jpg",
        "link": "/Algebra"
    },
    {
        "id":4,
        "title": "Geometry",
        "description": "Vedic geometry involves a study of the Śulbasūtras, conservatively dated as recorded between 800 and 500 BCE, though they contain knowledge from earlier times.",
        "button_text": "Explore",
        "image": "https://i.ibb.co/nLQzZGb/geometry-card-image.jpg",
        "link": "/Geometry"
    }
]

vedic = {
  "vedic_maths": {
    "courses": [
      {
        "id": 1,
        "name": "Vedic Addition / Substraction",
        "link": "/course?content=vedic-add-sub"
      },
      {
        "id": 2,
        "name": "Vedic Mulltiplication",
        "link": "/course?content=vedic-mul"
      },
      {
        "id": 3,
        "name": "Vedic Squares",
        "link": "/course?content=vedic-squares"
      }
    ],
    "quizes":[
      {
        "id": 1,
        "name": "Vedic Addition / Substraction",
        "link": "/quiz?content=vedic-add-sub"
      },
      {
        "id": 3,
        "name": "Vedic Mulltiplication",
        "link": "/quiz?content=vedic-mul"
      },
      {
        "id": 2,
        "name": "Vedic Squares",
        "link": "/quiz?content=vedic-squares"
      }
    ]
  }
}







@router.post('/login')
def login(request: schemas.UserLogIn, db: Session = Depends(get_db)):
    # print("hiiiiii")
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not hashing.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")

    access_token = token.create_access_token(data={"username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign-up', response_model=schemas.ShowUser)
def create_user(request: schemas.UserSignUp, db: Session = Depends(get_db)):
    return repo_user.createSignUp(request, db)


@router.post('/verify-user')
def verify_user(request: schemas.VerifyUser, db: Session = Depends(get_db)):
    return repo_user.verifyUser(request, db)


@router.get('/vedic-maths')
def vedicMaths(request: Request):

    # print("hiiii")
    id = OAuth2.get_current_user(request.headers['token'])
    return vedic['vedic_maths']


@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return repo_user.getOneSignUp(user_id, db)





@router.get('/resend-otp/{user_id}')
def resend_otp_user(user_id: int, db: Session = Depends(get_db)):
    return repo_user.resendOTPUser(user_id, db)




@router.get('/')
def home(request: Request):
    # print((request.headers['token']))
    print(request.headers['token'])
    id = OAuth2.get_current_user(request.headers['token'])
    return cards



