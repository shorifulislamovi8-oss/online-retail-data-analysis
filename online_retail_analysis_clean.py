from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = PROJECT_ROOT / "Online Retail.xlsx"
DATA_DIR = PROJECT_ROOT / "data"
CHARTS_DIR = PROJECT_ROOT / "charts"
CLEAN_CSV = DATA_DIR / "online_retail_clean.csv"
ANALYSIS_CSV = DATA_DIR / "online_retail_analysis.csv"

NON_PRODUCT_CODES = {"POST", "DOT", "M", "AMAZONFEE", "PADS", "S", "B"}
INVALID_DESCRIPTION_PATTERN = r"adjust|wrong|damag|bad debt|coded"


def ensure_output_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_excel(DATA_FILE, engine="openpyxl")
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)
    df["Description"] = df["Description"].fillna("Unknown").astype(str).str.strip()
    df["Country"] = df["Country"].fillna("Unknown").astype(str).str.strip()

    for col in ["Quantity", "UnitPrice", "CustomerID"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    df = df[(df["Quantity"] >= 0) & (df["UnitPrice"] >= 0)].copy()
    df = df[~df["Description"].fillna("").str.strip().eq("")].copy()
    df = df.drop_duplicates().copy()
    df = df.dropna(subset=["InvoiceDate"]).copy()

    df["TotalAmount"] = (df["Quantity"] * df["UnitPrice"]).round(2)
    return df


def build_analysis_dataset(clean_df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = clean_df[
        ~clean_df["Description"].str.contains(
            INVALID_DESCRIPTION_PATTERN,
            case=False,
            na=False,
        )
    ].copy()
    return analysis_df


def build_analysis_outputs(df: pd.DataFrame) -> dict:
    country_revenue = (
        df.groupby("Country", as_index=False)["TotalAmount"]
        .sum()
        .sort_values("TotalAmount", ascending=False)
        .head(10)
        .copy()
    )
    country_revenue["Country"] = country_revenue["Country"].astype(str)

    product_df = df[~df["StockCode"].isin(NON_PRODUCT_CODES)].copy()

    product_revenue = (
        product_df.groupby(["StockCode", "Description"], as_index=False)["TotalAmount"]
        .sum()
        .sort_values("TotalAmount", ascending=False)
        .head(10)
        .copy()
    )

    product_quantity = (
        product_df.groupby(["StockCode", "Description"], as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
        .head(10)
        .copy()
    )

    customer_df = df.dropna(subset=["CustomerID"]).copy()
    customer_df["CustomerID"] = customer_df["CustomerID"].astype(str)

    customer_revenue = (
        customer_df.groupby("CustomerID", as_index=False)["TotalAmount"]
        .sum()
        .sort_values("TotalAmount", ascending=False)
        .head(10)
        .copy()
    )

    monthly_df = df.copy()
    monthly_df["Month"] = monthly_df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_revenue = (
        monthly_df.groupby("Month", as_index=False)["TotalAmount"]
        .sum()
        .sort_values("Month")
        .reset_index(drop=True)
        .copy()
    )
    monthly_revenue.columns = ["Month", "Revenue"]

    monthly_growth = monthly_revenue.copy()
    monthly_growth["MoM_Growth_pct"] = monthly_growth["Revenue"].pct_change().fillna(0) * 100

    best_revenue_month = monthly_revenue.loc[monthly_revenue["Revenue"].idxmax()].copy()
    best_growth_month = monthly_growth.loc[monthly_growth["MoM_Growth_pct"].idxmax()].copy()

    return {
        "country_revenue": country_revenue,
        "product_revenue": product_revenue,
        "product_quantity": product_quantity,
        "customer_revenue": customer_revenue,
        "monthly_revenue": monthly_revenue,
        "monthly_growth": monthly_growth,
        "best_revenue_month": best_revenue_month,
        "best_growth_month": best_growth_month,
    }


def save_charts(results: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(
        results["monthly_revenue"]["Month"].astype(str),
        results["monthly_revenue"]["Revenue"],
        marker="o",
    )
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_revenue_trend.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(
        results["product_revenue"]["Description"].astype(str),
        results["product_revenue"]["TotalAmount"],
    )
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "top_10_products_by_revenue.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(
        results["country_revenue"]["Country"].astype(str),
        results["country_revenue"]["TotalAmount"],
    )
    plt.title("Top 10 Countries by Revenue")
    plt.xlabel("Country")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "top_10_countries_by_revenue.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(
        results["customer_revenue"]["CustomerID"].astype(str),
        results["customer_revenue"]["TotalAmount"],
    )
    plt.title("Top 10 Customers by Revenue")
    plt.xlabel("Customer ID")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "top_10_customers_by_revenue.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(
        results["product_quantity"]["Description"].astype(str),
        results["product_quantity"]["Quantity"],
    )
    plt.title("Top 10 Products by Quantity")
    plt.xlabel("Product")
    plt.ylabel("Quantity")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "top_10_products_by_quantity.png", dpi=200)
    plt.close()


