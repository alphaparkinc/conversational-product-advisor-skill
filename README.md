# conversational-product-advisor-skill

> **GenPark AI Agent Skill** -- # Conversational Product Advisor Skill

This repository contains the **Conversational Product Advisor Skill** — an agentic shopping assistant interface configuration (`skill.json`), developer SDK client (`product_advisor.py`), and validation script for running conversational product searches and technical compatibility checks.

---

## 🚀 Capabilities

* **Compatibility Check Engine:** Verifies technical constraints (e.g. computer component socket matches, size configurations) before items are added to a cart.
* **Diagnose User Preferences:** Converses with customers to narrow down specifications, sizes, and colors when user inputs are too vague.
* **Budget Safeguards:** Computes cart values dynamically against user limits and offers cheaper alternative configurations when limits are breached.

---

## 🛠️ Setup & Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configuration:
   Set your API environment variables if executing requests against the live production server (otherwise, client executes in mock mode):
   * **PowerShell**:
     ```powershell
     $env:ADVISOR_API_KEY="your_api_key"
     ```
   * **bash**:
     ```bash
     export ADVISOR_API_KEY="your_api_key"
     ```

---

## 💻 SDK Usage Reference

```python
from product_advisor import ProductAdvisorClient

# Initialize Client (mock mode by default)
client = ProductAdvisorClient()

# Check compatibility between cart items and a candidate item
compat = client.check_compatibility(
    cart_items=[{"name": "i9 CPU", "specs": {"socket": "LGA1700"}}],
    new_item={"name": "AMD Motherboard", "specs": {"socket": "AM5"}}
)
print(f"Is Compatible: {compat['is_compatible']}")
print(f"Warnings: {compat['warnings']}")

# Process shopping chat message
response = client.get_advisor_response(
    dialog_history=[{"sender": "user", "text": "I need a motherboard."}],
    cart=[{"name": "i9 CPU"}],
    preferences={"max_budget": 1000.00}
)
print(response["advisor_response"])
print(response["cart_updates"])
```

---

## 📜 License
This project is licensed under the MIT License.