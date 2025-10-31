from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import re

class PaymentMethodType(str, Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"
    CANCELED = "canceled"

class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    PAYOUT = "payout"
    FEE = "fee"

class CreditCardInfo(BaseModel):
    last4: str
    brand: str
    exp_month: int
    exp_year: int

class PaymentMethodCreate(BaseModel):
    user_id: str
    type: PaymentMethodType
    billing_details: Dict[str, Any]
    card_number: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None
    card_cvc: Optional[str] = None
    
    @validator('card_number')
    def validate_card_number(cls, v, values):
        if values.get('type') in [PaymentMethodType.CREDIT_CARD, PaymentMethodType.DEBIT_CARD]:
            if not v:
                raise ValueError('Card number is required for credit/debit cards')
            # Remove spaces and dashes
            v = re.sub(r'[\s-]', '', v)
            # Basic validation (Luhn algorithm would be used in a real implementation)
            if not v.isdigit() or len(v) < 13 or len(v) > 19:
                raise ValueError('Invalid card number format')
        return v
    
    @validator('card_exp_month')
    def validate_exp_month(cls, v, values):
        if values.get('type') in [PaymentMethodType.CREDIT_CARD, PaymentMethodType.DEBIT_CARD]:
            if not v:
                raise ValueError('Expiration month is required for credit/debit cards')
            if not isinstance(v, int) or v < 1 or v > 12:
                raise ValueError('Expiration month must be between 1 and 12')
        return v
    
    @validator('card_exp_year')
    def validate_exp_year(cls, v, values):
        if values.get('type') in [PaymentMethodType.CREDIT_CARD, PaymentMethodType.DEBIT_CARD]:
            if not v:
                raise ValueError('Expiration year is required for credit/debit cards')
            current_year = datetime.now().year
            if not isinstance(v, int) or v < current_year or v > current_year + 20:
                raise ValueError(f'Expiration year must be between {current_year} and {current_year + 20}')
        return v
    
    @validator('card_cvc')
    def validate_cvc(cls, v, values):
        if values.get('type') in [PaymentMethodType.CREDIT_CARD, PaymentMethodType.DEBIT_CARD]:
            if not v:
                raise ValueError('CVC is required for credit/debit cards')
            if not v.isdigit() or len(v) < 3 or len(v) > 4:
                raise ValueError('CVC must be 3 or 4 digits')
        return v

class PaymentMethodResponse(BaseModel):
    id: str
    user_id: str
    type: PaymentMethodType
    billing_details: Dict[str, Any]
    card_details: Optional[CreditCardInfo] = None
    is_default: bool
    created_at: datetime

class PaymentIntentCreate(BaseModel):
    user_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PaymentIntentResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    status: PaymentStatus
    payment_method_id: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class RefundRequest(BaseModel):
    payment_intent_id: str
    amount: Optional[float] = None  # If not provided, full refund
    reason: Optional[str] = None

class RefundResponse(BaseModel):
    id: str
    payment_intent_id: str
    amount: float
    status: PaymentStatus
    reason: Optional[str] = None
    created_at: datetime

class TransactionResponse(BaseModel):
    id: str
    user_id: str
    type: TransactionType
    amount: float
    currency: str
    description: Optional[str] = None
    status: PaymentStatus
    payment_method_id: Optional[str] = None
    payment_intent_id: Optional[str] = None
    refund_id: Optional[str] = None
    created_at: datetime
