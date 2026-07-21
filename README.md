# Pengukuran Pengaruh Geopolitik terhadap Ekspor dan Impor Indonesia

Materi *capacity building* FGD Analytical Notes 2026, Bank Indonesia (DPKL).
Empat latihan hands-on menghitung indikator geoekonomi dari data publik:

| # | Indikator | Skrip | Output |
|---|---------|-------|--------|
| 1 | Geopolitical Risk Index: global, USA, CHN, IDN | `code/01_gpr.py` | `figures/gpr_4series.png` |
| 2 | Menarik & membaca UNGA ideal points | `code/02_ideal_points.py` | `figures/ideal_points_sesi5.png` |
| 3 | GeoV & GeoC ekspor Indonesia dari nol | `code/03_geo_vc.py` | `figures/geo_vc_diy.png` |
| 4 | HHI & Theil konsentrasi mitra dagang | `code/04_hhi_theil.py` | `figures/hhi_theil.png` |

Slide: `sesi5.qmd` (Quarto reveal.js, tema DEN).

## Struktur folder

```
sesi5/
  sesi5.qmd        # slide deck (quarto render sesi5.qmd)
  mytheme.scss     # tema reveal.js
  README.md
  code/            # empat skrip latihan, jalankan berurutan dari folder code/
  data/            # seluruh data input (sudah disertakan, ~9 MB)
  figures/         # output PNG
```

## Setup

1. Python (disarankan Anaconda) dengan `pandas`, `numpy`, `matplotlib`, `xlrd`
   (pembaca `.xls`): `pip install pandas numpy matplotlib xlrd`.
2. Gaya figur DEN, [fig-den](https://github.com/den-econ/fig-den):
   `pip install git+https://github.com/den-econ/fig-den` — atau clone lalu set
   env var `FIG_DEN_PATH` ke folder clone-nya. (Skrip otomatis memakai path
   lokal `C:\Users\imedk\fig-den` bila ada.)
3. [Quarto](https://quarto.org) untuk me-render slide.

## Menjalankan

```bash
cd code
python 01_gpr.py
python 02_ideal_points.py
python 03_geo_vc.py
python 04_hhi_theil.py
cd ..
quarto render sesi5.qmd
```

Setiap skrip mencetak ringkasan angka di konsol (angka yang dikutip di slide)
dan menyimpan satu PNG ke `figures/`.

## Data & sumber

Semua data input **sudah disertakan** di `data/`; tabel berikut mencatat
sumber resminya bila ingin memperbarui.

| File | Isi | Sumber & cara download |
|------|-----|------------------------|
| `gpr_raw.xls` | GPR global & 44 GPRC negara, bulanan 1900–2026 | Caldara & Iacoviello (2022): <https://www.matteoiacoviello.com/gpr.htm> → `data_gpr_export.xls` |
| `ideal_points_1946_2025.tab` | UNGA ideal points 1946–2025 | Bailey, Strezhnev & Voeten (2017), Harvard Dataverse <https://doi.org/10.7910/DVN/LEJUQZ> → `Idealpointestimates1946-2025.tab` |
| `idn_bilateral_trade.csv` | Ekspor-impor bilateral Indonesia (TOTAL, USD), 2000–2024 | UN Comtrade, reporter 360, cmdCode TOTAL — ekstrak kecil teragregasi; refresh via paket `comtradeapicall` + env var `COMTRADE_API_KEY` |
| `GeoVGeoC.tab` | Database GeoV/GeoC 188 ekonomi (validasi Latihan 3) | Aiyar & Ohnsorge (2024), NCAER WP 173, Harvard Dataverse <https://doi.org/10.7910/DVN/PGCQVD> |

## Atribusi

- Caldara, D. & M. Iacoviello (2022). Measuring geopolitical risk. *AER* 112(4).
- Bailey, M., A. Strezhnev & E. Voeten (2017). Estimating dynamic state
  preferences from United Nations voting data. *JCR* 61(2).
- Aiyar, S. & F. Ohnsorge (2024). Geoeconomic fragmentation and "connector"
  countries. NCAER WP 173.
- UN Comtrade (data perdagangan; ekstrak kecil untuk reproducibility).

Penulis: Krisna Gupta (Dewan Ekonomi Nasional) — [krisna.or.id](https://krisna.or.id).
