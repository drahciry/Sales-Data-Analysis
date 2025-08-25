# Sales Data Analysis Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-blue?style=for-the-badge&logo=pandas&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow?style=for-the-badge&logo=powerbi&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

This project is a comprehensive data analysis solution built with Python and Pandas. It processes raw sales data from an Excel spreadsheet, performs various cleaning and transformation steps, and generates insightful reports answering key business questions. The entire analysis is conducted with a focus on data integrity, using Python's `Decimal` type for all financial calculations to ensure precision.

The final output of the Python script is then used as a data source for an interactive dashboard in Power BI.

## 📊 Dashboard & Visualizations

The processed data from this project was used as a data source for an interactive dashboard built in **Power BI**. The dashboard provides a high-level overview of key performance indicators (KPIs) and allows for interactive filtering and exploration of the sales data. Below are the main insights derived from the visualizations.

---

### Key Insights & Analysis

-   **Daily Sales Behavior (Line Chart):** The analysis of daily income reveals a clear trend: sales peak at the beginning of the month and gradually decrease towards the end. This suggests that marketing efforts and promotions could be strategically focused on the second half of the month to mitigate this drop-off.

<img src="./images/Line Graphic.png" title="Line Graphic" alt="Line Graphic" justify-content="center">

-   **Monthly Sales Distribution (Pie Chart):** Sales are evenly distributed throughout the months, indicating no significant seasonality in the current dataset. This stable performance provides a reliable baseline for measuring the impact of future marketing campaigns.

<img src="./images/Pizza Graphic 1.png" title="Pizza Graphic 1" alt="Pizza Graphic 1" justify-content="center">

-   **Customer Value Analysis (Bar Chart):** By ranking customers by their total spending, we can identify high-value clients. This segmentation is crucial for targeted marketing strategies, loyalty programs, and personalized engagement to boost sales.

<img src="./images/Bar Graphic 1.png" title="Bar Graphic 1" alt="Bar Graphic 1" justify-content="center">

-   **Product Price Point Performance (Donut Chart):** The data shows that high-value products (costing over $4,500.00) account for a considerable 25% of total revenue. This indicates a healthy demand for premium items and suggests opportunities for upselling and cross-selling high-margin products.

<img src="./images/Donuts Graphic.png" title="Donut Graphic 1" alt="Donut Graphic 1" justify-content="center">

-   **Geographical Sales Performance (Pie & Bar Charts):** The analysis of sales by state, both in quantity and total value, highlights a strong concentration of business in the Southeast region of Brazil. This confirms the region's high purchasing power and predisposition to buy. The comparison between quantity and value also reveals that a higher number of items sold doesn't always equate to higher revenue, providing a nuanced view for logistical and marketing planning.

<img src="./images/Pizza Graphic 2.png" title="Pizza Graphic 2" alt="Pizza Graphic 2" justify-content="center">

<img src="./images/Bar Graphic 2.png" title="Bar Graphic 2" alt="Bar Graphic 2" justify-content="center">

---

## 💡 Key Features of the Python Script

The core of this project is a Python script (`src/main.py`) that provides a suite of functions to analyze sales data, including:

-   **Financial Precision**: All monetary calculations use the `Decimal` type to avoid floating-point inaccuracies, which is crucial for financial reporting.
-   **Daily Income Reports**: Calculate total income for any given day.
-   **Client-Specific Analysis**: Track daily income for individual clients.
-   **Customer Ranking**: Identify the top 5 best and worst customers based on their total spending within a specified period.
-   **Complete Income History**: Generate a detailed, day-by-day report of daily and accumulated income for every client over a period. This report is saved as an `.xlsx` file.
-   **Best-Selling Products**: Determine the best-selling product(s) for any given day.
-   **Inventory Management**: Identify products with low stock levels (<= 50 units).
-   **High-Value Sales Tracking**: Filter and report high-value sales (>= $4,500.00).
-   **Sales by State**: Aggregate sales data by state to generate geographical performance reports.

## 📁 Project Structure

The project follows a standard and scalable structure for data science projects, ensuring a clear separation between data, source code, and results.

```
.
├── data
│   ├── processed/      # Output directory for generated reports (.xlsx files)
│   └── raw/            # Contains the original, unmodified data source
│       └── sales_relatory.xlsx
├── images/
│   ├── Bar Graphic 1.png
│   ├── Bar Graphic 2.png
│   ├── Donuts Graphic.png
│   ├── Line Graphic.png
│   ├── Pizza Graphic 1.png
│   ├── Pizza Graphic 2.png
│   └── Table.png
├── src/
│   └── main.py         # The main Python script with all analysis functions
├── .gitignore          # Specifies files to be ignored by Git
├── environment.yml     # Conda environment file for dependency management
├── LICENSE             # Project license
└── README.md           # This file
```

## 🔧 Technologies Used

-   **Python 3.10+**
-   **Pandas**: For data manipulation and analysis.
-   **Openpyxl**: Required by Pandas to read and write `.xlsx` files.
-   **Power BI**: For data visualization and dashboard creation.
-   **Conda**: For environment and dependency management.

## 🚀 How to Run

To set up and run the Python analysis script on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/drahciry/Sales-Data-Analysis.git
    cd Sales-Data-Analysis
    ```

2.  **Create the Conda environment:**
    This project uses Conda to manage its dependencies. The `environment.yml` file contains all the necessary packages.
    ```bash
    conda env create -f environment.yml
    ```

3.  **Activate the environment:**
    ```bash
    conda activate sales_data_analysis
    ```

4.  **Place your data:**
    Ensure your raw data file, `sales_relatory.xlsx`, is placed inside the `data/raw/` directory.

5.  **Run the analysis script:**
    Execute the main script from the root directory. The script will run the analyses and save the generated reports in the `data/processed/` folder.
    ```bash
    python -m src.main
    ```

---

## 👤 Author

This project was developed by **Richard** as a case study in data analysis and business intelligence.

-   **GitHub**: [@drahciry](https://github.com/drahciry)
-   **LinkedIn**: [Richard Gonçalves](https://www.linkedin.com/in/drahciry/)                