import sys
from product_advisor import ProductAdvisorClient

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("=== Conversational Product Advisor Example ===")
    
    # Initialize client in mock mode
    client = ProductAdvisorClient()
    
    # 1. Setup an initial hardware cart configuration
    cart = [
        {
            "sku": "CPU-INT-I9",
            "name": "Intel Core i9-13900K",
            "price": 560.00,
            "specs": {"socket": "LGA1700", "wattage": "125W"}
        }
    ]
    preferences = {
        "max_budget": 1000.00,
        "required_specs": {"form_factor": "ATX"}
    }
    
    print("\n--- Step 1: Checking Compatibility of New Item (Incompatible Socket) ---")
    incompatible_motherboard = {
        "sku": "MB-AMD-X670",
        "name": "ASUS TUF Gaming X670E-Plus",
        "price": 280.00,
        "specs": {"socket": "AM5", "form_factor": "ATX"}
    }
    
    compat_check_1 = client.check_compatibility(cart, incompatible_motherboard)
    print(f"Is Compatible: {compat_check_1['is_compatible']}")
    for warning in compat_check_1["warnings"]:
        print(f"  Warning: {warning}")

    print("\n--- Step 2: Checking Compatibility of New Item (Compatible Socket) ---")
    compatible_motherboard = {
        "sku": "MB-ROG-Z790",
        "name": "ASUS ROG Strix Z790-F",
        "price": 370.00,
        "specs": {"socket": "LGA1700", "form_factor": "ATX"}
    }
    
    compat_check_2 = client.check_compatibility(cart, compatible_motherboard)
    print(f"Is Compatible: {compat_check_2['is_compatible']}")
    if not compat_check_2["warnings"]:
        print("  No warnings found. Items are compatible.")

    # 3. Dialogue flow
    print("\n--- Step 3: Simulating Conversational Chat Flow ---")
    dialogue = [
        {"sender": "user", "text": "I need a motherboard for this build."}
    ]
    step_1 = client.get_advisor_response(dialogue, cart, preferences)
    print(f"User: {dialogue[0]['text']}")
    print(f"Advisor: {step_1['advisor_response']}")
    
    dialogue.append({"sender": "advisor", "text": step_1['advisor_response']})
    dialogue.append({"sender": "user", "text": "Yes, please add the Strix Z790 to my cart."})
    
    step_2 = client.get_advisor_response(dialogue, cart, preferences)
    print(f"\nUser: {dialogue[-1]['text']}")
    print(f"Advisor: {step_2['advisor_response']}")
    print(f"Cart Updates: {step_2['cart_updates']}")

if __name__ == "__main__":
    main()
