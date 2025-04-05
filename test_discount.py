import unittest
from typing import List, Dict

from discount_logic import calculate_total_price,validate_items, validate_campaigns, apply_coupon, apply_on_top, apply_seasonal, apply_discounts

class TestDiscountModule(unittest.TestCase):

    def test_calculate_total_price(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"},
            {"name": "Belt", "price": 230, "category": "Accessories"}
        ]
        total = calculate_total_price(items)
        self.assertEqual(total, 830)

    def test_validate_items(self):
        valid_items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"}
        ]
        invalid_items = [
            {"name": "T-Shirt", "category": "Clothing"},  # Missing price
            {"price": 250, "category": "Accessories"}  # Missing name
        ]
        self.assertTrue(validate_items(valid_items))
        self.assertFalse(validate_items(invalid_items))

    def test_validate_campaigns(self):
        valid_campaigns = [
            {"category": "Coupon", "type": "Fixed", "amount": 50},
            {"category": "On Top", "type": "Point", "points": 68},
            {"category": "Seasonal", "type": "Seasonal", "every": 300, "discount": 40}
        ]
        invalid_campaigns = [
            {"category": "Coupon", "type": "Fixed"},  # Missing amount
            {"category": "On Top", "type": "Point"},  # Missing points
            {"category": "Seasonal", "type": "Seasonal"}  # Missing every and discount
        ]
        self.assertTrue(validate_campaigns(valid_campaigns))
        self.assertFalse(validate_campaigns(invalid_campaigns))

    def test_apply_fix_coupon(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"}
        ]
        total = calculate_total_price(items)
        coupon_discount = {"category": "Coupon", "type": "Fixed", "amount": 50}
        new_total, details = apply_coupon(coupon_discount, total)
        self.assertEqual(new_total, 550)
        self.assertEqual(details, "Coupon - Fixed Amount: -50 THB")
    
    def test_apply_percentage_coupon(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"}
        ]
        campaigns = [
            {"category": "Coupon", "type": "Percentage", "percentage": 10}
        ]
        
        data = {"items": items, "campaigns": campaigns}
        
        result = apply_discounts(data)
        
        expected_price = 540  # 350 + 250 = 600, ลด 10% จะได้ 540
        self.assertEqual(result["final_price"], expected_price)
        self.assertIn("Coupon - 10% off", result["discount_details"])

    def test_apply_percentage_category_on_top(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hoodie", "price": 700, "category": "Clothing"},
            {"name": "Watch", "price": 850, "category": "Accessories"},
            {"name": "Bag", "price": 640, "category": "Accessories"}
        ]
        campaigns = [
            {
                "category": "On Top",
                "type": "CategoryPercentage",
                "product_category": "Clothing",
                "percentage": 15
            }
        ]
        data = {"items": items, "campaigns": campaigns}

        result = apply_discounts(data)

        clothing_total = 350 + 700
        discount = clothing_total * 0.15  # 157.5
        expected_price = 350 + 700 + 850 + 640 - discount  # = 2540 - 157.5 = 2382.5

        self.assertEqual(result["final_price"], 2382.5)
        self.assertIn("On Top - 15% off on Clothing", result["discount_details"])


    def test_apply_point_on_top(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"},
            {"name": "Belt", "price": 230, "category": "Accessories"}
        ]
        total = calculate_total_price(items)
        on_top_discount = {"category": "On Top", "type": "Point", "points": 68}
        new_total, details = apply_on_top(on_top_discount, items, total)
        self.assertEqual(new_total, 762)
        self.assertEqual(details, "On Top - Points Discount: -68 THB")

    def test_apply_seasonal(self):
        items = [
            {"name": "T-Shirt", "price": 350, "category": "Clothing"},
            {"name": "Hat", "price": 250, "category": "Accessories"},
            {"name": "Belt", "price": 230, "category": "Accessories"}
        ]
        total = calculate_total_price(items)
        seasonal_discount = {"category": "Seasonal", "type": "Seasonal", "every": 300, "discount": 40}
        new_total, details = apply_seasonal(seasonal_discount, total)
        self.assertEqual(new_total, 750)
        self.assertEqual(details, "Seasonal - Discount of 40 THB every 300 THB spent")

    def test_apply_discounts(self):
        data = {
            "items": [
                {"name": "T-Shirt", "price": 350, "category": "Clothing"},
                {"name": "Hat", "price": 250, "category": "Accessories"},
                {"name": "Belt", "price": 230, "category": "Accessories"}
            ],
            "campaigns": [
                {"category": "Coupon", "type": "Fixed", "amount": 50},
                {"category": "On Top", "type": "Point", "points": 68},
                {"category": "Seasonal", "type": "Seasonal", "every": 300, "discount": 40}
            ]
        }
        result = apply_discounts(data)
        self.assertEqual(result["final_price"], 632)
        self.assertIn("Coupon - Fixed Amount: -50 THB", result["discount_details"])
        self.assertIn("On Top - Points Discount: -68 THB", result["discount_details"])
        self.assertIn("Seasonal - Discount of 40 THB every 300 THB spent", result["discount_details"])

    def test_invalid_campaign_data(self):
        data = {
            "items": [
                {"name": "T-Shirt", "price": 350, "category": "Clothing"},
                {"name": "Hat", "price": 250, "category": "Accessories"}
            ],
            "campaigns": [
                {"category": "Coupon", "type": "Fixed"},  # Invalid campaign
                {"category": "On Top", "type": "Point", "points": 68}
            ]
        }
        result = apply_discounts(data)
        self.assertEqual(result, {"error": "Invalid campaign data"})

if __name__ == "__main__":
    unittest.main()