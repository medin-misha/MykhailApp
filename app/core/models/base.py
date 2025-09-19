from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__}"