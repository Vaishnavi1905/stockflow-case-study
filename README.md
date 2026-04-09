## Inventory Management System for B2B SaaS

# Task 1: Code Review & Debugging 
## Issues:
- No input validation:
    The code access field like data[‘name’] without checking .
- SKU is not checked for uniqueness :
    SKU can be added many times.
- Two database commits:
    Product and inventory are saved separately.
- No transaction handling:
    If any of the step fails then other still saves.
- No error handling:
    System may crash if something goes wrong.
-  No validation for price and value:
    It can store negative and wrong values.
-  Optional fields not handled:
    Initial_quantity may not be present.
 -  roduct linked to one warehouse:
    But requirement says multiple warehouse.
    

## Impacts:
-	Application may crash if data is missing.
-	Duplicate SKUs can create confusion.
-	Data may become inconsistent (product without inventory).
-	The wrong price can affect business calculations.
-	System becomes unreliable without error handling.
-	Not suitable for real-world scaling.

## Fixes and Improvements
I fixed these problems by:
-	Checking required fields before using them
-	Making sure SKU is unique
-	Saving product and inventory together (single commit)
-	Adding error handling to avoid crashes
-	Handling optional fields safely
-	Validating price and quantity
- Used transaction to ensure data consistency and avoid partial data saving
  
## Assumptions
-	 SKU must be unique
-	Price >= 0
-	Quantity optional

---


# Task 2: Database Design

## 1. Schema Design

Tables:

- Companies (id, name)
- Warehouses (id, name, location, company_id)
- Products (id, name, sku, price)
- Inventory (id, product_id, warehouse_id, quantity)
- Inventory_History (id, product_id, warehouse_id, change_quantity, timestamp)
- Suppliers (id, name)
- Supplier_Products (supplier_id, product_id)
- Product_Bundles (bundle_product_id, child_product_id, quantity)
- Product is linked to company for multi-tenant support



## 2. Identify Gaps

- Is SKU unique globally or per company?
- Can a product have multiple suppliers?
- Can bundles contain other bundles?
- Can a product exist without inventory?
- What happens if warehouse_id is invalid?



##  3. Explanation of Decisions

- Separate Inventory table to support multiple warehouses  
- Inventory_History to track stock changes  
- Many-to-many relationship handled using Supplier_Products  
- Product_Bundles used to support bundle products
- Product is linked to company to support multi-tenant system 
- Foreign keys used to maintain data consistency

---

# Task 3: Low Stock Alerts API

## 1. Implementation (Approach)

- Get all warehouses for the given company_id  
- For each warehouse, fetch inventory records  
- For each product in inventory:
  - Check if current stock is below threshold  
  - Check if product has recent sales  
- If both conditions are true:
  - Fetch supplier details  
  - Add product info to alerts list  
- Return alerts list with total count  


##  2. Edge Cases

- Company has no warehouses  
- Product has no supplier  
- Inventory record missing  
- Threshold not defined for product  
- No recent sales data available  



##  3. Explanation of Approach

- Used warehouse → inventory → product flow to get data  
- Applied business rules (low stock + recent sales)  
- Included supplier info for reordering  
- Designed response to match required format

 ## Assumptions

- Threshold is fixed (e.g., 20)
- Recent sales means last 30 days
- Each product has at least one supplier
- Days until stockout is estimated






