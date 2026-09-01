import json
from datetime import datetime
import yfinance as yf

# Master Tracked Universe (45 Multi-Horizon Equities)
UNIVERSE = [
    # 1. Penny / Turnaround Stocks (Sub-₹100)
    {"ticker": "SUZLON.NS", "clean": "SUZLON", "name": "Suzlon Energy", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.12, "target_mult": 3.0, "thesis": "Debt-free balance sheet with multi-GW wind order book."},
    {"ticker": "RPOWER.NS", "clean": "RPOWER", "name": "Reliance Power", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.12, "target_mult": 3.0, "thesis": "Debt settlement and renewable power venture pivot."},
    {"ticker": "GTLINFRA.NS", "clean": "GTLINFRA", "name": "GTL Infrastructure", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 3 Months", "risk_pct": 0.15, "target_mult": 3.0, "thesis": "5G telecom small-cell tower tenancies."},
    {"ticker": "JPPOWER.NS", "clean": "JPPOWER", "name": "Jaiprakash Power", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.12, "target_mult": 3.0, "thesis": "Thermal plant turnaround & debt restructuring."},
    {"ticker": "SOUTHBANK.NS", "clean": "SOUTHBANK", "name": "South Indian Bank", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.10, "target_mult": 3.0, "thesis": "NPA cleanup lifting Return on Assets."},
    {"ticker": "IDEA.NS", "clean": "VI", "name": "Vodafone Idea", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "3 - 6 Months", "risk_pct": 0.15, "target_mult": 3.0, "thesis": "Equity infusion & 4G/5G capital expenditure."},
    {"ticker": "YESBANK.NS", "clean": "YESBANK", "name": "Yes Bank", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 5 Months", "risk_pct": 0.10, "target_mult": 3.0, "thesis": "Resolution of legacy bad debt book."},
    {"ticker": "HFCL.NS", "clean": "HFCL", "name": "HFCL Ltd", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.10, "target_mult": 3.0, "thesis": "5G optical fiber cables & defense exports."},
    {"ticker": "INFIBEAM.NS", "clean": "INFIBEAM", "name": "Infibeam Avenues", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "2 - 4 Months", "risk_pct": 0.12, "target_mult": 3.0, "thesis": "AI payment fraud detection & international growth."},
    {"ticker": "TRIDENT.NS", "clean": "TRIDENT", "name": "Trident Ltd", "cat": "penny", "horizon": "Turnaround / Penny (2-4M)", "timeframe": "3 - 5 Months", "risk_pct": 0.10, "target_mult": 3.0, "thesis": "US textile export demand revival."},

    # 2. Large Cap (6 - 18 Months)
    {"ticker": "HDFCBANK.NS", "clean": "HDFCBANK", "name": "HDFC Bank", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Post-merger loan-to-deposit normalization."},
    {"ticker": "RELIANCE.NS", "clean": "RELIANCE", "name": "Reliance Industries", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 15 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Telecom tariff expansion and retail monetization."},
    {"ticker": "ICICIBANK.NS", "clean": "ICICIBANK", "name": "ICICI Bank", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.07, "target_mult": 3.5, "thesis": "Top RoA and low credit cost among peers."},
    {"ticker": "LT.NS", "clean": "LT", "name": "Larsen & Toubro", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "9 - 18 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Multidecade high domestic/Middle-East order backlog."},
    {"ticker": "BHARTIARTL.NS", "clean": "BHARTIARTL", "name": "Bharti Airtel", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Strong ARPU compounding & enterprise cloud growth."},
    {"ticker": "TCS.NS", "clean": "TCS", "name": "Tata Consultancy Services", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "12 - 18 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Zero debt, high dividend yield and AI pipelines."},
    {"ticker": "TITAN.NS", "clean": "TITAN", "name": "Titan Company", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 14 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Indian jewelry formalization tailwind."},
    {"ticker": "SUNPHARMA.NS", "clean": "SUNPHARMA", "name": "Sun Pharmaceutical", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.07, "target_mult": 3.5, "thesis": "Global specialty pharma margin resilience."},
    {"ticker": "M&M.NS", "clean": "M&M", "name": "Mahindra & Mahindra", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Dominant SUV market share & farm equip cashflows."},
    {"ticker": "NTPC.NS", "clean": "NTPC", "name": "NTPC Ltd", "cat": "large", "horizon": "Long-Term (6-18M)", "timeframe": "6 - 12 Months", "risk_pct": 0.08, "target_mult": 3.5, "thesis": "Green hydrogen & renewable expansion."},

    # 3. Mid Cap (3 - 12 Months)
    {"ticker": "CUMMINSIND.NS", "clean": "CUMMINSIND", "name": "Cummins India", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Data center backup power & green engines."},
    {"ticker": "SOLARINDS.NS", "clean": "SOLARINDS", "name": "Solar Industries", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "4 - 8 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Pinaka rockets & global defense export orders."},
    {"ticker": "DIXON.NS", "clean": "DIXON", "name": "Dixon Tech", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 8 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "PLI beneficiary in smartphone & IT hardware."},
    {"ticker": "MAXHEALTH.NS", "clean": "MAXHEALTH", "name": "Max Healthcare", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Bed capacity addition and high ARPOB metrics."},
    {"ticker": "PERSISTENT.NS", "clean": "PERSISTENT", "name": "Persistent Systems", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "4 - 9 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Outperforming Tier-1 IT in US software deals."},
    {"ticker": "POLYCAB.NS", "clean": "POLYCAB", "name": "Polycab India", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Real estate boom and power cable dominance."},
    {"ticker": "MAZDOCK.NS", "clean": "MAZDOCK", "name": "Mazagon Dock", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 8 Months", "risk_pct": 0.07, "target_mult": 2.8, "thesis": "Submarine & destroyer manufacturing backlog."},
    {"ticker": "HDFCAMC.NS", "clean": "HDFCAMC", "name": "HDFC AMC", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "4 - 8 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Financialization of household equity SIP inflows."},
    {"ticker": "TRENT.NS", "clean": "TRENT", "name": "Trent Ltd", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Rapid Zudio store expansion & inventory turns."},
    {"ticker": "SUPREMEIND.NS", "clean": "SUPREMEIND", "name": "Supreme Industries", "cat": "mid", "horizon": "Positional (3-6W)", "timeframe": "4 - 9 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "National piping & infrastructure demand leader."},

    # 4. Small Cap (2 - 6 Months)
    {"ticker": "KAYNES.NS", "clean": "KAYNES", "name": "Kaynes Technology", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "2 - 5 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Aerospace, defense & OSAT semiconductor assembly."},
    {"ticker": "DATAREPAT.NS", "clean": "DATAREPAT", "name": "Data Patterns", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Fighter jet radar systems & avionics."},
    {"ticker": "ELECON.NS", "clean": "ELECON", "name": "Elecon Engineering", "cat": "small", "horizon": "Swing (3-8D)", "timeframe": "2 - 4 Months", "risk_pct": 0.05, "target_mult": 2.5, "thesis": "Global industrial gear market share expansion."},
    {"ticker": "GRAVITA.NS", "clean": "GRAVITA", "name": "Gravita India", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Mandatory battery scrap recycling regulations."},
    {"ticker": "KFINTECH.NS", "clean": "KFINTECH", "name": "KFin Tech", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "2 - 5 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Dominant RTA in mutual funds & global alternatives."},
    {"ticker": "TEGAIND.NS", "clean": "TEGAIND", "name": "Tega Industries", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Gold/copper mining mill liner repeat revenues."},
    {"ticker": "CERA.NS", "clean": "CERA", "name": "Cera Sanitaryware", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Premium housing renovation demand."},
    {"ticker": "NEWGEN.NS", "clean": "NEWGEN", "name": "Newgen Software", "cat": "small", "horizon": "Swing (3-8D)", "timeframe": "2 - 5 Months", "risk_pct": 0.05, "target_mult": 2.5, "thesis": "Banking workflow digital transformation SaaS."},
    {"ticker": "PNCINFRA.NS", "clean": "PNCINFRA", "name": "PNC Infratech", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "2 - 4 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Highway monetization deleveraging balance sheet."},
    {"ticker": "ACE.NS", "clean": "ACTIONIND", "name": "Action Construction (ACE)", "cat": "small", "horizon": "Positional (3-6W)", "timeframe": "3 - 6 Months", "risk_pct": 0.06, "target_mult": 2.8, "thesis": "Dominant mobile industrial crane manufacturer."},

    # 5. Active Swing (3 - 8 Trading Days)
    {"ticker": "BEL.NS", "clean": "BEL", "name": "Bharat Electronics", "cat": "swing", "horizon": "Swing (3-8D)", "timeframe": "4 - 8 Trading Days", "risk_pct": 0.04, "target_mult": 2.5, "thesis": "Flat Base breakout near 52-week highs."},
    {"ticker": "HAL.NS", "clean": "HAL", "name": "Hindustan Aeronautics", "cat": "swing", "horizon": "Swing (3-8D)", "timeframe": "5 - 10 Trading Days", "risk_pct": 0.04, "target_mult": 2.5, "thesis": "Cup & Handle pattern breakout on defense orders."},
    {"ticker": "COALINDIA.NS", "clean": "COALINDIA", "name": "Coal India", "cat": "swing", "horizon": "Swing (3-8D)", "timeframe": "3 - 7 Trading Days", "risk_pct": 0.04, "target_mult": 2.5, "thesis": "20-EMA pullback support with high dividend yield."},
    {"ticker": "ZOMATO.NS", "clean": "ZOMATO", "name": "Zomato Ltd", "cat": "swing", "horizon": "Swing (3-8D)", "timeframe": "5 - 12 Trading Days", "risk_pct": 0.04, "target_mult": 2.5, "thesis": "Blinkit quick commerce turning EBITDA positive."},
    {"ticker": "BSE.NS", "clean": "BSE", "name": "BSE Ltd", "cat": "swing", "horizon": "Swing (3-8D)", "timeframe": "4 - 9 Trading Days", "risk_pct": 0.04, "target_mult": 2.5, "thesis": "Ascending triangle breakout on derivatives volumes."}
]

def generate_recommendations():
    results = []
    tickers_str = " ".join([item["ticker"] for item in UNIVERSE])
    data = yf.download(tickers_str, period="5d", interval="1d", group_by="ticker", progress=False)

    for item in UNIVERSE:
        sym = item["ticker"]
        try:
            df = data[sym] if len(UNIVERSE) > 1 else data
            df = df.dropna()
            if df.empty:
                continue
            
            cmp = float(df["Close"].iloc[-1])
            risk_amt = cmp * item["risk_pct"]
            sl = round(cmp - risk_amt, 1)
            t1 = round(cmp + (risk_amt * item["target_mult"]), 1)
            t2 = round(cmp + (risk_amt * (item["target_mult"] + 1.5)), 1)
            
            entry_low = round(cmp * 0.98, 1)
            entry_high = round(cmp * 1.01, 1)
            
            results.append({
                "ticker": item["clean"],
                "name": item["name"],
                "cat": item["cat"],
                "horizon": item["horizon"],
                "timeframe": item["timeframe"],
                "cmp": round(cmp, 2),
                "entry": f"{entry_low} - {entry_high}",
                "t1": t1,
                "t2": t2,
                "sl": sl,
                "thesis": item["thesis"]
            })
        except Exception as e:
            print(f"Error fetching {sym}: {e}")

    output = {
        "last_updated": datetime.now().strftime("%d %b %Y, %I:%M %p IST"),
        "count": len(results),
        "data": results
    }

    with open("recommendations.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    generate_recommendations()
