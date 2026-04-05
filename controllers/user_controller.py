from sqlmodel import Session, select
from database.database import engine
from models.user_model import User

def login_user(username: str, password: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()

        if not user:
            return False, "No existe el usuario"
        
        if user.password != password:
            return False, "Contraseña incorrecta"
        
        return True, user 

