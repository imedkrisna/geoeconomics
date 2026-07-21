"""membangun GeoV dan GeoC ekspor Indonesia dari nol.

Resep (Aiyar & Ohnsorge 2024, NCAER WP 173):
  1. Bobot   : w_j = pangsa mitra j dalam ekspor Indonesia (UN Comtrade,
               data/idn_bilateral_trade.csv — reporter 360, cmdCode TOTAL).
  2. Jarak   : d_j = |p_IDN - p_j|, dengan p = IdealPointFP dari voting UNGA
               (Bailey, Strezhnev & Voeten; data/ideal_points_1946_2025.tab).
  3. GeoV    : rata-rata tertimbang    GeoV = sum_j w_j d_j.
  4. GeoC    : simpangan baku tertimbang
               GeoC = sqrt( N/(N-1) * sum_j w_j (d_j - GeoV)^2 ).

Validasi: seri terbitan Aiyar & Ohnsorge (data/GeoVGeoC.tab, Harvard
Dataverse doi:10.7910/DVN/PGCQVD, kolom GeoV_exports / GeoC_exports untuk
Indonesia). Seri DIY tidak akan persis sama: vintage ideal points, sumber
bobot, dan cakupan mitra berbeda — itulah pelajaran replikasinya.

Output: figures/geo_vc_diy.png
"""

from pathlib import Path

import numpy as np
import pandas as pd
import fig_den as den

ROOT = Path(__file__).resolve().parents[1]
SLIDE_BG = "#f0f1eb"

trade = pd.read_csv(ROOT / "data" / "idn_bilateral_trade.csv")
ip = pd.read_csv(ROOT / "data" / "ideal_points_1946_2025.tab", sep="\t")
ip = ip[["iso3c", "year", "IdealPointFP"]].dropna()

exp = trade[(trade["flowCode"] == "X") & (trade["partnerCode"] != 0)].copy()

# Bikin loop per tahun untuk ngitung GeoV dan GeoC ekspor Indonesia
rows = []
for year, g in exp.groupby("refYear"): # ngambil ideal point untuk tiap negara tujuan ekspor tiap taun.
    p = ip[ip["year"] == year].set_index("iso3c")["IdealPointFP"]
    if "IDN" not in p.index:
        continue
    g = g[g["iso3"].isin(p.index) & (g["iso3"] != "IDN")]
    total = exp.loc[exp["refYear"] == year, "primaryValue"].sum()
    covered = g["primaryValue"].sum() / total  # cakupan mitra yang punya ideal point untuk normalisasi bobot
    w = g["primaryValue"] / g["primaryValue"].sum()  # renormalisasi bobot
    d = (p["IDN"] - p.loc[g["iso3"]]).abs().to_numpy() 
    geov = float((w.to_numpy() * d).sum())
    n = len(g)
    geoc = float(np.sqrt(n / (n - 1) * (w.to_numpy() * (d - geov) ** 2).sum()))
    rows.append({"year": year, "GeoV": geov, "GeoC": geoc,
                 "n_partners": n, "coverage": covered})

diy = pd.DataFrame(rows).set_index("year").sort_index()

pub = pd.read_csv(ROOT / "data" / "GeoVGeoC.tab", sep="\t") # Karena .tab jadinya perlu dikasi tau separatornya pake `sep="\t"`
pub = (pub[pub["country"] == "Indonesia"]
       .set_index("year")[["GeoV_exports", "GeoC_exports"]]
       .dropna().sort_index())
pub = pub[pub.index <= 2023]

den.style()
fig, (axV, axC) = den.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor(SLIDE_BG)

for ax, col_diy, col_pub, ttl in [
        (axV, "GeoV", "GeoV_exports", "A | GeoV ekspor: rata-rata tertimbang jarak"),
        (axC, "GeoC", "GeoC_exports", "B | GeoC ekspor: simpangan baku tertimbang")]:
    ax.plot(diy.index, diy[col_diy], color=den.BRIGHT_GOLD, lw=2.6,
            marker="o", ms=3, label="DIY (sesi ini)")
    ax.plot(pub.index, pub[col_pub], color=den.RED, lw=2.0, ls="--",
            label="Aiyar & Ohnsorge (2024)")
    ax.axvline(2016, color=den.MEDIUM_GREY, ls=":", lw=1, alpha=0.7)
    ax.set_title(ttl, fontsize=11, fontweight="bold", loc="left")
    ax.set_facecolor(SLIDE_BG)
    ax.grid(False)
    ax.legend(frameon=False)

fig.suptitle("GeoV & GeoC ekspor Indonesia: hitungan sendiri vs terbitan",
             fontsize=13, fontweight="bold", x=0.012, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.94])
den.save(fig, ROOT / "figures" / "geo_vc_diy.png")

cmp_years = [y for y in (2002, 2016, 2023) if y in diy.index]
print("Perbandingan DIY vs terbitan (ekspor):")
for y in cmp_years:
    pv = pub.loc[y] if y in pub.index else pd.Series(dtype=float)
    print(f"  {y}: GeoV DIY {diy.loc[y,'GeoV']:.2f} vs pub "
          f"{pv.get('GeoV_exports', float('nan')):.2f} | "
          f"GeoC DIY {diy.loc[y,'GeoC']:.2f} vs pub "
          f"{pv.get('GeoC_exports', float('nan')):.2f}")
print(f"\nCakupan nilai ekspor dengan ideal point: "
      f"{diy['coverage'].min():.0%}-{diy['coverage'].max():.0%} "
      f"({diy['n_partners'].min()}-{diy['n_partners'].max()} mitra)")