def print_analysis(results: dict):
    print("\n=== Top 10 Countries by Revenue ===")
    print(results["country_revenue"].to_string(index=False))

    print("\n=== Top 10 Products by Revenue ===")
    print(results["product_revenue"].to_string(index=False))

    print("\n=== Top 10 Products by Quantity ===")
    print(results["product_quantity"].to_string(index=False))

    print("\n=== Top 10 Customers by Revenue ===")
    print(results["customer_revenue"].to_string(index=False))

    print("\n=== Monthly Revenue Trend ===")
    print(results["monthly_revenue"].to_string(index=False))

    print("\n=== Month-over-Month Revenue Growth ===")
    print(results["monthly_growth"].to_string(index=False))

    print("\n=== Best Revenue Month ===")
    print(results["best_revenue_month"].to_string())

    print("\n=== Best Growth Month ===")
    print(results["best_growth_month"].to_string())

    print("\n=== Business Insights ===")
    top_country = results["country_revenue"].iloc[0]
    top_product = results["product_revenue"].iloc[0]
    top_customer = results["customer_revenue"].iloc[0]
    best_revenue_month = results["best_revenue_month"]
    best_growth_month = results["best_growth_month"]

    print(
        f"1. Best revenue month: {best_revenue_month['Month']} "
        f"with revenue {best_revenue_month['Revenue']:,.2f}."
    )
    print(
        f"2. Best growth month: {best_growth_month['Month']} "
        f"with MoM growth {best_growth_month['MoM_Growth_pct']:.2f}%."
    )
    print(
        f"3. Top country by revenue: {top_country['Country']} "
        f"({top_country['TotalAmount']:,.2f})."
    )
    print(
        f"4. Top product by revenue: {top_product['Description']} "
        f"({top_product['TotalAmount']:,.2f})."
    )
    print(
        f"5. Top customer by revenue: {top_customer['CustomerID']} "
        f"({top_customer['TotalAmount']:,.2f})."
    )


def main():
    ensure_output_directories()

    raw_df = load_data()
    clean_df = clean_dataset(raw_df)
    clean_df.to_csv(CLEAN_CSV, index=False)

    analysis_df = build_analysis_dataset(clean_df)
    analysis_df.to_csv(ANALYSIS_CSV, index=False)

    results = build_analysis_outputs(analysis_df)
    save_charts(results, CHARTS_DIR)

    print(f"Clean dataset rows: {len(clean_df)}")
    print(f"Analysis dataset rows: {len(analysis_df)}")
    print(f"Saved clean CSV: {CLEAN_CSV.name}")
    print(f"Saved analysis CSV: {ANALYSIS_CSV.name}")

    print_analysis(results)


if __name__ == "__main__":
    main()
