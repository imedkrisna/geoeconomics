"""Latihan 4 — HHI dan Theil: konsentrasi mitra dagang Indonesia.

Data: UN Comtrade (data/idn_bilateral_trade.csv — reporter 360=Indonesia,
cmdCode TOTAL, 2000-2024, flowCode X=ekspor / M=impor; baris partnerCode==0
adalah total dunia). Refresh via `comtradeapicall` + $COMTRADE_API_KEY.

Rumus (s_j = pangsa mitra j, N = jumlah mitra bernilai positif):
  HHI   = sum_j s_j^2 * 10.000          (10.000 = satu mitra; 10.000/N merata)
  Theil = sum_j s_j ln(N s_j)           (0 = merata; ln N = satu mitra)

Catatan: kode mitra khusus Comtrade ("areas nes" dsb.) tetap dihitung
sebagai mitra; pengaruhnya kecil pada level agregat.

Output: figures/hhi_theil.png (panel A HHI, panel B Theil; ekspor & impor)
"""

from pathlib import Path

import numpy as np
import pandas as pd

import os
import sys

# Pakai fig-den lokal bila ada (repo: github.com/den-econ/fig-den);
# bila path tidak ada, Python otomatis memakai versi hasil pip install.
sys.path.insert(0, os.environ.get("FIG_DEN_PATH", r"C:\Users\imedk\fig-den"))
import fig_den as den

ROOT = Path(__file__).resolve().parents[1]
SLIDE_BG = "#f0f1eb"

trade = pd.read_csv(ROOT / "data" / "idn_bilateral_trade.csv")
trade = trade[trade["partnerCode"] != 0]  # buang baris total dunia


def concentration(values):
    """HHI (x10.000) dan Theil dari satu vektor nilai transaksi per mitra."""
    v = values[values > 0]
    s = v / v.sum()
    hhi = float((s ** 2).sum() * 10_000)
    theil = float((s * np.log(len(s) * s)).sum())
    return hhi, theil, len(s)


rows = []
for (year, flow), g in trade.groupby(["refYear", "flowCode"]):
    hhi, theil, n = concentration(g["primaryValue"])
    rows.append({"year": year, "flow": flow, "HHI": hhi, "Theil": theil, "N": n})
res = pd.DataFrame(rows).pivot(index="year", columns="flow",
                               values=["HHI", "Theil", "N"]).sort_index()

den.style()
fig, (axH, axT) = den.subplots(1, 2, figsize=(13, 5.5))
fig.patch.set_facecolor(SLIDE_BG)

FLOWS = {"X": ("Ekspor", den.BRIGHT_GOLD), "M": ("Impor", den.RED)}
for metric, ax, ttl in [("HHI", axH, "A | HHI mitra dagang (0-10.000)"),
                        ("Theil", axT, "B | Theil mitra dagang (0-ln N)")]:
    for f, (lab, c) in FLOWS.items():
        ax.plot(res.index, res[(metric, f)], color=c, lw=2.4,
                marker="o", ms=3, label=lab)
    ax.axvline(2016, color=den.MEDIUM_GREY, ls=":", lw=1, alpha=0.7)
    ax.set_title(ttl, fontsize=11, fontweight="bold", loc="left")
    ax.set_facecolor(SLIDE_BG)
    ax.grid(False)
    ax.legend(frameon=False)

fig.suptitle("Konsentrasi mitra dagang Indonesia, 2000-2024 (UN Comtrade, total trade)",
             fontsize=13, fontweight="bold", x=0.012, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.94])
den.save(fig, ROOT / "figures" / "hhi_theil.png")

print("HHI / Theil, 2016 vs 2024:")
for f, (lab, _) in FLOWS.items():
    for y in (2016, 2024):
        hhi = res.loc[y, ("HHI", f)]
        print(f"  {lab:6s} {y}: HHI {hhi:7.0f} (mitra efektif ~{10_000/hhi:.1f}), "
              f"Theil {res.loc[y, ('Theil', f)]:.3f}")

print("\nTop-5 mitra 2024:")
for f, (lab, _) in FLOWS.items():
    g = trade[(trade["refYear"] == 2024) & (trade["flowCode"] == f)]
    top = g.nlargest(5, "primaryValue")
    tot = g["primaryValue"].sum()
    shares = ", ".join(f"{r.iso3} {r.primaryValue/tot:.1%}" for r in top.itertuples())
    print(f"  {lab}: {shares}")
