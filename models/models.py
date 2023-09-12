from sqlalchemy import (
    JSON,
    BigInteger,
    Float,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("telegram_id", BigInteger, nullable=False),
    Column("balance", Float, default=0.00),
    Column("permissons", JSON),
    Column("application_id", Integer, ForeignKey("application.id")),
)

application = Table(
    "application",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("business direction", String, nullable=False),
    Column("bot development platform", String, nullable=False),
    Column("min_budget", Integer, nullable=False),
    Column("max_budget", Integer, nullable=False),
    Column("phone", String, nullable=False),
)
