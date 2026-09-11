from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# ==============================================================================
# LOGIQUE DU GÉNÉRATEUR (CLASSE PRINCIPALE)
# ==============================================================================
class WalmartConnectDataGenerator:

  def __init__(self, config, campaigns):
    self.config = config
    self.campaigns = campaigns
    np.random.seed(self.config["random_seed"])

  def load_source_products(self):
    """Charge les produits uniques à partir du CSV source."""
    df_source = pd.read_csv(self.config["source_csv_path"])
    products_df = (
        df_source[["Category", "Product_Name"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    return list(products_df.itertuples(index=False))

  def generate_dataset(self):
    products_list = self.load_source_products()
    n = self.config["num_records"]

    # Génération d'un pool d'annonceurs uniques
    advertisers = [f"ADV-{np.random.randint(1000, 9999)}" for _ in range(300)]

    # Extraction des configurations
    c_type_names = list(self.config["campaign_type_weights"].keys())
    c_type_probs = list(self.config["campaign_type_weights"].values())

    device_names = list(self.config["platform_device_weights"].keys())
    device_probs = list(self.config["platform_device_weights"].values())

    rows = []

    for i in range(n):
      adv_id = np.random.choice(advertisers)
      camp_id = f"CAMP-{10001 + i}"

      # 1. Sélection de la campagne promotionnelle
      camp_meta = self.campaigns[np.random.choice(len(self.campaigns))]
      walmart_event = camp_meta["name"]
      c_start_base = datetime.strptime(camp_meta["start"], "%Y-%m-%d")
      c_end_base = datetime.strptime(camp_meta["end"], "%Y-%m-%d")
      focus_cats = camp_meta["categories"]

      # 2. Sélection du produit (filtré préférentiellement par catégorie)
      if np.random.rand() < 0.75:
        eligible = [p for p in products_list if p.Category in focus_cats]
        chosen_prod = eligible[
            np.random.choice(len(eligible))
        ] if eligible else products_list[np.random.choice(len(products_list))]
      else:
        chosen_prod = products_list[np.random.choice(len(products_list))]

      prod_name, category = chosen_prod.Product_Name, chosen_prod.Category

      # 3. Calcul des dates de la campagne
      duration_days = (c_end_base - c_start_base).days
      if duration_days <= 3:
        c_start, c_end = c_start_base, c_end_base
        dur = max(1, duration_days)
      else:
        offset = np.random.randint(0, max(1, duration_days - 2))
        sub_dur = np.random.randint(3, max(4, duration_days - offset + 1))
        c_start = c_start_base + timedelta(days=int(offset))
        c_end = min(
            c_start_base + timedelta(days=int(offset + sub_dur)), c_end_base
        )
        dur = max(1, (c_end - c_start).days)

      # 4. Canal et Format
      c_type = np.random.choice(c_type_names, p=c_type_probs)
      p_dev = np.random.choice(device_names, p=device_probs)

      # 5. Calcul du Budget
      b_cfg = self.config["budget"]
      budget_per_day = np.random.uniform(
          b_cfg["daily_min"], b_cfg["daily_max"]
      )
      if any(k in walmart_event for k in ["Black Friday", "Cyber", "Deals"]):
        budget_per_day *= b_cfg["multipliers"]["Major_Event"]
      if c_type in b_cfg["multipliers"]:
        budget_per_day *= b_cfg["multipliers"][c_type]

      budget = round(budget_per_day * dur, 2)

      # 6. Performance : CTR & Impresions
      m_cfg = self.config["metrics"]
      base_ctr = np.random.beta(
          a=m_cfg["ctr_beta_alpha"], b=m_cfg["ctr_beta_beta"]
      )
      base_ctr *= self.config["ctr_multipliers"].get(p_dev, 1.0)
      base_ctr *= self.config["ctr_multipliers"].get(c_type, 1.0)
      base_ctr = max(m_cfg["ctr_min"], min(base_ctr, m_cfg["ctr_max"]))

      cpm = np.random.uniform(m_cfg["cpm_min_usd"], m_cfg["cpm_max_usd"])
      if c_type == "Sponsored Videos":
        cpm *= m_cfg["cpm_video_multiplier"]

      spend_ratio = np.random.uniform(
          m_cfg["spend_ratio_min"], m_cfg["spend_ratio_max"]
      )
      actual_spend = budget * spend_ratio

      imp = max(500, int((actual_spend / cpm) * 1000))
      clk = max(1, int(imp * base_ctr))
      actual_ctr = round((clk / imp) * 100, 2)

      # 7. Conversions (CVR)
      cvr_min, cvr_max = self.config["cvr_base_range"]
      base_cvr = np.random.uniform(cvr_min, cvr_max)
      base_cvr *= self.config["cvr_category_multipliers"].get(category, 1.0)

      conv_14d = int(clk * base_cvr)
      cvr_actual = conv_14d / clk if clk > 0 else 0

      # 8. Modèle de Churn
      cost_per_conv = (
          (actual_spend / conv_14d) if conv_14d > 0 else (actual_spend * 2)
      )
      rules = self.config["churn_rules"]
      churn_score = 0.0

      if actual_ctr < (rules["ctr_threshold"] * 100):
        churn_score += 0.35
      if cvr_actual < rules["cvr_threshold"]:
        churn_score += 0.40
      if cost_per_conv > rules["cost_per_conv_threshold"]:
        churn_score += 0.30
      if (
          actual_spend > 2500
          and conv_14d < rules["min_conversions_high_spend"]
      ):
        churn_score += 0.45

      churn_prob = 1 / (1 + np.exp(-(churn_score - 0.45) * 5))
      has_churned = 1 if np.random.rand() < churn_prob else 0

      # Structure de la ligne
      rows.append({
          "Advertiser_ID": adv_id,
          "Campaign_ID": camp_id,
          "Walmart_Promotional_Event": walmart_event,
          "Product_Category": category,
          "Product_Name": prod_name,
          "Campaign_Type": c_type,
          "Platform_Device": p_dev,
          "Campaign_Start_Date": c_start.strftime("%Y-%m-%d"),
          "Campaign_End_Date": c_end.strftime("%Y-%m-%d"),
          "Campaign_Budget_USD": f"${budget:,.2f}",
          "Impressions": imp,
          "Clicks": clk,
          "CTR (%)": f"{actual_ctr}%",
          "Conversions_14Day": conv_14d,
          "Has_Churned": has_churned,
      })

    df = pd.DataFrame(rows)
    df.to_csv(self.config["output_csv_path"], index=False)
    print(
        f"Génération réussie : {len(df)} lignes exportées dans"
        f" '{self.config['output_csv_path']}'."
    )
    return df


# ==============================================================================
# 3. EXÉCUTION DU SCRIPT
# ==============================================================================
if __name__ == "__main__":
  # Vous pouvez instancier le générateur et modifier les paramètres à la volée :
  generator = WalmartConnectDataGenerator(
      config=DEFAULT_CONFIG, campaigns=WALMART_CAMPAIGNS_CONFIG
  )

  # Exemple de modification d'un paramètre avant l'exécution :
  # generator.config["num_records"] = 10000 # Pour générer 10 000 lignes
  # generator.config["metrics"]["ctr_min"] = 0.005 # Modifier le CTR minimal

  df_generated = generator.generate_dataset()