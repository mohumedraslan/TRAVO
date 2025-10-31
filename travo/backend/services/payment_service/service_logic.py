import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import asyncio

# Import schemas
from .schemas import (
    PaymentMethodCreate, 
    PaymentMethodResponse, 
    PaymentIntentCreate, 
    PaymentIntentResponse,
    PaymentStatus,
    PaymentMethodType,
    CreditCardInfo,
    RefundRequest,
    RefundResponse,
    TransactionType,
    TransactionResponse
)

# Mock data for payment methods
MOCK_PAYMENT_METHODS = [
    {
        "id": "pm_1",
        "user_id": "u1",
        "type": PaymentMethodType.CREDIT_CARD,
        "billing_details": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": {
                "line1": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "postal_code": "94111",
                "country": "US"
            }
        },
        "card_details": {
            "last4": "4242",
            "brand": "Visa",
            "exp_month": 12,
            "exp_year": 2025
        },
        "is_default": True,
        "created_at": datetime.utcnow() - timedelta(days=30)
    },
    {
        "id": "pm_2",
        "user_id": "u1",
        "type": PaymentMethodType.PAYPAL,
        "billing_details": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "address": {
                "line1": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "postal_code": "94111",
                "country": "US"
            }
        },
        "card_details": None,
        "is_default": False,
        "created_at": datetime.utcnow() - timedelta(days=15)
    },
    {
        "id": "pm_3",
        "user_id": "u2",
        "type": PaymentMethodType.CREDIT_CARD,
        "billing_details": {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "address": {
                "line1": "456 Market St",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US"
            }
        },
        "card_details": {
            "last4": "1234",
            "brand": "Mastercard",
            "exp_month": 10,
            "exp_year": 2024
        },
        "is_default": True,
        "created_at": datetime.utcnow() - timedelta(days=60)
    }
]

# Mock data for payment intents
MOCK_PAYMENT_INTENTS = [
    {
        "id": "pi_1",
        "user_id": "u1",
        "amount": 100.00,
        "currency": "USD",
        "description": "Payment for booking #12345",
        "metadata": {"booking_id": "12345"},
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": "pm_1",
        "error_message": None,
        "created_at": datetime.utcnow() - timedelta(days=10),
        "updated_at": datetime.utcnow() - timedelta(days=10)
    },
    {
        "id": "pi_2",
        "user_id": "u2",
        "amount": 200.00,
        "currency": "USD",
        "description": "Payment for booking #67890",
        "metadata": {"booking_id": "67890"},
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": "pm_3",
        "error_message": None,
        "created_at": datetime.utcnow() - timedelta(days=5),
        "updated_at": datetime.utcnow() - timedelta(days=5)
    },
    {
        "id": "pi_3",
        "user_id": "u1",
        "amount": 50.00,
        "currency": "USD",
        "description": "Payment for booking #54321",
        "metadata": {"booking_id": "54321"},
        "status": PaymentStatus.FAILED,
        "payment_method_id": "pm_2",
        "error_message": "Insufficient funds",
        "created_at": datetime.utcnow() - timedelta(days=3),
        "updated_at": datetime.utcnow() - timedelta(days=3)
    }
]

# Mock data for refunds
MOCK_REFUNDS = [
    {
        "id": "rf_1",
        "payment_intent_id": "pi_1",
        "amount": 100.00,
        "status": PaymentStatus.SUCCEEDED,
        "reason": "Customer requested",
        "created_at": datetime.utcnow() - timedelta(days=5)
    }
]

# Mock data for transactions
MOCK_TRANSACTIONS = [
    {
        "id": "tx_1",
        "user_id": "u1",
        "type": TransactionType.PAYMENT,
        "amount": 100.00,
        "currency": "USD",
        "description": "Payment for booking #12345",
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": "pm_1",
        "payment_intent_id": "pi_1",
        "refund_id": None,
        "created_at": datetime.utcnow() - timedelta(days=10)
    },
    {
        "id": "tx_2",
        "user_id": "u2",
        "type": TransactionType.PAYMENT,
        "amount": 200.00,
        "currency": "USD",
        "description": "Payment for booking #67890",
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": "pm_3",
        "payment_intent_id": "pi_2",
        "refund_id": None,
        "created_at": datetime.utcnow() - timedelta(days=5)
    },
    {
        "id": "tx_3",
        "user_id": "u1",
        "type": TransactionType.REFUND,
        "amount": 100.00,
        "currency": "USD",
        "description": "Refund for booking #12345",
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": "pm_1",
        "payment_intent_id": "pi_1",
        "refund_id": "rf_1",
        "created_at": datetime.utcnow() - timedelta(days=5)
    },
    {
        "id": "tx_4",
        "user_id": "u1",
        "type": TransactionType.PAYMENT,
        "amount": 50.00,
        "currency": "USD",
        "description": "Payment for booking #54321",
        "status": PaymentStatus.FAILED,
        "payment_method_id": "pm_2",
        "payment_intent_id": "pi_3",
        "refund_id": None,
        "created_at": datetime.utcnow() - timedelta(days=3)
    }
]

