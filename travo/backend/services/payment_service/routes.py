from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import List, Optional

# Import schemas and service logic
from .schemas import (
    PaymentMethodCreate, 
    PaymentMethodResponse, 
    PaymentIntentCreate, 
    PaymentIntentResponse,
    PaymentStatus,
    RefundRequest,
    RefundResponse,
    TransactionResponse
)
from .service_logic import (
    create_payment_method, 
    get_payment_methods, 
    delete_payment_method,
    create_payment_intent,
    get_payment_intent,
    process_payment,
    create_refund,
    get_transactions
)

# Create router
router = APIRouter()

# Test route
@router.get("/test")
async def test_payment_service():
    return {"status": "ok", "service": "payment_service"}

# Create a payment method
@router.post("/methods", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
async def add_payment_method(payment_method: PaymentMethodCreate):
    result = await create_payment_method(payment_method)
    return result

# Get payment methods for a user
@router.get("/methods", response_model=List[PaymentMethodResponse])
async def list_payment_methods(user_id: str):
    methods = await get_payment_methods(user_id)
    return methods

# Delete a payment method
@router.delete("/methods/{method_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_payment_method(method_id: str):
    success = await delete_payment_method(method_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    return None

# Create a payment intent
@router.post("/intents", response_model=PaymentIntentResponse, status_code=status.HTTP_201_CREATED)
async def create_intent(payment_intent: PaymentIntentCreate):
    result = await create_payment_intent(payment_intent)
    return result

# Get a payment intent
@router.get("/intents/{intent_id}", response_model=PaymentIntentResponse)
async def get_intent(intent_id: str):
    intent = await get_payment_intent(intent_id)
    if not intent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment intent not found"
        )
    return intent

# Process a payment
@router.post("/intents/{intent_id}/process", response_model=PaymentIntentResponse)
async def process_intent_payment(
    intent_id: str, 
    payment_method_id: str,
    background_tasks: BackgroundTasks
):
    # Get the payment intent
    intent = await get_payment_intent(intent_id)
    if not intent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment intent not found"
        )
    
    # Check if already processed
    if intent.status == PaymentStatus.SUCCEEDED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment has already been processed"
        )
    
    # Process the payment (in background for async processing)
    background_tasks.add_task(process_payment, intent_id, payment_method_id)
    
    # Return the updated intent (will be in processing state)
    intent.status = PaymentStatus.PROCESSING
    return intent

# Create a refund
@router.post("/refunds", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
async def request_refund(refund_request: RefundRequest):
    refund = await create_refund(refund_request)
    return refund

# Get transaction history
@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transaction_history(
    user_id: str,
    transaction_type: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
):
    transactions = await get_transactions(user_id, transaction_type, limit, offset)
    return transactions
