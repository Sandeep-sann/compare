import streamlit as st
import pandas as pd

# Load datasets
flipkart_file = "flipkart_all_electronics.csv"
amazon_file = "All Electronics.csv"

try:
    # Load Flipkart data
    flipkart_df = pd.read_csv(flipkart_file)
    amazon_df = pd.read_csv(amazon_file)

    # Clean Flipkart ratings column
    flipkart_df['ratings'] = flipkart_df['ratings'].astype(str)  # Ensure the column is of type string
    flipkart_df['ratings'] = flipkart_df['ratings'].str.extract(r'(\d+\.?\d*)')  # Extract numeric part
    flipkart_df['ratings'] = pd.to_numeric(flipkart_df['ratings'], errors='coerce')  # Convert to numeric

    # Clean Amazon ratings column
    amazon_df['ratings'] = amazon_df['ratings'].astype(str)  # Ensure the column is of type string
    amazon_df['ratings'] = amazon_df['ratings'].str.extract(r'(\d+\.?\d*)')  # Extract numeric part
    amazon_df['ratings'] = pd.to_numeric(amazon_df['ratings'], errors='coerce')  # Convert to numeric

    # Drop rows with missing ratings
    flipkart_df = flipkart_df.dropna(subset=['ratings'])
    amazon_df = amazon_df.dropna(subset=['ratings'])

    # App Title
    st.title("Product Comparison: Flipkart vs Amazon")

    # Search Section
    st.header("Search for a Product")
    product_name = st.text_input("Enter Product Name:", "")

    if product_name:
        # Filter products by name
        flipkart_products = flipkart_df[flipkart_df['name'].str.contains(product_name, case=False, na=False)]
        amazon_products = amazon_df[amazon_df['name'].str.contains(product_name, case=False, na=False)]

        if flipkart_products.empty and amazon_products.empty:
            st.warning("No products found for the given name.")
        else:
            # Display results
            st.subheader("Search Results")
            col1, col2 = st.columns(2)

            # Limit results to 20 products
            flipkart_products = flipkart_products.head(20)
            amazon_products = amazon_products.head(20)

            with col1:
                st.write("### Flipkart Products")
                if not flipkart_products.empty:
                    for _, product in flipkart_products.iterrows():
                        image_url = product['image'][0] if isinstance(product['image'], list) else product['image']
                        st.markdown(f"""
                            <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px; display:flex; flex-direction:column; align-items:center;">
                                <img src="{image_url}" width="100" height="100" style="border-radius:5px;">
                                <h5>{product['name']}</h5>
                                <p>Rating: {product['ratings']}</p>
                                <p>Price: ₹{product['actual_price']}</p>
                                <a href="{product['link']}" target="_blank" style="color:blue; text-decoration:none;">View Product</a>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No products found on Flipkart.")

            with col2:
                st.write("### Amazon Products")
                if not amazon_products.empty:
                    for _, product in amazon_products.iterrows():
                        st.markdown(f"""
                            <div style="border:1px solid #ddd; padding:10px; border-radius:5px; margin-bottom:10px; display:flex; flex-direction:column; align-items:center;">
                                <img src="{product['image']}" width="100" height="100" style="border-radius:5px;">
                                <h5>{product['name']}</h5>
                                <p>Rating: {product['ratings']}</p>
                                <p>Price: ₹{product['actual_price']}</p>
                                <a href="{product['link']}" target="_blank" style="color:blue; text-decoration:none;">View Product</a>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No products found on Amazon.")

            # Comparison Logic
            st.subheader("Comparison Result")
            if not flipkart_products.empty and not amazon_products.empty:
                # Compare based on highest rating
                best_flipkart = flipkart_products.loc[flipkart_products['ratings'].idxmax()]
                best_amazon = amazon_products.loc[amazon_products['ratings'].idxmax()]

                if best_flipkart['ratings'] > best_amazon['ratings']:
                    st.success(f"Best Product: Flipkart - {best_flipkart['name']} (Rating: {best_flipkart['ratings']})")
                elif best_amazon['ratings'] > best_flipkart['ratings']:
                    st.success(f"Best Product: Amazon - {best_amazon['name']} (Rating: {best_amazon['ratings']})")
                else:
                    st.info("Both Flipkart and Amazon have similar products with comparable ratings.")
            else:
                st.info("Comparison not possible as one of the platforms has no matching products.")
except Exception as e:
    st.error(f"Error loading datasets: {e}")

# Footer
st.markdown("""
---
**Developed by [n j nsandeep]**  
Compare products easily and find the best deals!
""")