# Service functions
async def create_payment_method(payment_method: PaymentMethodCreate) -> PaymentMethodResponse:
    """Create a new payment method for a user."""
    # Generate a new payment method ID
    method_id = f"pm_{len(MOCK_PAYMENT_METHODS) + 1}"
    
    # Create card details if it's a card payment method
    card_details = None
    if payment_method.type in [PaymentMethodType.CREDIT_CARD, PaymentMethodType.DEBIT_CARD]:
        # In a real implementation, we would tokenize the card details
        # and only store the token and last 4 digits
        card_details = {
            "last4": payment_method.card_number[-4:],
            "brand": "Visa",  # In a real implementation, we would determine the brand from the card number
            "exp_month": payment_method.card_exp_month,
            "exp_year": payment_method.card_exp_year
        }
    
    # Check if this is the first payment method for the user
    is_default = True
    for method in MOCK_PAYMENT_METHODS:
        if method["user_id"] == payment_method.user_id:
            is_default = False
            break
    
    # Create the new payment method
    new_method = {
        "id": method_id,
        "user_id": payment_method.user_id,
        "type": payment_method.type,
        "billing_details": payment_method.billing_details,
        "card_details": card_details,
        "is_default": is_default,
        "created_at": datetime.utcnow()
    }
    
    # Add to mock data
    MOCK_PAYMENT_METHODS.append(new_method)
    
    # Convert to response model
    return PaymentMethodResponse(
        id=new_method["id"],
        user_id=new_method["user_id"],
        type=new_method["type"],
        billing_details=new_method["billing_details"],
        card_details=CreditCardInfo(**new_method["card_details"]) if new_method["card_details"] else None,
        is_default=new_method["is_default"],
        created_at=new_method["created_at"]
    )

async def get_payment_methods(user_id: str) -> List[PaymentMethodResponse]:
    """Get all payment methods for a user."""
    # Filter payment methods by user ID
    user_methods = [method for method in MOCK_PAYMENT_METHODS if method["user_id"] == user_id]
    
    # Convert to response models
    result = []
    for method in user_methods:
        result.append(PaymentMethodResponse(
            id=method["id"],
            user_id=method["user_id"],
            type=method["type"],
            billing_details=method["billing_details"],
            card_details=CreditCardInfo(**method["card_details"]) if method["card_details"] else None,
            is_default=method["is_default"],
            created_at=method["created_at"]
        ))
    
    return result

async def delete_payment_method(method_id: str) -> bool:
    """Delete a payment method."""
    # Find the payment method
    for i, method in enumerate(MOCK_PAYMENT_METHODS):
        if method["id"] == method_id:
            # In a real implementation, we would soft delete the payment method
            # Here we just remove it from the mock data
            MOCK_PAYMENT_METHODS.pop(i)
            return True
    
    return False

async def create_payment_intent(payment_intent: PaymentIntentCreate) -> PaymentIntentResponse:
    """Create a new payment intent."""
    # Generate a new payment intent ID
    intent_id = f"pi_{len(MOCK_PAYMENT_INTENTS) + 1}"
    
    # Create the new payment intent
    now = datetime.utcnow()
    new_intent = {
        "id": intent_id,
        "user_id": payment_intent.user_id,
        "amount": payment_intent.amount,
        "currency": payment_intent.currency,
        "description": payment_intent.description,
        "metadata": payment_intent.metadata,
        "status": PaymentStatus.PENDING,
        "payment_method_id": None,
        "error_message": None,
        "created_at": now,
        "updated_at": now
    }
    
    # Add to mock data
    MOCK_PAYMENT_INTENTS.append(new_intent)
    
    # Convert to response model
    return PaymentIntentResponse(**new_intent)

async def get_payment_intent(intent_id: str) -> Optional[PaymentIntentResponse]:
    """Get a payment intent by ID."""
    # Find the payment intent
    for intent in MOCK_PAYMENT_INTENTS:
        if intent["id"] == intent_id:
            return PaymentIntentResponse(**intent)
    
    return None

