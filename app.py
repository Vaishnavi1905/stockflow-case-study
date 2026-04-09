from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.json

        
        required_fields = ['name', 'sku', 'price', 'warehouse_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        
        if data['price'] < 0:
            return jsonify({"error": "Invalid price"}), 400

        
        existing_product = Product.query.filter_by(sku=data['sku']).first()
        if existing_product:
            return jsonify({"error": "SKU already exists"}), 400

        
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=float(data['price'])
        )

        db.session.add(product)
        db.session.flush()   

    
        quantity = data.get('initial_quantity', 0)
        if quantity < 0:
            return jsonify({"error": "Invalid quantity"}), 400

    
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=quantity
        )

        db.session.add(inventory)

    
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        }), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500

    except Exception:
        return jsonify({"error": "Something went wrong"}), 500
