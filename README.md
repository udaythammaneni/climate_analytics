# 🌍 CO₂ Emissions Monitoring & Environmental Impact Analytics System

## 📌 Project Overview

This project is an end-to-end environmental data analytics system built using **Python, PySpark, Databricks, Delta Lake, Unity Catalog, Apache Airflow, and Databricks SQL Dashboards**.

The system ingests global CO₂ emissions data, processes it through a Medallion Architecture (Bronze, Silver, Gold layers), and provides interactive dashboards for trend analysis and environmental insights.

---

# 🎯 Business Objective

Environmental agencies require scalable systems to:

* Monitor CO₂ emissions across countries
* Analyze year-over-year emission trends
* Identify high-emission countries
* Support environmental policy decisions
* Provide centralized visual dashboards

This project automates data ingestion, transformation, analytics, and reporting.

---

# 🏗 Architecture

```
Local CSV (OWID Dataset)
        ↓
Unity Catalog Volume
        ↓
Bronze Layer (Raw Delta Table)
        ↓
Silver Layer (Cleaned & Validated Data)
        ↓
Gold Layer (Business KPIs & Aggregations)
        ↓
Airflow Orchestration
        ↓
Databricks SQL Warehouse
        ↓
Interactive Dashboard
```

---

# 🛠 Technology Stack

### Data Processing

* Python
* PySpark
* Delta Lake

### Platform

* Azure Databricks
* Unity Catalog

### Workflow Orchestration

* Apache Airflow

### Visualization

* Databricks SQL Warehouse
* Databricks Dashboards

### Storage

* Unity Catalog Managed Storage
* Delta Tables

---

# 📂 Project Structure

```
climate_analytics/
│
├── dags/
│   └── co2_pipeline_dag.py
|
├── dashboards/
│   ├── dashboard_screenshots/
|   └── CO2 Emissions Analytics Dashboard.lvdash.json
|
├── data/
│   └── raw/
|        └── owid-co2-data.csv
│
├── notebooks/
|   ├── setup.py
│   ├── 01_bronze_ingestion.py
│   ├── 02_silver_cleaning.py
│   └── 03_gold_kpis.py
│
├── README.md
```

---

# 🥉 Bronze Layer – Raw Data Ingestion

* Uploaded OWID CO₂ dataset into Unity Catalog Volume
* Read CSV using PySpark
* Selected required columns
* Added metadata:

  * ingestion_timestamp
  * data_source
* Stored as Delta table:

```
climate_analytics.bronze.co2_raw
```

---

# 🥈 Silver Layer – Data Cleaning & Validation

Data quality rules applied:

* Removed null country & year
* Removed aggregated regions (filtered using ISO code)
* Removed negative CO₂ values
* Filtered year >= 1950
* Removed duplicate (country, year)

Stored as:

```
climate_analytics.silver.co2_clean
```

---

# 🥇 Gold Layer – Business Analytics

### Implemented KPIs:

1. Emissions Per Capita
2. Year-over-Year Growth (Window Functions)
3. Global Yearly CO₂ Trend
4. Top Polluting Countries

Gold tables created:

```
climate_analytics.gold.country_analytics
climate_analytics.gold.global_trends
climate_analytics.gold.top_polluters
```

---

# 🔄 Workflow Automation (Airflow)

An Apache Airflow DAG orchestrates:

```
Bronze → Silver → Gold
```

Features:

* Task dependency management
* Retry logic
* Daily schedule
* Databricks job integration

DAG Name:

```
co2_emissions_pipeline
```

---

# 📊 Databricks Dashboard

A dedicated SQL Warehouse serves curated Gold tables.

Dashboard includes:

* 📈 Global CO₂ Trend (Line Chart)
* 📊 Top 10 Polluters (Bar Chart)
* 📉 Country Year-over-Year Growth
* 📌 KPI Summary Card

This enables interactive analytics and stakeholder reporting.

---

# 📈 Key Insights Enabled

* Identification of high-emission countries
* Long-term global emission trends
* Year-over-year emission growth analysis
* Per capita emission comparison

---

# 🔐 Production Best Practices Followed

* Medallion Architecture (Bronze/Silver/Gold)
* Unity Catalog governance
* Delta Lake ACID tables
* Automated workflow orchestration
* SQL Warehouse for BI separation
* Data validation rules in Silver layer

---

# 🚀 How to Run the Project

1. Upload OWID CSV to Unity Catalog Volume.
2. Run Bronze notebook.
3. Run Silver notebook.
4. Run Gold notebook.
5. Trigger Airflow DAG.
6. Access SQL Warehouse and Dashboard.