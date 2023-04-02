from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerUser(Base):
    __tablename__ = "customer_user"

    private_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password_encrypted = Column(String, nullable=False)


class RentalBusinessRegisterAccountInvite(Base):
    __tablename__ = "rental_business_user_register_account_token"

    private_id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    used_by = Column(Integer, nullable=True, unique=True, default=None)


class RentalBusinessUser(Base):
    __tablename__ = "rental_business_user"

    private_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    password_encrypted = Column(String, nullable=False)


class RentalBusinessUserInfo(Base):
    __tablename__ = "rental_business_user_info"

    private_id = Column(Integer, primary_key=True, index=True)
    rental_business_user_id = Column(Integer, unique=True)
    business_type = Column(String, nullable=True)
    business_title = Column(String, nullable=True)
    business_description = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)


class RentalBusinessUserInfoImage(Base):
    __tablename__ = "rental_business_user_info_image"

    private_id = Column(Integer, primary_key=True, index=True)
    rental_business_user_id = Column(Integer, unique=True)
    filename = Column(String, nullable=False)


class RentalBusinessUserInfoImageMain(Base):
    __tablename__ = "rental_business_user_info_image_main"

    private_id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, unique=True)
    rental_business_user_id = Column(Integer, unique=True)


class Board(Base):
    __tablename__ = "board"

    private_id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    rental_business_user_id = Column(Integer, nullable=False)
