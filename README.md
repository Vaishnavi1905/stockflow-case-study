## Issues:
1.	No input validation:
    The code access field like data[‘name’] without checking .
2.	SKU is not checked for uniqueness :
    SKU can be added many times.
3.	Two database commits:
    Product and inventory are saved separately.
4.	No transaction handling:
    If any of the step fails then other still saves.
5.	No error handling:
    System may crash if something goes wrong.
6.	No validation for price and value:
    It can store negative and wrong values.
7.	Optional fields not handled:
    Initial_quantity may not be present.
8.	Product linked to one warehouse:
    But requirement says multiple warehouse.

## Impacts:
•	Application may crash if data is missing.
•	Duplicate SKUs can create confusion.
•	Data may become inconsistent (product without inventory).
•	Wrong price can affect business calculations.
•	System becomes unreliable without error handling.
•	Not suitable for real-world scaling.

## Fixes and Improvements
I fixed these problems by:
•	Checking required fields before using them
•	Making sure SKU is unique
•	Saving product and inventory together (single commit)
•	Adding error handling to avoid crashes
•	Handling optional fields safely
•	Validating price and quantity

## Assumptions
  SKU must be unique
  Price >= 0
  Quantity optional