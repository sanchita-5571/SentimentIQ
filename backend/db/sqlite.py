from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.config import settings


class Base(DeclarativeBase):
    pass


connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(settings.DATABASE_URL, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_sqlite() -> None:
    from core.security import hash_password
    from db.sql_models import UserRecord

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        seeds = [
            ("admin", settings.ADMIN_EMAIL, "Admin", settings.ADMIN_PASSWORD),
            ("analyst", settings.DEMO_USER_EMAIL, "Demo Analyst", settings.DEMO_USER_PASSWORD),
        ]

        changed = False
        for user_id, email, full_name, password in seeds:
            record = session.query(UserRecord).filter(UserRecord.id == user_id).first()
            if record is None:
                session.add(
                    UserRecord(
                        id=user_id,
                        email=email,
                        full_name=full_name,
                        hashed_password=hash_password(password),
                        is_active=True,
                    )
                )
                changed = True

        if changed:
            session.commit()
