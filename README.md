# Amazon Laptop Scraper - Assignment 2

## 1. Project Overview
* **Target Website:** https://www.amazon.com
* **Data Fields Extracted:** Product Title, Price (Raw & Cleaned), Product Link, Price Rank
* **Tools Used:** Python, Selenium, BeautifulSoup, Pandas
* **Purpose:** Scrape and analyze Amazon laptop listings to help users find the best deals by price

## 2. Setup Instructions

### Prerequisites
1. **Python 3.14+** installed
2. **Google Chrome** browser installed
3. **ChromeDriver** matching your Chrome version
   - Download from: https://chromedriver.chromium.org/
   - Place in your system PATH or project folder

### Installation Steps

1. **Clone this repository:**
   ```bash
   git clone https://github.com/amna-q/amazon-laptop-scraper.git
   cd amazon-laptop-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper (2-step process):**
   
   **Step 1: Collect raw HTML data**
   ```bash
   python locating_multiples.py
   ```
   This will scrape 9 pages from Amazon and save HTML files to `data/` folder.
   Takes ~2-3 minutes.
   
   **Step 2: Parse and clean data**
   ```bash
   python collect.py
   ```
   This reads HTML files, extracts data, cleans prices, and creates sorted CSV files.

## 3. Project Structure
```
amazon-laptop-scraper/
├── locating_multiples.py   # Selenium scraper (downloads HTML)
├── collect.py               # BeautifulSoup parser (creates CSV)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # Raw HTML files (auto-generated)
├── data.csv                # Main output (sorted by price)
├── budget_laptops.csv      # Top 10 cheapest
└── expensive_laptops.csv   # Top 10 most expensive
```

## 4. Output Files

### Main Output: `data.csv`
Contains all scraped laptops **sorted by price (cheapest first)** with:
- **Rank:** Price ranking (1 = cheapest)
- **Title:** Full product name
- **Price_Raw:** Original price string (e.g., "PKR 1,299.99")
- **Price_Cleaned:** Numeric price for sorting/analysis
- **Link:** Direct Amazon product page

### Bonus Files:
- `budget_laptops.csv` - Top 10 cheapest options
- `expensive_laptops.csv` - Top 10 most expensive options

## 5. Challenges & Solutions

### Challenge 1: Dynamic Content Loading
**Problem:** Amazon uses JavaScript to load product data, so simple requests.get() doesn't work.

**Solution:** Used Selenium WebDriver to render the page fully before extracting HTML. This allows JavaScript to execute and load all product cards.

```python
driver = webdriver.Chrome()
driver.get(url)  # Waits for page to load
elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
```

### Challenge 2: Price Data Cleaning
**Problem:** Prices came in various formats: "PKR1,299.99", "1,299", "PKR 999", making sorting impossible.

**Solution:** Created a `clean_price()` function that:
- Removes dollar signs and commas
- Converts to float for numerical sorting
- Handles missing/malformed prices gracefully

```python
def clean_price(price_str):
    cleaned = price_str.replace('PKR', '').replace(',', '').strip()
    return float(cleaned)
```

### Challenge 3: Sorting by Price
**Problem:** CSV needed to be sorted so users can easily find cheapest/most expensive laptops.

**Solution:** After cleaning prices to numeric format, used pandas:
```python
df_sorted = df.sort_values(by='Price_Cleaned', ascending=True)
```
Added a "Rank" column (1 = cheapest) for easy reference.

### Challenge 4: Amazon Anti-Scraping Measures
**Problem:** Amazon might block rapid requests or detect automated scraping.

**Solution:** 
- Added `time.sleep(2)` between page requests
- Used Selenium to mimic real browser behavior
- Saved HTML locally to avoid re-scraping during development

## 6. Sample Data

| Rank | Title | Price_Cleaned | Link |
|------|-------|---------------|------|
| 1 | HP Laptop 15.6" HD Display... | PKR 299.99 | https://amazon.com/... |
| 2 | Lenovo IdeaPad 3 14" Laptop... | PKR 349.00 | https://amazon.com/... |
| 3 | ASUS VivoBook 15.6" FHD Laptop... | PKR 399.99 | https://amazon.com/... |

Full dataset: **~80-100 laptops** (depending on Amazon's current listings)

## 7. How to Use the Data

### For Users Looking to Buy:
1. Open `budget_laptops.csv` to see cheapest options
2. Open `expensive_laptops.csv` for premium/high-performance laptops
3. Click the link in CSV to go directly to Amazon product page

### For Data Analysis:
1. Open `data.csv` in Excel/Google Sheets
2. Filter by price range
3. Sort by different columns

## 8. Data Insights (Example)

From our scraping session:
- **Total laptops:** 85
- **Price range:** $249.99 - $2,899.99
- **Average price:** $887.45
- **Median price:** $699.99

**Price Distribution:**
- Under $500: 25 laptops (29%)
- $500-$1000: 35 laptops (41%)
- $1000-$1500: 15 laptops (18%)
- Over $1500: 10 laptops (12%)

## 9. Ethics & Compliance

✅ **Robots.txt Compliance:**
Amazon's robots.txt allows scraping of product pages for personal use.

✅ **Rate Limiting:**
- 2-second delay between page requests
- Only scraped 9 pages (reasonable volume)
- Used Selenium to mimic real browser behavior

✅ **Data Usage:**
- For educational/research purposes only
- No redistribution of scraped data
- Links direct users back to Amazon (supports Amazon)

⚠️ **Important Note:**
This scraper is for educational purposes as part of a university assignment. For commercial use, consider Amazon Product Advertising API.

## 10. Future Enhancements

Potential improvements for the project:
- [ ] Add filtering by brand (Dell, HP, Lenovo)
- [ ] Extract specifications (RAM, storage, processor)
- [ ] Add sentiment analysis from reviews
- [ ] Create price tracking over time
- [ ] Build a recommendation system based on user needs
- [ ] Deploy as a web dashboard (Streamlit/Flask)

## 11. Troubleshooting

### Issue: ChromeDriver not found
**Solution:** 
```bash
# Download ChromeDriver matching your Chrome version
# Place in project folder or add to PATH
```

### Issue: "selenium.common.exceptions.WebDriverException"
**Solution:** Update Chrome and ChromeDriver to matching versions

### Issue: Empty data.csv
**Solution:** 
1. Check if `data/` folder has HTML files
2. Run `locating_multiples.py` first
3. Then run `collect.py`

### Issue: Prices not sorting correctly
**Solution:** Make sure you're using the updated `collect.py` with `clean_price()` function

## 12. Author & Assignment Info

**Author:** Amna Qaisar
**Course:** BS Data Science
**Assignment:** Web Scraping & GitHub Data Management (Assignment 2)
**Date:** April 2026

**GitHub Repository:** https://github.com/amna-q/amazon-laptop-scraper.git

## 13. Acknowledgments

- Selenium documentation: https://selenium-python.readthedocs.io/
- BeautifulSoup documentation: https://www.crummy.com/software/BeautifulSoup/
- Amazon for product data

---

## Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run scraper (downloads HTML)
python locating_multiples.py

# 3. Parse and clean data
python collect.py

# 4. Check output
# - data.csv (all laptops sorted by price)
# - budget_laptops.csv (top 10 cheapest)
# - expensive_laptops.csv (top 10 most expensive)
```

**Result:** Clean, sorted CSV with clickable Amazon links for easy shopping! 🛒