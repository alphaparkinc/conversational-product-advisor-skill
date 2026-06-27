import os
import requests
from typing import List, Dict, Any, Optional

class ProductAdvisorError(Exception):
    """Base exception class for Conversational Product Advisor Client."""
    pass

class ProductAdvisorClient:
    """
    Client for driving conversational e-commerce product advice and checking technical compatibility.
    Supports a mock mode for local testing.
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.conversational-advisor.ai/v1"):
        self.api_key = api_key or os.environ.get("ADVISOR_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.mock_mode = self.api_key is None or self.api_key == "mock"
        
        if self.mock_mode:
            print("[ProductAdvisorClient] API Key not set. Running in MOCK Mode.")

    def check_compatibility(self, cart_items: List[Dict[str, Any]], new_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate technical or structural compatibility between cart items and a candidate item.
        """
        if self.mock_mode:
            is_compatible = True
            warnings = []
            
            # Simple rule-based hardware simulator
            new_specs = new_item.get("specs", {})
            new_socket = new_specs.get("socket") or new_specs.get("compatibility_key")
            
            for item in cart_items:
                item_specs = item.get("specs", {})
                item_socket = item_specs.get("socket") or item_specs.get("compatibility_key")
                
                # If both have sockets/compatibility keys, they must match
                if new_socket and item_socket and new_socket.lower() != item_socket.lower():
                    is_compatible = False
                    warnings.append(
                        f"Incompatibility detected: '{new_item['name']}' requires socket {new_socket}, "
                        f"but your cart contains '{item['name']}' which uses socket {item_socket}."
                    )
            
            return {
                "is_compatible": is_compatible,
                "warnings": warnings
            }

        # Remote API integration call
        payload = {"cart": cart_items, "new_item": new_item}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(f"{self.base_url}/verify-compatibility", json=payload, headers=headers, timeout=30)
            return resp.json()
        except Exception as e:
            raise ProductAdvisorError(f"API Compatibility check failed: {e}")

    def get_advisor_response(
        self,
        dialog_history: List[Dict[str, str]],
        cart: List[Dict[str, Any]],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processes conversational messages and determines recommendations, cart additions, or compatibility warnings.
        """
        if self.mock_mode:
            last_message = dialog_history[-1]["text"].lower() if dialog_history else ""
            max_budget = preferences.get("max_budget", 9999.00)
            
            # Compute current cart total
            cart_total = sum(i["price"] for i in cart)
            
            add_skus = []
            remove_skus = []
            
            # Simple heuristic conversation states
            if "motherboard" in last_message:
                response = (
                    "I see you are looking for a motherboard. Since you have an Intel i9 CPU in your cart "
                    "(Socket LGA1700), I highly recommend the ASUS ROG Strix Z790 motherboard. It matches "
                    "your processor socket and fits your budget. Shall I add it to your cart?"
                )
            elif "yes" in last_message or "add" in last_message:
                response = "Perfect! I have added the ASUS ROG Strix Z790 motherboard to your cart and verified compatibility."
                add_skus.append("MB-ROG-Z790")
            elif "price" in last_message or "cheaper" in last_message:
                response = (
                    "No problem, let's fit your budget. I suggest the MSI PRO Z790-P as a cost-effective alternative. "
                    "It will save you $120 while keeping full compatibility."
                )
            else:
                response = "Hello! I am your AI Shopping Companion. How can I help you configure your build today?"

            return {
                "advisor_response": response,
                "cart_updates": {
                    "add": add_skus,
                    "remove": remove_skus
                },
                "estimated_cart_total": round(cart_total, 2)
            }

        payload = {"dialog_history": dialog_history, "cart": cart, "preferences": preferences}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            resp = requests.post(f"{self.base_url}/dialog", json=payload, headers=headers, timeout=30)
            return resp.json()
        except Exception as e:
            raise ProductAdvisorError(f"API Dialog processing failed: {e}")
