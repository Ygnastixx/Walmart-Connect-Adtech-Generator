# 🛒 Walmart Connect AdTech Data Generator & Churn Simulator

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un générateur et simulateur de données synthétiques paramétrable dédié à l'analyse de performance publicitaire (*AdTech*) et à la prédiction du désengagement des annonceurs (*Merchant/Advertiser Churn*) sur la plateforme **Walmart Connect**.

---

## 📌 À propos du Projet

Dans le secteur du *Retail Media*, comprendre la relation entre le rendement des campagnes publicitaires (CTR, CVR, Coût par Conversion) et la rétention des annonceurs est essentiel. 

Ce projet propose un cadre complet permettant de :
1. Ancrer des campagnes publicitaires synthétiques sur des données transactionnelles réelles de vente au détail.
2. Modéliser les variations de comportement publicitaire (CTR, CVR, CPM) selon les formats (*Sponsored Products*, *Sponsored Brands*, *Videos*), les canaux (*App*, *Desktop*, *Mobile Web*) et le calendrier promotionnel officiel de Walmart.
3. Simuler le risque de désengagement d'un annonceur (*Has_Churned*) selon une fonction logistique multi-critères liée à la dégradation du ROI.

---

## 📐 Méthodologie & Provenance des Données (*Data Lineage*)

Ce dépôt s'appuie sur une démarche d'**Ingénierie de Données Synthétiques** :

* **Données de référence (Ground Truth) :** Les catégories et noms de produits sont directement extraits d'un historique transactionnel réel (`Walmart_customer_purchases.csv`).
* **Calendrier Promotionnel :** Alignement strict des fenêtres temporelles de campagnes sur les événements commerciaux officiels de Walmart sur la période 2024-2025 (*Black Friday*, *Walmart+ Week*, *Back-to-School*, etc.).
* **Distribution AdTech :** Utilisation de distributions statistiques (ex: distribution Beta pour le CTR, variations pondérées de CPM/CVR) calibrées d'après les benchmarks publics récents de l'industrie Retail Media (*Pacvue, eMarketer, RMIQ*).

> **Mention de transparence / Citation des outils :**  
> La conception de la logique métier, la formalisation des règles de Churn et le paramétrage de l'architecture ont été conçus par l'auteur du dépôt. L'implémentation du code de génération et la modélisation statistique ont été affinées avec l'assistance d'un modèle d'IA (LLM).

---

## 📁 Structure du Dépôt

```text
├── config/             # Fichiers de configuration (JSON) pour les métriques de base
├── data/               # Dossier contenant le dataset source et le dataset généré
├── docs/               # Documentation détaillée des champs (Data Dictionary)
├── src/                # Modules Python du générateur (WalmartConnectDataGenerator)
├── main.py             # Script principal d'exécution
└── requirements.txt    # Dépendances du projet

```

---

## 🚀 Installation & Utilisation

### 1. Clonage du dépôt et installation des dépendances

```bash
git clone [https://github.com/Ygnastixx/Walmart-Connect-Adtech-Generator.git](https://github.com/Ygnastixx/Walmart-Connect-Adtech-Generator.git)
cd walmart-connect-adtech-generator
pip install -r requirements.txt

```

### 2. Générer le dataset par défaut

Exécutez le script principal pour générer le fichier CSV dans `data/output/` :

```bash
python main.py

```

### 3. Personnaliser les paramètres de simulation

Vous pouvez ajuster les paramètres de simulation (taux de CTR de base, budgets min/max, seuils de déclenchement du churn) directement dans le dictionnaire de configuration ou via `config/config.json` :

```python
from src.generator import WalmartConnectDataGenerator

# Exemple de personnalisation
custom_config = {
    "num_records": 10000,               # Ajuster le nombre de campagnes
    "metrics": {
        "ctr_min": 0.005,                # Modifier le CTR minimal
    }
}

generator = WalmartConnectDataGenerator(config=custom_config)
df = generator.generate_dataset()

```

---

## 📑 Dictionnaire des Données

La documentation complète de chaque variable et de sa règle de calcul est disponible dans le fichier [docs/DATASET_DOCUMENTATION.md](https://github.com/Ygnastixx/Walmart-Connect-Adtech-Generator/blob/main/docs/DATASET_DOCUMENTATION.md).

| Champ | Type | Description |
| --- | --- | --- |
| `Advertiser_ID` | String | Identifiant anonymisé de l'annonceur |
| `Walmart_Promotional_Event` | String | Événement marketing officiel associé |
| `Campaign_Type` | String | Format (*Sponsored Products / Brands / Videos*) |
| `CTR (%)` | Float | Taux de clic généré |
| `Conversions_14Day` | Integer | Ventes attribuées sous 14 jours |
| `Has_Churned` | Binary | Target : 1 si l'annonceur s'est désengagé, 0 sinon |


### 🎯 Cas d'Usage Complémentaire : Analyse Croisée AdTech & Rétention Client (CRM)

En croisant ce dataset avec le fichier transactionnel source (`Walmart_customer_purchases.csv`), le projet permet d'explorer des problématiques avancées d'attribution et de fidélisation :

* **Segmentation & Ciblage :** Identifier quels formats publicitaires (*Sponsored Brands, Videos, Products*) impactent le plus la récurrence d'achat des segments clients à haute valeur.
* **Prévention du Churn Client :** Détecter les segments de clientèle en déclin d'activité et simuler l'impact de campagnes de reconquête (*Win-back campaigns*) sur leur panier moyen.
* **Optimisation des Budgets Média :** Déterminer la combinaison Canaux / Formats offrant le meilleur ROI de rétention selon les catégories de produits.
