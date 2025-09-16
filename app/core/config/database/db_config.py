from pydantic import BaseModel, PostgresDsn


class DatabaseConfig(BaseModel):
    """
    https://alembic.sqlalchemy.org/en/latest/naming.html#integration-of-naming-conventions-into-operations-autogenerate
    https://docs.sqlalchemy.org/en/20/core/constraints.html#constraint-naming-conventions
    """

    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # правила для именования индексов, unique constraint,
    # check constraint, primary constraint, pk, fk
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
