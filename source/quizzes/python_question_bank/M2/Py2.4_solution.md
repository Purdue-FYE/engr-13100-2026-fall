## Py2.4 (Two Parts) - Solutions

(a) Use the Python code to fill in 3 blanks in the sample input/output:

### Editor - checkout.py
```python
# --- Checkout at a membership warehouse club ---
membership = input("Membership (Gold, Silver, Guest): ").strip().lower()
cart_total = float(input("Cart total (e.g., 72.50): "))
items = float(input("Number of items (e.g., 3): "))

if membership in {"gold", "silver"}:
    print("Member Checkout.")
    if cart_total >= 100:
        print("Free express shipping + member discount.")
    elif 50 <= cart_total < 100:
        if membership == "gold" or items >= 4:
            print("Free standard shipping; small member discount applied.")
        else:
            print("Standard shipping; member discount applied.")
    else:
        print("Shipping applies; consider adding more items for perks.")
elif membership == "guest":
    print("Guest checkout.")
    if cart_total >= 100 and items >= 2:
        print("Free standard shipping for large guest order.")
    elif cart_total < 30 or items == 1:
        print("Shipping fee applies; sign up for perks.")
    else:
        print("Standard shipping; consider joining for discounts.")
else:
    print("Invalid input. Enter a membership option.")
```

### Program Description

This script simulates checkout logic for a membership warehouse club by asking the user for their membership level (Gold, Silver, or Guest), the cart total, and the number of items, then printing shipping/discount outcomes based on those inputs. For Gold/Silver members, it announces “Member Checkout” and: (1) if the cart total is at least 100, grants free express shipping plus a member discount; (2) if the cart total is between 50 and 99.99, it gives free standard shipping with a small discount if the user is Gold or has 4+ items, otherwise standard shipping with a member discount; (3) if the cart total is under 50, shipping fees apply with a nudge to add more items. For Guests, it announces “Guest checkout” and: (1) if the cart total is at least 100 and there are 2+ items, it grants free standard shipping; (2) if the cart total is under 30 or there’s only 1 item, a shipping fee applies with a prompt to sign up; (3) otherwise, standard shipping is applied, and it suggests joining for discounts.

### Terminal

    # Sample input/ouput 1
    $ python checkout.py
    Membership (Gold, Silver, Guest): Gold
    Cart total (e.g., 72.50): 85.75
    Number of items (e.g., 3): 2
    Member checkout.
    Free standard shipping; small member discount applied.

    # Sample input/ouput 2
    $ python checkout.py
    Membership (Gold, Silver, Guest): silver
    Cart total (e.g., 72.50): 55.45
    Number of items (e.g., 3): 3
    Member checkout.
    Standard shipping; member discount applied.

    # Sample input/ouput 3
    $ python checkout.py
    Membership (Gold, Silver, Guest): Guest
    Cart total (e.g., 72.50): 110
    Number of items (e.g., 3): 2
    Guest checkout.
    Free standard shipping for large guest order.

    # Sample input/ouput 4
    $ python checkout.py
    Membership (Gold, Silver, Guest): Platinum
    Cart total (e.g., 72.50): 140.32
    Number of items (e.g., 3): 6
    Invalid input. Enter a membership option.


(b) Are there any inputs that would cause check.py to raise an error? If so, indicate the error type and include an example of an input that would result in this error.

Yes, checkout.py will throw a TypeError if the user inputs a string (e.g., "ten") instead of a number for either cart total or number of items.
