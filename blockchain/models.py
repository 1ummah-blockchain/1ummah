# blockchain/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="user", uselist=False)
    kyc = relationship("KYC", back_populates="user", uselist=False)
    referral = relationship("Referral", back_populates="user", uselist=False)

class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="wallet")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class KYC(Base):
    __tablename__ = 'kyc'
    id = Column(Integer, primary_key=True)
    document_filename = Column(String)
    selfie_filename = Column(String)
    status = Column(String, default='pending')  # pending, approved, rejected
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="kyc")

class Referral(Base):
    __tablename__ = 'referrals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    referrer_wallet = Column(String)
    total_bonus = Column(Float, default=0.0)
    total_referrals = Column(Integer, default=0)

    user = relationship("User", back_populates="referral")

class MiningLog(Base):
    __tablename__ = 'mining_log'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String, unique=True)
    last_mined = Column(DateTime)

class SendLog(Base):
    __tablename__ = 'send_log'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String, unique=True)
    last_sent = Column(DateTime)
