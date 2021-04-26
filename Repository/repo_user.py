from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime
from Database import models
from Repository import hashing
from Repository.send_mail import send_otp


def checkEmailExist(email, db: Session):
    user = db.query(models.UserSignUp).filter(models.UserSignUp.email == email).first()
    if not user:
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            return True

        return False

    return True


def checkUsernameExist(username, db: Session):
    user = db.query(models.UserSignUp).filter(models.UserSignUp.username == username).first()
    if not user:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user:
            return True

        return False

    return True


def createSignUp(request, db: Session):
     username = checkUsernameExist(request.username, db)
     email = checkEmailExist(request.email, db)

     print(username)
     print(email)

     if username and email:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Username and Email already exists.")
     elif username:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Username already exists.")
     elif email:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Email already exists.")
     else:
        otp = send_otp("gambhir")
        print(otp)
        new_user = models.UserSignUp(
                                        name=request.name,
                                        email=request.email,
                                        password=hashing.bcrypt(request.password),
                                        username=request.username,
                                        verification={
                                            "otp": otp,
                                            "try": 0,
                                            "datetime": str(datetime.datetime.now())
                                        }
                                    )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def getOneSignUp(user_id, db: Session):
    user = db.query(models.UserSignUp).filter(models.UserSignUp.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not found")
    return user


def addUser(user, db: Session):
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password,
        username=user.username,
        phone_no=None,
        school=None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.query(models.UserSignUp).filter(models.UserSignUp.id == user.id).delete()
    # del_user.delete(synchronize_session = False)
    db.commit()

    return new_user


def resendOTP(user, db: Session):
    verification = {
        "otp": send_otp(user.email),
        "try": 0,
        "datetime": str(datetime.datetime.now())
    }
    user.verification = verification
    db.commit()


def verifyUser(request, db: Session):
    user = db.query(models.UserSignUp).filter(models.UserSignUp.id == request.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {request.id} is not found")

    currTime = datetime.datetime.now()
    secDiff = (currTime - datetime.datetime.strptime(user.verification['datetime'], '%Y-%m-%d %H:%M:%S.%f')).total_seconds()

    # OTP Expired
    if secDiff > 180:
        resendOTP(user, db)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"OTP has expired. New OTP sent to {user.email}")

    else:

        if request.otp == user.verification['otp']:
            addUser(user, db)
            return "Account Verified"

        else:
            if user.verification['try'] == 2:
                resendOTP(user, db)
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"OTP didn't match. Three wrong attempts made, new OTP has been sent to {user.email}.")
            else:
                verification = {
                    "otp": user.verification['otp'],
                    "try": user.verification['try'] + 1,
                    "datetime": user.verification['datetime']
                }
                user.verification = verification
                db.commit()
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"OTP didn't match. You have {3 - verification['try']} attempts left.")


def resendOTPUser(user_id, db: Session):
    user = db.query(models.UserSignUp).filter(models.UserSignUp.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not found")

    currTime = datetime.datetime.now()
    secDiff = (currTime - datetime.datetime.strptime(user.verification['datetime'], '%Y-%m-%d %H:%M:%S.%f')).total_seconds()
    if secDiff > 120:
        resendOTP(user, db)
        return f"New OTP sent to {user.email}"

    else:
        return f"Please wait for {120-int(secDiff)} seconds."

