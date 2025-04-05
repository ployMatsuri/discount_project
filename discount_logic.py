from typing import List, Dict

CATEGORY_ORDER = ['Coupon', 'On Top', 'Seasonal']

def calculate_total_price(items: List[Dict]) -> float:
    return sum(item["price"] for item in items)

def validate_items(items: List[Dict]) -> bool:
    for item in items:
        if "name" not in item or "price" not in item or "category" not in item:
            return False
        if not isinstance(item["price"], (int, float)) or item["price"] < 0:
            return False
    return True

def validate_campaigns(campaigns: List[Dict]) -> bool:
    for campaign in campaigns:
        if "category" not in campaign or "type" not in campaign:
            return False
        if campaign["category"] not in CATEGORY_ORDER:
            return False
        if campaign["type"] == "Fixed" and "amount" not in campaign:
            return False
        if campaign["type"] == "Percentage" and "percentage" not in campaign:
            return False
        if campaign["type"] == "CategoryPercentage" and ("category" not in campaign or "percentage" not in campaign):
            return False
        if campaign["type"] == "Point" and "points" not in campaign:
            return False
        if campaign["type"] == "Seasonal" and ("every" not in campaign or "discount" not in campaign):
            return False
    return True

def apply_coupon(discount, total):
    if discount["type"] == "Fixed":
        new_total = max(0, total - discount["amount"])
        return new_total, f"Coupon - Fixed Amount: -{discount['amount']} THB"
    elif discount["type"] == "Percentage":
        new_total = total * (1 - discount["percentage"] / 100)
        return new_total, f"Coupon - {discount['percentage']}% off"
    return total, "No Coupon"

def apply_on_top(discount, items, total):
    if discount["type"] == "CategoryPercentage":
        category = discount.get("product_category") or discount.get("category")
        percentage = discount["percentage"]
        discount_amount = sum(item["price"] * percentage / 100 for item in items if item["category"] == category)
        new_total = total - discount_amount
        return new_total, f"On Top - {percentage}% off on {category}"
    elif discount["type"] == "Point":
        max_discount = total * 0.2
        applied = min(discount["points"], max_discount)
        new_total = total - applied
        return new_total, f"On Top - Points Discount: -{applied} THB"
    return total, "No On Top Discount"

def apply_seasonal(discount, total):
    x = discount["every"]
    y = discount["discount"]
    discount_amount = int(total // x) * y
    new_total = total - discount_amount
    return new_total, f"Seasonal - Discount of {y} THB every {x} THB spent"

def apply_discounts(data: Dict) -> Dict:
    items = data["items"]
    campaigns = data["campaigns"]

    if not validate_items(items):
        return {"error": "Invalid item data in the cart"}
    
    if not validate_campaigns(campaigns):
        return {"error": "Invalid campaign data"}

    total = calculate_total_price(items)
    discount_details = []

    for category in CATEGORY_ORDER:
        campaign = next((c for c in campaigns if c["category"] == category), None)
        if campaign:
            print(f"Applying campaign: {campaign}")  # Debugging line
            if category == "Coupon":
                total, details = apply_coupon(campaign, total)
                discount_details.append(details)
            elif category == "On Top":
                total, details = apply_on_top(campaign, items, total)
                discount_details.append(details)
            elif category == "Seasonal":
                total, details = apply_seasonal(campaign, total)
                discount_details.append(details)

    return {
        "final_price": round(total, 2),
        "discount_details": discount_details
    }
