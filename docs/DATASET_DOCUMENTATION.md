# Walmart Connect Campaign Performance & Churn Dataset

## Overview
This synthetic dataset simulates advertising campaign performance data for **Walmart Connect** across 2024 and 2025. It is designed for machine learning, exploratory data analysis (EDA), and churn prediction modeling.

---

## Data Schema & Feature Definitions

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `campaign_id` | String | Unique Identifier for the campaign (e.g., `CAMP-10001`). |
| `advertiser_id` | String | Unique Identifier for the advertiser account. |
| `campaign_name` | String | Name of the campaign or promotional event. |
| `campaign_type` | Categorical | Type of ad placement: `Sponsored Products`, `Sponsored Brands`, `Sponsored Videos`. |
| `platform_device` | Categorical | Device type target: `App`, `Desktop`, `Mobile Web`. |
| `product_category` | Categorical | Category targeted: `Electronics`, `Home`, `Beauty`, `Clothing`. |
| `start_date` | Date | Start date of the campaign (`YYYY-MM-DD`). |
| `end_date` | Date | End date of the campaign (`YYYY-MM-DD`). |
| `daily_budget_usd` | Float | Allocated daily ad spend in USD. |
| `impressions` | Integer | Total number of ad impressions served. |
| `clicks` | Integer | Total user clicks on the ad. |
| `conversions` | Integer | Total completed sales attributed to the campaign. |
| `ctr` | Float | Click-Through Rate ($CTR = \frac{\text{clicks}}{\text{impressions}}$). |
| `cpm_usd` | Float | Cost Per Mille / Cost Per 1,000 Impressions. |
| `spend_usd` | Float | Total spend incurred by the campaign. |
| `cvr` | Float | Conversion Rate ($CVR = \frac{\text{conversions}}{\text{clicks}}$). |
| `cost_per_conversion_usd` | Float | Average cost spent per conversion. |
| `churned` | Boolean | Target Label (`0` = Retained, `1` = Churned/Low Performing). |

---

## Business Logic & Churn Rules

A campaign/advertiser is flagged as **Churned (`churned = 1`)** if any of the following threshold conditions are met:

* **Low Engagement:** $CTR < 0.35\%$
* **Low Conversion:** $CVR < 3.0\%$
* **Inefficient Acquisition:** $\text{Cost Per Conversion} > \$85.00$
* **High Spend Failure:** Total spend $> \$1,000$ with fewer than 15 conversions.

---

## Configuration & Customization

The dataset generation script (`src/generator.py`) relies on `config/config.json`. You can modify the following parameters to adjust data distribution:

* `num_records`: Number of records to generate.
* `campaign_type_weights`: Distribution weights for ad types.
* `churn_rules`: Threshold values for rule-based churn labeling.