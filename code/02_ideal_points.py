"""Latihan 2 — menarik dan membaca UNGA ideal points.

Data: Bailey, Strezhnev & Voeten (2017), "Estimating Dynamic State Preferences
from United Nations Voting Data", JCR 61(2). Update 1946-2025.

Cara download:
  1. Buka Harvard Dataverse doi:10.7910/DVN/LEJUQZ
     (https://doi.org/10.7910/DVN/LEJUQZ).
  2. Unduh file `Idealpointestimates1946-2025.tab` (format tab-separated).
  3. Simpan sebagai data/ideal_points_1946_2025.tab.
Kolom kunci: `iso3c` (kode negara), `year`, `IdealPointFP` (ideal point
dimensi pertama; makin tinggi = makin dekat ke tatanan liberal pimpinan AS).

Output: figures/ideal_points_sesi5.png
  Panel A - ideal point USA, CHN, IDN, AUS, 1946-2025.
  Panel B - jarak ideal point Indonesia ke AS dan ke Tiongkok.
"""

from pathlib import Path

import pandas as pd

import os
import sys

# Pakai fig-den lokal bila ada (repo: github.com/den-econ/fig-den);
# bila path tidak ada, Python otomatis memakai versi hasil pip install.
sys.path.insert(0, os.environ.get("FIG_DEN_PATH", r"C:\Users\imedk\fig-den"))
import fig_den as den

ROOT = Path(__file__).resolve().parents[1]
SLIDE_BG = "#f0f1eb"

COUNTRIES = {"USA": den.RED, "CHN": den.DARK_BROWN,
             "IDN": den.BRIGHT_GOLD, "AUS": den.TAN}

df = pd.read_csv(ROOT / "data" / "ideal_points_1946_2025.tab", sep="\t")
wide = (df[df["iso3c"].isin(COUNTRIES)]
        .pivot(index="year", columns="iso3c", values="IdealPointFP"))

dist = pd.DataFrame({
    "Indonesia-AS": (wide["IDN"] - wide["USA"]).abs(),
    "Indonesia-Tiongkok": (wide["IDN"] - wide["CHN"]).abs(),
})

den.style()
fig, (axA, axB) = den.subplots(2, 1, figsize=(10, 8), sharex=True)
fig.patch.set_facecolor(SLIDE_BG)

for iso, c in COUNTRIES.items():
    s = wide[iso].dropna()
    axA.plot(s.index, s.values, color=c, lw=2.2, label=iso)
axA.set_title("A | Ideal point (dim. 1): makin tinggi, makin dekat ke AS",
              fontsize=11, fontweight="bold", loc="left")
axA.legend(frameon=False, ncol=4, loc="upper left")

for col, c in [("Indonesia-AS", den.RED), ("Indonesia-Tiongkok", den.DARK_BROWN)]:
    s = dist[col].dropna()
    axB.plot(s.index, s.values, color=c, lw=2.2, label=col)
axB.set_title("B | Jarak ideal point Indonesia: $d_{IDN,j} = |p_{IDN} - p_j|$",
              fontsize=11, fontweight="bold", loc="left")
axB.legend(frameon=False, loc="upper left")

for ax in (axA, axB):
    ax.set_facecolor(SLIDE_BG)
    ax.grid(False)

fig.suptitle("UNGA ideal points (Bailey, Strezhnev & Voeten 2017), 1946-2025",
             fontsize=13, fontweight="bold", x=0.012, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.96])
den.save(fig, ROOT / "figures" / "ideal_points_sesi5.png")

latest = int(wide.dropna(how="all").index.max())
print(f"Tahun terakhir: {latest}")
print(wide.loc[latest].round(2).to_string())
print("\nJarak Indonesia, tahun terakhir:")
print(dist.loc[latest].round(2).to_string())
