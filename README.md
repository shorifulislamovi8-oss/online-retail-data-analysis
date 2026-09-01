# Online Retail Data Analysis

A portfolio-focused analysis of transactional retail data using Python, pandas, and Matplotlib. This project cleanly prepares the raw sales dataset, creates a filtered analysis dataset, and highlights the strongest revenue and quantity patterns across countries, products, customers, and time.

## Business Objective

The goal of this project is to understand which countries, products, customers, and months drive the most revenue in the Online Retail dataset. The analysis focuses on identifying top-performing business segments and high-impact periods while keeping the workflow transparent, reproducible, and easy to review.

## Dataset Overview

The project uses the Online Retail sales dataset, which contains transactional records including invoice information, stock codes, descriptions, quantities, unit prices, customer IDs, dates, and countries.

This dataset is analyzed in two stages:
- a cleaned dataset used to prepare the data for analysis
- an analysis dataset filtered to remove invalid or non-relevant description records

## Data Cleaning Steps

The cleaning process follows the project logic and preserves the business rules used in the analysis:

- Removes records with negative quantities
- Removes records with negative unit prices
- Removes duplicate rows
- Handles missing descriptions by filling them with a default value
- Converts relevant numeric and date columns to appropriate data types
- Creates a derived `TotalAmount` column using `Quantity × UnitPrice`
- Excludes records with descriptions matching adjustment, wrong, damaged, bad debt, or coded patterns from the analysis dataset
- Keeps records with missing `CustomerID` values in the general analysis dataset, while customer-level analysis uses only rows where `CustomerID` is available

## Analysis Performed

The script performs a structured sales review across several dimensions:

- Country-level revenue analysis
- Product-level revenue analysis
- Product-level quantity analysis
- Customer-level revenue analysis
- Monthly revenue trend analysis
- Month-over-month growth analysis
- Identification of the best revenue month and best growth month

## Key Business Insights

The verified results from the current project are:

- Clean dataset rows: 526,052
- Analysis dataset rows: 526,023
- Top country by revenue: United Kingdom — 8,990,682.03
- Top product by revenue: REGENCY CAKESTAND 3 TIER — 174,156.54
- Top product by quantity: PAPER CRAFT, LITTLE BIRDIE — 80,995 units
- Top customer by revenue: Customer 14646 — 280,206.02
- Best revenue month: November 2011 — 1,503,866.78
- Best MoM growth: May 2011 — 43.27%

These results show that the United Kingdom is the largest revenue contributor, the product mix is strongly influenced by a few high-value items, and customer and monthly demand patterns reveal clear opportunities for revenue optimization.

## Visualizations

The project creates the following charts in the `charts/` folder:

- Monthly Revenue Trend
- Top 10 Products by Revenue
- Top 10 Countries by Revenue
- Top 10 Customers by Revenue
- Top 10 Products by Quantity

These visuals help communicate the strongest revenue drivers and seasonal performance in a simple, portfolio-friendly format.

## Technologies Used

- Python
- pandas
- Matplotlib
- openpyxl
- pathlib

## Project Structure

```text
Online Retail Analysis/
├── Online Retail.xlsx
├── online_retail_analysis_clean.py
├── data/
│   ├── online_retail_clean.csv
│   └── online_retail_analysis.csv
└── charts/
    ├── monthly_revenue_trend.png
    ├── top_10_products_by_revenue.png
    ├── top_10_countries_by_revenue.png
    ├── top_10_customers_by_revenue.png
    └── top_10_products_by_quantity.png
```

## How to Run the Project Locally

1. Clone or download the project folder.
2. Ensure the dataset file `Online Retail.xlsx` is saved in the project root.
3. Install the required Python packages:

```bash
pip install pandas matplotlib openpyxl
```

4. Run the analysis script from the project directory:

```bash
python online_retail_analysis_clean.py
```

This will:
- create the `data/` and `charts/` folders automatically if they do not exist
- save the cleaned and analysis CSV files to `data/`
- save the generated charts to `charts/`
- print the analysis summary in the terminal

## Future Improvements

Potential next steps for this project include:

- adding a clearer executive summary section in the script output
- refining chart labels and formatting for presentation quality
- exploring product segmentation or repeat-customer trends
- comparing revenue performance by country and month in a more explicit narrative format

These enhancements would improve readability and presentation without changing the current analysis logic or core findings.

## Summary

This project is a straightforward retail sales analysis built to communicate business insights clearly and professionally. It demonstrates practical data cleaning, business-focused analysis, and effective charting using common Python tools appropriate for a GitHub portfolio.
