-- Sample dataset for the mock MCP store database.
INSERT INTO customers (email, full_name, address)
VALUES
    ('alice@example.com', 'Alice Johnson', '123 Maple Street, Springfield, USA'),
    ('bob@example.com', 'Bob Smith', '456 Oak Avenue, Lakeside, USA'),
    ('carol@example.com', 'Carol Lee', '789 Pine Road, Riverside, USA')
ON CONFLICT (email) DO NOTHING;

INSERT INTO products (sku, name, description, price)
VALUES
    ('SKU-001', 'Wireless Headphones', 'Noise-cancelling over-ear headphones.', 199.99),
    ('SKU-002', 'Smartwatch', 'Water-resistant smartwatch with health tracking.', 149.50),
    ('SKU-003', 'Portable Speaker', 'Bluetooth speaker with 12-hour battery life.', 89.00),
    ('SKU-004', 'USB-C Charger', '65W fast charger for laptops and phones.', 39.99)
ON CONFLICT (sku) DO NOTHING;

INSERT INTO inventory (product_id, quantity, location)
VALUES
    (1, 25, 'Warehouse A - Aisle 4'),
    (2, 18, 'Warehouse A - Aisle 7'),
    (3, 40, 'Warehouse B - Shelf 2'),
    (4, 60, 'Warehouse B - Shelf 5')
ON CONFLICT DO NOTHING;

INSERT INTO orders (customer_id, status, total_amount, placed_at)
VALUES
    (1, 'processing', 349.49, NOW() - INTERVAL '2 days'),
    (2, 'shipped', 199.99, NOW() - INTERVAL '1 day'),
    (3, 'delivered', 128.99, NOW() - INTERVAL '5 days')
ON CONFLICT DO NOTHING;

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES
    (1, 1, 1, 199.99),
    (1, 2, 1, 149.50),
    (2, 1, 1, 199.99),
    (3, 3, 1, 89.00),
    (3, 4, 1, 39.99)
ON CONFLICT DO NOTHING;
