# **Historical Multiple App**

## **Overview**

This project began as a personal initiative to simplify and speed up how my colleagues and I analyzed company price data.  
Many of us wanted to invest but didn’t have the time or tools to compare prices, read multiple company reports, or handle a flood of financial metrics.  
To solve that, I built this Python application — a lightweight, user-friendly tool that helps users quickly understand how a company’s current price compares to its historical performance.

The app provides contextual insights on price behavior over time: it shows how much higher or lower the current price is compared to the company’s historical averages, and suggests potential buy thresholds based on past data performance.  
It has already been used by hundreds of my colleagues, who found it helpful for developing early financial literacy and making more informed decisions.

---

## **What the App Does**

The **Historical Multiple App** retrieves company price data, computes moving averages, and evaluates how the current market price compares with historical patterns.  
It then estimates the historical “multiple” (current price divided by its 50-day average) and analyzes what typical future returns followed when the company traded at similar levels.

**In simpler terms:**
- It tells whether a stock is relatively expensive or cheap compared to its own past.  
- It calculates median future returns for different time horizons (180 and 360 days).  
- It identifies thresholds where historical data suggests the best buy opportunities occurred.

This makes it a practical decision-support tool for students, beginners, or anyone learning how to read the market historically rather than emotionally.

---

## **Technical Details**

- **Language:** Python  
- **Interface:** Built using the Flet library for designing cross-platform apps (desktop, web, and mobile).  
- **Data Source:** Yahoo Finance API, which provides historical price data and company information.  
- **Core Logic:** Uses pandas, NumPy, and datetime to compute moving averages, relative multiples, and median forward returns.  
- **App Design:** Modular and reactive — when you input a ticker (e.g., `AAPL` or `PETR4`), the app dynamically fetches, processes, and visualizes results.

---

## **How It Works (Step by Step)**

**1. Data Retrieval**  
The app fetches full historical data for a given ticker from Yahoo Finance. It automatically adjusts for local formats (e.g., `.SA` suffix for Brazilian markets).

**2. Data Processing**  
A 50-day moving average is computed, and the ratio between current price and that average is treated as the *Historical Multiple* — a dynamic measure of price position.

**3. Statistical Analysis**  
Using median future returns across historical multiples, the program identifies *optimal buy zones* — price levels historically followed by higher average returns.

**4. Interface and Output**  
The user interface is interactive and simple, displaying:
- Current and average prices  
- Historical multiple comparison  
- Percentage of time current price was higher/lower than historical norms  
- Suggested thresholds for long-term gains (180- and 360-day horizons)

---

## **Structure of the Repository**

```
/
│
├── main.py              # The complete Python source code
├── assets/              # Folder containing icon image and other visual assets
│   └── favicon.jpg
├── requirements.txt     # Dependencies required to run the app
├── app_en.py            # English version of the app (optional)
└── app_pt.py            # Portuguese version (original)
```

---

## **Running the App**

To run locally:
```
pip install -r requirements.txt
python main.py
```


The design will render directly in your terminal or browser window via Flet’s built-in environment — no heavy setup required.

---

## **Deployment and Build Options**

Flet allows you to build native executables or mobile apps effortlessly.  
To build an application file, use:
flet build [desired_format]
flet build apk

If you face dependency issues related to Flutter or Flet, reinstalling the required Flutter files and dependencies typically resolves them.

---

## **Final Remarks**

This project reflects how I approach learning and building: I create tools when I need or want to see them exist.  
I learn by building — and every iteration deepens both my technical and conceptual understanding.  
If you notice opportunities to improve or extend this project, your feedback would be truly welcome.

Thank you for taking the time to explore this work.

---

**Author:** Matheus Tinta  
**Year:** 2024  
**Language:** Python  
**Libraries Used:** Flet, yfinance, pandas, numpy, datetime
