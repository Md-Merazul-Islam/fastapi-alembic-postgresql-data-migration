import pandas as pd
import random

# Generate 25 sample products
products = []
for i in range(1, 50000):
    product = {
        "name": f"Product {i}",
        "price": round(random.uniform(10, 500), 2)  # random price between 10 and 500
    }
    products.append(product)

# Create DataFrame
df = pd.DataFrame(products)

# Save to Excel
df.to_excel("products.xlsx", index=False)

print("Excel file 'products.xlsx' created successfully!")
