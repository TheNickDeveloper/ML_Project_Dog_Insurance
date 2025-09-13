# 🐾 Pawtection – Dog Insurance Estimator

This Machine Learning project demonstrates how data science and interactive web applications can be applied to real-world decision-making—in this case, estimating third-party insurance premiums for dogs based on various risk factors.

## 🌐 Live Demo

🔗 [Try it on Streamlit](https://hkuptmbapawtection.streamlit.app/)

---

## 🎯 Project Objective

**Pawtection** is a mock insurance estimation platform designed to:

- Showcase data analysis and modeling applied to pet insurance underwriting.
- Provide a simple and intuitive UI for users to input pet details.
- Calculate **Estimated Biting Risk** and **Monthly Premium** based on historical behavior and demographic risk factors.

---

## 📊 Features

- Interactive web interface built with Streamlit.
- Input fields for:
  - Biting history
  - Gender
  - Breed category
  - Spay/Neuter status
  - Age
  - Borough of residence
- Real-time estimation of:
  - **Biting Risk Score (0–100)**
  - **Monthly Insurance Premium**

---

## 🧠 Behind the Scenes

This project includes:

- **Data Preparation & Cleaning** using pandas.
- **Exploratory Data Analysis (EDA)** to uncover trends.
- **Risk Scoring Algorithm** combining historical data and probabilistic adjustments.
- **Pricing Model** translating risk into premium estimates.
- UI/UX designed to simulate a real-world product quote experience.

---

## 📁 Repository Structure

```bash
PTMBA_Data_Analysis_Project/
│
├── app/                      # Streamlit application files
├── data/                     # Cleaned and raw datasets
├── model/                    # Risk scoring and pricing logic
├── analysis/                 # Jupyter notebooks for EDA and modeling
└── README.md                 # You're here!
