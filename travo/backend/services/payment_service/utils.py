import uuid
import re
import hashlib
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
import random

# Credit card validation patterns
CARD_PATTERNS = {
    "visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
    "mastercard": r"^5[1-5][0-9]{14}$",
    "amex": r"^3[47][0-9]{13}$",
    "discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$"
}

def generate_payment_method_id() -> str:
    """Generate a unique ID for a payment method."""
    return f"pm_{uuid.uuid4().hex[:8]}"

def generate_payment_intent_id() -> str:
    """Generate a unique ID for a payment intent."""
    return f"pi_{uuid.uuid4().hex[:8]}"

def generate_refund_id() -> str:
    """Generate a unique ID for a refund."""
    return f"rf_{uuid.uuid4().hex[:8]}"

def generate_transaction_id() -> str:
    """Generate a unique ID for a transaction."""
    return f"tx_{uuid.uuid4().hex[:8]}"

def validate_credit_card(card_number: str) -> Tuple[bool, Optional[str]]:
    """Validate a credit card number and return its type."""
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)
    
    # Check if it's a valid number (Luhn algorithm)
    if not is_luhn_valid(card_number):
        return False, None
    
    # Determine card type
    for card_type, pattern in CARD_PATTERNS.items():
        if re.match(pattern, card_number):
            return True, card_type
    
    return False, None

def is_luhn_valid(card_number: str) -> bool:
    """Validate a card number using the Luhn algorithm."""
    # Remove non-digits
    digits = re.sub(r'\D', '', card_number)
    
    # Check if it's all digits and not empty
    if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
        return False
    
    # Luhn algorithm
    sum_digits = 0
    num_digits = len(digits)
    odd_even = num_digits & 1
    
    for i in range(num_digits):
        digit = int(digits[i])
        if ((i & 1) ^ odd_even) == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_digits += digit
    
    return (sum_digits % 10) == 0

def mask_card_number(card_number: str) -> str:
    """Mask a credit card number for display."""
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)
    
    # Keep only the last 4 digits
    masked = "*" * (len(card_number) - 4) + card_number[-4:]
    
    # Format with spaces for readability
    if len(masked) == 16:  # Most common length
        return f"{masked[:4]} {masked[4:8]} {masked[8:12]} {masked[12:]}"
    else:
        return masked

def validate_expiry_date(exp_month: int, exp_year: int) -> bool:
    """Validate that a card expiry date is in the future."""
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # Check if the expiry date is valid
    if exp_year < current_year:
        return False
    elif exp_year == current_year and exp_month < current_month:
        return False
    elif exp_month < 1 or exp_month > 12:
        return False
    
    return True

def calculate_transaction_stats(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate statistics for a list of transactions."""
    if not transactions:
        return {
            "total_count": 0,
            "total_amount": 0,
            "average_amount": 0,
            "success_rate": 0,
            "currency_breakdown": {}
        }
    
    total_count = len(transactions)
    total_amount = sum(tx["amount"] for tx in transactions)
    average_amount = total_amount / total_count if total_count > 0 else 0
    
    # Count successful transactions
    successful = sum(1 for tx in transactions if tx["status"].value == "succeeded")
    success_rate = (successful / total_count) * 100 if total_count > 0 else 0
    
    # Group by currency
    currency_breakdown = {}
    for tx in transactions:
        currency = tx["currency"]
        if currency not in currency_breakdown:
            currency_breakdown[currency] = {
                "count": 0,
                "total_amount": 0
            }
        
        currency_breakdown[currency]["count"] += 1
        currency_breakdown[currency]["total_amount"] += tx["amount"]
    
    return {
        "total_count": total_count,
        "total_amount": total_amount,
        "average_amount": average_amount,
        "success_rate": success_rate,
        "currency_breakdown": currency_breakdown
    }

def sanitize_payment_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize payment data to prevent injection attacks."""
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remove any potentially dangerous characters
            sanitized[key] = re.sub(r'[<>"\\]', '', value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_payment_data(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_payment_data(item) if isinstance(item, dict) else item for item in value]
        else:
            sanitized[key] = value
    
    return sanitized

def generate_receipt_number() -> str:
    """Generate a unique receipt number."""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    random_suffix = random.randint(1000, 9999)
    return f"REC-{timestamp}-{random_suffix}"

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a currency amount for display."""
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    # Format with 2 decimal places, except for JPY
    if currency == "JPY":
        return f"{symbol}{int(amount):,}"
    else:
        return f"{symbol}{amount:,.2f}"

def calculate_refund_amount(original_amount: float, refund_percentage: float) -> float:
    """Calculate refund amount based on percentage."""
    if refund_percentage <= 0 or refund_percentage > 100:
        raise ValueError("Refund percentage must be between 0 and 100")
    
    return round(original_amount * (refund_percentage / 100), 2)

def is_valid_payment_amount(amount: float, currency: str) -> bool:
    """Validate payment amount based on currency."""
    # Different currencies have different minimum amounts
    min_amounts = {
        "USD": 0.50,
        "EUR": 0.50,
        "GBP": 0.30,
        "JPY": 50
    }
    
    min_amount = min_amounts.get(currency, 0.50)
    
    return amount >= min_amount
