"""
collect.py - Data Collection and Cleaning for Amazon Laptop Scraper
This script reads HTML files, extracts data, cleans it, and creates a sorted CSV
"""

from bs4 import BeautifulSoup
import os 
import pandas as pd

def clean_price(price_str):
    """
    Clean price string and convert to numeric value
    
    Examples:
    '1,299' -> 1299.00
    'PKR 999' -> 999.00
    """
    if not price_str:
        return None
    
    try:
        cleaned = price_str.replace('PKR', '').replace(',', '').strip()
        return float(cleaned)
    except:
        return None

def clean_title(title_str):
    """Remove extra whitespace and newlines from title"""
    if not title_str:
        return "N/A"
    return ' '.join(title_str.split())

d = {
    'Title': [], 
    'Price_Raw': [],
    'Price_Cleaned': [],
    'Link': []
}

print("Reading HTML files from data folder...")
file_count = 0
success_count = 0
error_count = 0

# Process each HTML file
for file in os.listdir("data"):
    file_count += 1
    
    try:
        # Read HTML file
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        # Extract title
        t = soup.find("h2")
        title = t.get_text() if t else "N/A"
        title = clean_title(title)
        
        # Extract link
        l = soup.find("a")
        link = "https://amazon.com" + l['href'] if l and l.get('href') else "N/A"
        
        # Extract price
        p = soup.find("span", class_='a-price-whole')
        price_raw = p.get_text() if p else "N/A"
        
        price_cleaned = clean_price(price_raw)
        
        # Store 
        d['Title'].append(title)
        d['Price_Raw'].append(price_raw)
        d['Price_Cleaned'].append(price_cleaned)
        d['Link'].append(link)
        
        success_count += 1
        
    except Exception as e:
        error_count += 1
        print(f"Error processing {file}: {e}")

df = pd.DataFrame(data=d)

print("\n")
print(f"Data Collection Summary:")
print("\n")
print(f"Total files processed: {file_count}")
print(f"Successfully extracted: {success_count}")
print(f"Errors encountered: {error_count}")
print("\n")

print("Data Quality Check:")
print(f"  Total products: {len(df)}")
print(f"  Missing titles: {df['Title'].isna().sum()}")
print(f"  Missing prices: {df['Price_Cleaned'].isna().sum()}")
print(f"  Valid prices: {df['Price_Cleaned'].notna().sum()}")

# Remove rows with no price (can't sort without price)
df_with_prices = df[df['Price_Cleaned'].notna()].copy()
print(f"\nAfter removing products without prices: {len(df_with_prices)} products")

# Sort by price (ASCENDING - cheapest first)
df_sorted = df_with_prices.sort_values(by='Price_Cleaned', ascending=True)

# Reset index
df_sorted = df_sorted.reset_index(drop=True)

# Add a rank column
df_sorted.insert(0, 'Rank', range(1, len(df_sorted) + 1))

# Save to CSV
df_sorted.to_csv("data.csv", index=False)
print(f"\nData saved to: data.csv")

# Display price statistics
print("\n")
print(f"Price Statistics (PKR):")
print("\n")
print(f"Cheapest laptop:  PKR {df_sorted['Price_Cleaned'].min():,.2f}")
print(f"Most expensive:   PKR {df_sorted['Price_Cleaned'].max():,.2f}")
print(f"Average price:    PKR {df_sorted['Price_Cleaned'].mean():,.2f}")
print(f"Median price:     PKR {df_sorted['Price_Cleaned'].median():,.2f}")
print("\n")

print("TOP 5 CHEAPEST LAPTOPS:")
print("\n")
for idx, row in df_sorted.head(5).iterrows():
    print(f"{row['Rank']}. PKR {row['Price_Cleaned']:,.2f} - {row['Title'][:60]}...")
    print(f"   Link: {row['Link']}")
    print()

print("\nTOP 5 MOST EXPENSIVE LAPTOPS:")
print("\n")
for idx, row in df_sorted.tail(5).iterrows():
    print(f"{row['Rank']}. PKR {row['Price_Cleaned']:,.2f} - {row['Title'][:60]}...")
    print(f"   Link: {row['Link']}")
    print()

# Create a separate file with only expensive laptops (for easy access)
expensive_laptops = df_sorted.tail(10).copy()
expensive_laptops.to_csv("expensive_laptops.csv", index=False)
print("Also saved top 10 most expensive laptops to: expensive_laptops.csv")

# Create a separate file with budget laptops
budget_laptops = df_sorted.head(10).copy()
budget_laptops.to_csv("budget_laptops.csv", index=False)
print("Also saved top 10 cheapest laptops to: budget_laptops.csv")

print("\nData collection and cleaning complete!")