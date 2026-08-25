# 🏥 Healthcare Accessibility in Greater Accra

> **Project Summary**
>
> This project analyzes healthcare accessibility across the **Greater Accra Region of Ghana** by estimating the population that can reach a healthcare facility within an **8-minute travel time** using road network analysis.

---

## 📊 Key Results

Using **274 healthcare facilities**, OpenStreetMap road data, and **WorldPop (2020)** population data, the analysis found:

| Accessibility       |    Population |      Share |
| ------------------- | ------------: | ---------: |
| 🟢 Within 8 minutes | **4,405,459** | **82.38%** |
| 🔴 Beyond 8 minutes |   **942,344** | **17.62%** |
| **Total**           | **5,347,803** |   **100%** |

### Key takeaway

**82.38% of the Greater Accra population can reach a healthcare facility within 8 minutes, while 17.62% remain outside the accessibility threshold.**

---

## 🛠️ Methodology

The analysis followed a geospatial accessibility workflow:

1. **Healthcare & Road Data**

   * Retrieved healthcare facilities and road network data using **OSMnx**.

2. **Spatial Data Preparation**

   * Cleaned and reprojected spatial datasets to **EPSG:32630**.

3. **Travel-Time Modeling**

   * Calculated road travel speeds and estimated travel times across the road network.

4. **Isochrone Analysis**

   * Generated **8-minute travel-time isochrones** around healthcare facilities.

5. **Population Analysis**

   * Clipped **WorldPop 2020** population data to the Greater Accra Region.

6. **Accessibility Estimation**

   * Estimated the population **within and outside** the 8-minute healthcare accessibility zones.

---

## 🔍 Key Findings

### 🟢 High Overall Accessibility

Out of a total population of **5,347,803**, approximately **4.4 million residents** have access to a healthcare facility within an 8-minute travel time.

### 🔴 Persistent Accessibility Gap

Approximately **942,000 residents** live beyond the 8-minute accessibility threshold, representing **17.62% of the regional population**.

### 🗺️ Spatial Concentration

Healthcare accessibility is highest in the **western part of Greater Accra**, where both **population density and healthcare facility concentration** are greatest.

This highlights an important spatial relationship between the distribution of healthcare facilities, population concentration, and travel-time accessibility.

---

## 💡 Recommendations

Although overall healthcare coverage is relatively high, nearly **one in five residents** remains outside the 8-minute accessibility threshold.

To improve spatial equity in healthcare access, policymakers and healthcare planners should prioritize underserved areas through:

* 🏥 **Establishing new healthcare facilities** in locations with low accessibility.
* 🛣️ **Improving road infrastructure** to reduce travel times to existing facilities.

---

## 🌍 Project Significance

This project demonstrates how **geospatial analysis, road-network modeling, and population data** can support evidence-based healthcare planning.

By identifying areas where populations experience longer travel times to healthcare facilities, geospatial methods can help decision-makers:

> **Identify accessibility gaps → Prioritize underserved communities → Allocate healthcare resources more effectively**

Ultimately, the analysis provides a spatially informed approach to understanding and improving **equitable healthcare access across Greater Accra**.
