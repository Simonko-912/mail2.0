from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from starlette.responses import Response
import markdown2
import uvicorn

app = FastAPI(middleware=[Middleware(SessionMiddleware, secret_key="SUPERSECRET123")])

templates = Jinja2Templates(directory="templates")

# DB Setup
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    messages_sent = relationship("Message", back_populates="sender", foreign_keys="Message.from_user_id")
    messages_received = relationship("Message", back_populates="recipient", foreign_keys="Message.to_user_id")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, default="No Subject")  # Add this line
    content = Column(Text)

    sender = relationship("User", foreign_keys=[from_user_id], back_populates="messages_sent")
    recipient = relationship("User", foreign_keys=[to_user_id], back_populates="messages_received")

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auth helpers
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Session-based current user
def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("user")
    if not username:
        return None
    user = get_user_by_username(db, username)
    return user

# Routes

@app.get("/", response_class=HTMLResponse)
def home(request: Request, current_user: User = Depends(get_current_user)):
    if current_user:
        return RedirectResponse(url="/inbox")
    return RedirectResponse(url="/login")

@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request,
           username: str = Form(...),
           email: str = Form(...),
           password: str = Form(...),
           password2: str = Form(...),
           db: Session = Depends(get_db)):
    error = None
    if password != password2:
        error = "Passwords don't match!"
        return templates.TemplateResponse("signup.html", {"request": request, "error": error})

    if get_user_by_username(db, username):
        error = "Username taken."
        return templates.TemplateResponse("signup.html", {"request": request, "error": error})

    if get_user_by_email(db, email):
        error = "Email already registered."
        return templates.TemplateResponse("signup.html", {"request": request, "error": error})

    hashed_pw = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Log in immediately after signup
    request.session["user"] = username
    return RedirectResponse(url="/inbox", status_code=303)



@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/inbox", response_class=HTMLResponse)
def inbox(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")

    msgs = db.query(Message).filter(Message.to_user_id == current_user.id).all()
    msgs_data = []
    for m in msgs:
        content_html = markdown2.markdown(m.content)  # parse markdown to HTML
        # Create a preview snippet of first 8 words (plain text)
        preview_words = m.content.split()
        preview = ' '.join(preview_words[:8])
        if len(preview_words) > 8:
            preview += '...'

        msgs_data.append({
            "from_username": m.sender.username,
            "from_email": m.sender.email,
            "subject": m.subject or "No Subject",
            "preview": preview,
            "full_content": content_html
        })
    all_users = db.query(User).all()
    return templates.TemplateResponse("inbox.html", {
        "request": request,
        "username": current_user.username,
        "messages": msgs_data,
        "all_users": all_users
    })


@app.post("/send")
def send_message(
    request: Request,
    to_email: str = Form(...),
    subject: str = Form(None),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(request, db)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    recipient = get_user_by_email(db, to_email)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    msg = Message(
        from_user_id=current_user.id,
        to_user_id=recipient.id,
        subject=subject or "No Subject",
        content=message
    )
    db.add(msg)
    db.commit()
    return RedirectResponse("/inbox", status_code=303)





@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request,
          username: str = Form(...),
          password: str = Form(...),
          db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    
    request.session["user"] = username
    return RedirectResponse(url="/inbox", status_code=303)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Allow external access
        port=10000,         # Use port 80 (default HTTP)
        reload=True
    )
