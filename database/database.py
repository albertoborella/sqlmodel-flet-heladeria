from sqlmodel import SQLModel, Session, select, create_engine
from models.stock_model import Gusto, Ingreso, Conteo
from models.user_model import User

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    print("🔧 Creando tablas...")
    SQLModel.metadata.create_all(engine)

def crear_admin():
    with Session(engine) as session:
        admin = session.exec(
            select(User).where(User.username == "admin")
        ).first()

        if not admin:
            nuevo_admin = User(
                username="admin",
                password="admin",
                is_admin=True
            )
            session.add(nuevo_admin)
            session.commit()
            print("✅ Usuario admin creado")
        else:
            print("ℹ️ Usuario admin ya existe")
