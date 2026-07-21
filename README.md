# Pengukuran Pengaruh Geopolitik terhadap Ekspor dan Impor Indonesia

Repository ini mencoba menunjukkan bagaimana mencari dan menggunakan data-data terkait geoeconomics. In total ada 4 indikator:

| # | Indikator | Skrip | Output |
|---|---------|-------|--------|
| 1 | Geopolitical Risk Index: global, USA, CHN, IDN | `code/01_gpr.py` | `figures/gpr_4series.png` |
| 2 | Menarik & membaca UNGA ideal points | `code/02_ideal_points.py` | `figures/ideal_points_sesi5.png` |
| 3 | GeoV & GeoC ekspor Indonesia dari nol | `code/03_geo_vc.py` | `figures/geo_vc_diy.png` |
| 4 | HHI & Theil konsentrasi mitra dagang | `code/04_hhi_theil.py` | `figures/hhi_theil.png` |

Slide: `index.qmd` (Quarto reveal.js, tema DEN) yang dirender jadi `index.html`

## Struktur folder

```
geoeconomics/
  index.qmd        # slide deck (quarto render index.qmd)
  mytheme.scss     # tema reveal.js
  README.md
  code/            # empat skrip latihan, jalankan berurutan dari folder code/
  data/            # seluruh data input (sudah disertakan, ~9 MB)
  figures/         # output PNG
```

## Setup

Semuanya diplot dengan menggunakan `python` tapi tentu anda bisa juga menggunakan alat lain seperti Excel, R, ataupun Stata.
Repo ini menggunakan Python (lebih spesifiknya Anaconda distribution) dengan `pandas`, `numpy`, `matplotlib`, `xlrd`
   (pembaca `.xls`): `pip install pandas numpy matplotlib xlrd`.


## Menjalankan

Anda bisa jalankan satu persatu, tapi bisa juga langsung jalankan semua dengan command prompt. Nanti resultsnya masuk ke "figures".

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

Semua data input sudah disertakan di `data/`. Tabel berikut mencatat sumber resminya bila ingin memperbarui.

| File | Isi | Sumber & cara download |
|------|-----|------------------------|
| `gpr_raw.xls` | GPR global & 44 GPRC negara, bulanan 1900–2026 | Caldara & Iacoviello (2022): <https://www.matteoiacoviello.com/gpr.htm> → `data_gpr_export.xls` |
| `ideal_points_1946_2025.tab` | UNGA ideal points 1946–2025 | Bailey, Strezhnev & Voeten (2017), Harvard Dataverse <https://doi.org/10.7910/DVN/LEJUQZ> → `Idealpointestimates1946-2025.tab` |
| `idn_bilateral_trade.csv` | Ekspor-impor bilateral Indonesia (TOTAL, USD), 2000–2024 | UN Comtrade, reporter 360, cmdCode TOTAL — ekstrak kecil teragregasi; refresh via paket `comtradeapicall` + env var `COMTRADE_API_KEY` |
| `GeoVGeoC.tab` | Database GeoV/GeoC 188 ekonomi (validasi Latihan 3) | Aiyar & Ohnsorge (2024), NCAER WP 173, Harvard Dataverse <https://doi.org/10.7910/DVN/PGCQVD> |

## Referensi

- Caldara, D. & M. Iacoviello (2022). Measuring geopolitical risk. *AER* 112(4).
- Bailey, M., A. Strezhnev & E. Voeten (2017). Estimating dynamic state
  preferences from United Nations voting data. *JCR* 61(2).
- Aiyar, S. & F. Ohnsorge (2024). Geoeconomic fragmentation and "connector"
  countries. NCAER WP 173.
- UN Comtrade (data perdagangan; perbarui dengan mendownload dari sini atau sumber lain).

Penulis: Krisna Gupta  — [krisna.or.id](https://krisna.or.id).