async def process_payment(intent_id: str, payment_method_id: str) -> PaymentIntentResponse:
    """Process a payment for a payment intent."""
    # Find the payment intent
    intent = None
    for i, pi in enumerate(MOCK_PAYMENT_INTENTS):
        if pi["id"] == intent_id:
            intent = pi
            intent_index = i
            break
    
    if not intent:
        return None
    
    # Find the payment method
    payment_method = None
    for pm in MOCK_PAYMENT_METHODS:
        if pm["id"] == payment_method_id:
            payment_method = pm
            break
    
    if not payment_method:
        # Update intent with error
        intent["status"] = PaymentStatus.FAILED
        intent["error_message"] = "Payment method not found"
        intent["updated_at"] = datetime.utcnow()
        MOCK_PAYMENT_INTENTS[intent_index] = intent
        return PaymentIntentResponse(**intent)
    
    # Simulate payment processing delay
    await asyncio.sleep(1)
    
    # Simulate payment success/failure (90% success rate)
    success = random.random() < 0.9
    
    # Update intent with result
    intent["payment_method_id"] = payment_method_id
    intent["updated_at"] = datetime.utcnow()
    
    if success:
        intent["status"] = PaymentStatus.SUCCEEDED
        
        # Create a transaction record
        transaction_id = f"tx_{len(MOCK_TRANSACTIONS) + 1}"
        transaction = {
            "id": transaction_id,
            "user_id": intent["user_id"],
            "type": TransactionType.PAYMENT,
            "amount": intent["amount"],
            "currency": intent["currency"],
            "description": intent["description"],
            "status": PaymentStatus.SUCCEEDED,
            "payment_method_id": payment_method_id,
            "payment_intent_id": intent_id,
            "refund_id": None,
            "created_at": datetime.utcnow()
        }
        MOCK_TRANSACTIONS.append(transaction)
    else:
        intent["status"] = PaymentStatus.FAILED
        intent["error_message"] = "Payment processing failed"
        
        # Create a failed transaction record
        transaction_id = f"tx_{len(MOCK_TRANSACTIONS) + 1}"
        transaction = {
            "id": transaction_id,
            "user_id": intent["user_id"],
            "type": TransactionType.PAYMENT,
            "amount": intent["amount"],
            "currency": intent["currency"],
            "description": intent["description"],
            "status": PaymentStatus.FAILED,
            "payment_method_id": payment_method_id,
            "payment_intent_id": intent_id,
            "refund_id": None,
            "created_at": datetime.utcnow()
        }
        MOCK_TRANSACTIONS.append(transaction)
    
    # Update the intent in the mock data
    MOCK_PAYMENT_INTENTS[intent_index] = intent
    
    return PaymentIntentResponse(**intent)

async def create_refund(refund_request: RefundRequest) -> RefundResponse:
    """Create a refund for a payment intent."""
    # Find the payment intent
    intent = None
    for i, pi in enumerate(MOCK_PAYMENT_INTENTS):
        if pi["id"] == refund_request.payment_intent_id:
            intent = pi
            intent_index = i
            break
    
    if not intent:
        return None
    
    # Check if the payment was successful
    if intent["status"] != PaymentStatus.SUCCEEDED:
        return None
    
    # Determine refund amount
    refund_amount = refund_request.amount if refund_request.amount else intent["amount"]
    
    # Create the refund
    refund_id = f"rf_{len(MOCK_REFUNDS) + 1}"
    refund = {
        "id": refund_id,
        "payment_intent_id": refund_request.payment_intent_id,
        "amount": refund_amount,
        "status": PaymentStatus.SUCCEEDED,
        "reason": refund_request.reason,
        "created_at": datetime.utcnow()
    }
    
    # Add to mock data
    MOCK_REFUNDS.append(refund)
    
    # Update the payment intent status
    if refund_amount == intent["amount"]:
        intent["status"] = PaymentStatus.REFUNDED
    else:
        intent["status"] = PaymentStatus.PARTIALLY_REFUNDED
    
    intent["updated_at"] = datetime.utcnow()
    MOCK_PAYMENT_INTENTS[intent_index] = intent
    
    # Create a transaction record for the refund
    transaction_id = f"tx_{len(MOCK_TRANSACTIONS) + 1}"
    transaction = {
        "id": transaction_id,
        "user_id": intent["user_id"],
        "type": TransactionType.REFUND,
        "amount": refund_amount,
        "currency": intent["currency"],
        "description": f"Refund for {intent['description']}",
        "status": PaymentStatus.SUCCEEDED,
        "payment_method_id": intent["payment_method_id"],
        "payment_intent_id": intent["id"],
        "refund_id": refund_id,
        "created_at": datetime.utcnow()
    }
    MOCK_TRANSACTIONS.append(transaction)
    
    # Convert to response model
    return RefundResponse(**refund)

async def get_transactions(
    user_id: str,
    transaction_type: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[TransactionResponse]:
    """Get transaction history for a user."""
    # Filter transactions by user ID and type
    filtered_transactions = [tx for tx in MOCK_TRANSACTIONS if tx["user_id"] == user_id]
    
    if transaction_type:
        filtered_transactions = [tx for tx in filtered_transactions if tx["type"].value == transaction_type]
    
    # Sort by date (newest first)
    filtered_transactions.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Apply pagination
    paginated_transactions = filtered_transactions[offset:offset + limit]
    
    # Convert to response models
    result = []
    for tx in paginated_transactions:
        result.append(TransactionResponse(**tx))
    
    return result
