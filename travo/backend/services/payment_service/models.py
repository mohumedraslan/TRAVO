from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

# This would be imported from a database module in a real application
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    type = Column(String, nullable=False)  # credit_card, debit_card, paypal, etc.
    billing_details = Column(JSON, nullable=False)
    card_details = Column(JSON, nullable=True)  # For card methods
    is_default = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)  # Soft delete
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentIntent(Base):
    __tablename__ = "payment_intents"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    description = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    status = Column(String, nullable=False)  # pending, processing, succeeded, failed, etc.
    payment_method_id = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    refunds = relationship("Refund", back_populates="payment_intent")
    transactions = relationship("Transaction", back_populates="payment_intent")

class Refund(Base):
    __tablename__ = "refunds"
    
    id = Column(String, primary_key=True)
    payment_intent_id = Column(String, ForeignKey("payment_intents.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)  # pending, succeeded, failed
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payment_intent = relationship("PaymentIntent", back_populates="refunds")
    transactions = relationship("Transaction", back_populates="refund")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    type = Column(String, nullable=False)  # payment, refund, payout, fee
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="USD")
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False)  # pending, succeeded, failed
    payment_method_id = Column(String, nullable=True)
    payment_intent_id = Column(String, ForeignKey("payment_intents.id"), nullable=True)
    refund_id = Column(String, ForeignKey("refunds.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    payment_intent = relationship("PaymentIntent", back_populates="transactions")
    refund = relationship("Refund", back_populates="transactions")
