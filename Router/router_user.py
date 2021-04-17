from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Database import database, models
from Repository import repo_user, hashing
from . import schemas


router = APIRouter(
    tags=['Users']
)

get_db = database.get_db


# @router.post('/login', response_model=schemas.ShowUser)
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     return repo_user.create(request, db)

# @router.post('/login')
# def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(models.User.email == request.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Invalid Credentials")
#     if not hashing.verify(user.password, request.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Incorrect password")
#
#     access_token = token.create_access_token(data={"sub": user.email})
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign-up', response_model=schemas.ShowUser)
def create_user(request: schemas.UserSignUp, db: Session = Depends(get_db)):
    return repo_user.createSignUp(request, db)


@router.post('/verify-user')
def create_user(request: schemas.VerifyUser, db: Session = Depends(get_db)):
    return repo_user.verifyUser(request, db)


@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return repo_user.getOneSignUp(user_id, db)


@router.get('/resend-otp/{user_id}')
def resend_otp_user(user_id: int, db: Session = Depends(get_db)):
    return repo_user.resendOTPUser(user_id, db)
