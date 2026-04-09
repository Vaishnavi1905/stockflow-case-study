# Inventory Management System for B2B SaaS

---

## Task 1: Code Review & Debugging

### Issues
- No input validation: The code accesses fields like `data['name']` without checking.
- SKU is not checked for uniqueness: Duplicate SKUs can be created.
- Two database commits: Product and inventory are saved separately.
- No transaction handling: If one step fails, the other may still be saved.
- No error handling: System may crash if something goes wrong.
- No validation for price and quantity: Negative or invalid values can be stored.
- Optional fields not handled: `initial_quantity` may be missing.
- Product linked to one warehouse: Requirement states multiple warehouses.

---

### Impact
- Application may crash if required data is missing.
- Duplicate SKUs can create confusion.
- Data inconsistency (product without inventory).
- Incorrect price affects business calculations.
- System becomes unreliable without proper error handling.
- Not suitable for real-world scalability.

---

### Fixes and Improvements
- Checked required fields before using them
- Ensured SKU uniqueness
- Used a single commit to save product and inventory together
- Added error handling to prevent crashes
- Handled optional fields safely
- Validated price and quantity
- Used transactions to ensure data consistency and avoid partial data saving

👉 Code implementation is provided in `app.py`

---

### Assumptions
- SKU must be unique
- Price must be greater than or equal to 0
- Quantity is optional

---

## Task 2: Database Design

### 1. Schema Design

Tables:
- Companies (id, name)
- Warehouses (id, name, location, company_id)
- Products (id, name, sku, price)
- Inventory (id, product_id, warehouse_id, quantity)
- Inventory_History (id, product_id, warehouse_id, change_quantity, timestamp)
- Suppliers (id, name)
- Supplier_Products (supplier_id, product_id)
- Product_Bundles (bundle_product_id, child_product_id, quantity)

- Product is linked to company to support multi-tenant systems

---

### 2. Identify Gaps
- Is SKU unique globally or per company?
- Can a product have multiple suppliers?
- Can bundles contain other bundles?
- Can a product exist without inventory?
- What happens if warehouse_id is invalid?

---

### 3. Explanation of Decisions
- Used separate Inventory table to support multiple warehouses
- Inventory_History tracks stock changes
- Many-to-many relationship handled using Supplier_Products
- Product_Bundles supports bundle products
- Product linked to company for multi-tenant support
- Foreign keys ensure data consistency

---

## Task 3: Low Stock Alerts API

### 1. Implementation (Approach)
- Get all warehouses for the given company_id
- For each warehouse, fetch inventory records
- For each product in inventory:
  - Check if current stock is below threshold
  - Check if product has recent sales
- If both conditions are true:
  - Fetch supplier details
  - Add product info to alerts list
- Return alerts list with total count

---

### 2. Edge Cases
- Company has no warehouses
- Product has no supplier
- Inventory record missing
- Threshold not defined
- No recent sales data available

---

### 3. Explanation of Approach
- Used warehouse → inventory → product flow
- Applied business rules (low stock + recent sales)
- Included supplier information for reordering
- Designed response as per required format

---

### Assumptions
- Threshold is fixed (e.g., 20)
- Recent sales means last 30 days
- Each product has at least one supplier
- Days until stockout is estimated
