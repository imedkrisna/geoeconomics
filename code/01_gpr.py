"""Geopolitical Risk Index: global, USA, Tiongkok, Indonesia.

Data: Caldara & Iacoviello (2022), "Measuring Geopolitical Risk", AER 112(4).
Download: https://www.matteoiacoviello.com/gpr_files/data_gpr_export.xls
(halaman data: https://www.matteoiacoviello.com/gpr.htm; salinan lokal:
data/gpr_raw.xls). Kolom: `GPR` (global, 1985-), `GPRH` (global historis,
1900-), `GPRC_<ISO3>` (44 negara, 1985-; share artikel surat kabar).

Output: figures/gpr_4series.png
  Panel A - GPR global (indeks, 1985:2019 = 100), 1985-2026.
  Panel B - GPRC untuk USA, CHN, IDN (share artikel), 1985-2026.
"""

from pathlib import Path

import pandas as pd

import os
import sys

# Pakai fig-den untuk DEN-style graph. matikan jika anda tidak mau pakai fig-den.
# bisa didownload di github.com/den-econ/fig-den
import fig_den as den

ROOT = Path(__file__).resolve().parents[1] # supaya root-nya ga perlu di-hard-coded
SLIDE_BG = "#f0f1eb"  # samakan dengan background slide saya. matikan jika anda punya kosmetik sendiri

raw = pd.read_excel(ROOT / "data" / "gpr_raw.xls", sheet_name="Sheet1") # read data
monthly = raw.set_index("month")[["GPR", "GPRC_USA", "GPRC_CHN", "GPRC_IDN"]]
monthly = monthly.dropna(subset=["GPR"])  # GPR & GPRC mulai 1985

# Bikin dictionary untuk event penting.

EVENTS = {pd.Timestamp("1991-01-01"): "Perang Teluk",
          pd.Timestamp("2001-09-01"): "9/11",
          pd.Timestamp("2003-03-01"): "Irak",
          pd.Timestamp("2022-02-01"): "Ukraina",
          pd.Timestamp("2023-10-01"): "7 Okt",
          pd.Timestamp("2026-03-01"): "Iran"}

den.style()             # Menggunakan den-style figures. matikan jika anda punya style sendiri
fig, (axA, axB) = den.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.patch.set_facecolor(SLIDE_BG)

axA.plot(monthly.index, monthly["GPR"], color=den.RED, lw=1.4)
axA.set_title("A | GPR global (indeks, 1985:2019 = 100)",
              fontsize=11, fontweight="bold", loc="left")

for col, lab, c in [("GPRC_USA", "USA", den.DARK_BROWN),
                    ("GPRC_CHN", "Tiongkok", den.SLATE_BLUE),
                    ("GPRC_IDN", "Indonesia", den.BRIGHT_GOLD)]:
    axB.plot(monthly.index, monthly[col], color=c, lw=1.2, label=lab)
axB.set_title("B | GPRC per negara (share artikel surat kabar)",
              fontsize=11, fontweight="bold", loc="left")
axB.legend(frameon=False, loc="upper left")

for ax in (axA, axB):
    ax.set_facecolor(SLIDE_BG)
    for yr, lab in EVENTS.items():
        ax.axvline(yr, color=den.MEDIUM_GREY, ls=":", lw=1, alpha=0.7)
    ax.grid(False)
# selang-seling tinggi label agar event yang berdekatan tidak tumpang tindih
for i, (dt, lab) in enumerate(EVENTS.items()):
    axA.annotate(lab, (dt, axA.get_ylim()[1] * (0.97 if i % 2 == 0 else 0.90)),
                 fontsize=8, color=den.MEDIUM_GREY, ha="center")

fig.suptitle("Geopolitical Risk Index, 1985-2026 (Caldara & Iacoviello 2022)",
             fontsize=13, fontweight="bold", x=0.012, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.96])
den.save(fig, ROOT / "figures" / "gpr_4series.png")

m10 = monthly.loc["2010":"2019"].mean()
m22 = monthly.loc["2022":].mean()
print("Rata-rata 2010-19 vs 2022-26:")
for col in monthly.columns:
    print(f"  {col:9s} {m10[col]:7.3f} -> {m22[col]:7.3f}  ({m22[col]/m10[col]:.2f}x)")
