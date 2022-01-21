import uvicorn
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from datetime import timedelta
from app import models, schemas, crud
from app.database import engine, SessionLocal
from app.app_utils import create_access_token,decode_access_token


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        print(token)
        payload = decode_access_token(data=token)
        print(payload)
        public_id: str = payload.get("sub")
        if public_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(public_id=public_id)
    except PyJWTError:
        raise credentials_exception
    user = crud.get_user_by_public_id(db, public_id=token_data.public_id)
    if user is None:
        raise credentials_exception
    return user



@app.get("/")
async def API():
    return {"API NAME": "AaoNxt Partner"}

@app.post("/register", response_model=schemas.UserInfo)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    


@app.post("/login", response_model=schemas.Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email not existed")
    else:
        is_password_correct = crud.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:            
            access_token_expires = timedelta(minutes=1440)            
            access_token = create_access_token(
                data={"sub": db_user.public_id}, expires_delta=access_token_expires)
            return {"token": access_token, "token_type": "Bearer"}

@app.get("/alluser")
async def alluser(current_user: schemas.UserInfo = Depends(get_current_user)
                        , db: Session = Depends(get_db)):
    return crud.alluser(db=db)
    
