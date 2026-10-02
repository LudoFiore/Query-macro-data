# Manifest del ponte dati

Aggiornamento: **2026-10-02 11:37 UTC**

Fonte macro: **FRED API ufficiale**

Riuscite: 43 · Fallite: 1

Una serie FALLITA e' un dato ASSENTE: non va imputato, non va sostituito con un proxy, va dichiarato assente nel run.

```
========================================================================
SONDAGGIO FONTI MACRO — quale risponde da questo runner?
========================================================================
  FRED API ufficiale     HTTP 200    0.6s    89025 byte  UTILIZZABILE
  FRED fredgraph         FALLITO dopo  25.4s  ReadTimeout
  DBnomics v22           HTTP 404    0.5s      307 byte  nessuna serie nella risposta
  DBnomics search        HTTP 200    0.6s      131 byte  nessuna serie nella risposta

  --> fonte macro scelta: FRED API ufficiale

========================================================================
PRELIEVO MACRO — 41 serie via FRED API ufficiale
========================================================================
[ 1/41] OK      UNRATE                944 oss.  1948-01-01 -> 2026-08-01  (0.4s)
[ 2/41] OK      CIVPART               944 oss.  1948-01-01 -> 2026-08-01  (0.8s)
[ 3/41] OK      PAYEMS               1052 oss.  1939-01-01 -> 2026-08-01  (0.3s)
[ 4/41] OK      ICSA                 3117 oss.  1967-01-07 -> 2026-09-26  (0.3s)
[ 5/41] OK      CCSA                 3116 oss.  1967-01-07 -> 2026-09-19  (0.3s)
[ 6/41] OK      GDPC1                 318 oss.  1947-01-01 -> 2026-04-01  (0.3s)
[ 7/41] OK      INDPRO               1292 oss.  1919-01-01 -> 2026-08-01  (0.2s)
[ 8/41] OK      PNFI                  322 oss.  1946-01-01 -> 2026-04-01  (0.3s)
[ 9/41] OK      NEWORDER              703 oss.  1968-02-01 -> 2026-08-01  (0.3s)
[10/41] OK      CPIAUCSL              956 oss.  1947-01-01 -> 2026-08-01  (0.6s)
[11/41] OK      CPILFESL              836 oss.  1957-01-01 -> 2026-08-01  (0.4s)
[12/41] OK      PCEPILFE              812 oss.  1959-01-01 -> 2026-08-01  (0.2s)
[13/41] OK      PCEPI                 812 oss.  1959-01-01 -> 2026-08-01  (0.2s)
[14/41] OK      FEDFUNDS              867 oss.  1954-07-01 -> 2026-09-01  (0.2s)
[15/41] OK      TB3MS                1113 oss.  1934-01-01 -> 2026-09-01  (0.3s)
[16/41] OK      GS1                   882 oss.  1953-04-01 -> 2026-09-01  (0.2s)
[17/41] OK      GS2                   604 oss.  1976-06-01 -> 2026-09-01  (0.3s)
[18/41] OK      GS10                  882 oss.  1953-04-01 -> 2026-09-01  (0.4s)
[19/41] OK      T10Y3M              11674 oss.  1982-01-04 -> 2026-10-01  (0.3s)
[20/41] OK      T10Y2Y              13133 oss.  1976-06-01 -> 2026-10-01  (0.3s)
[21/41] OK      SP500                2609 oss.  2016-10-03 -> 2026-10-01  (0.3s)
[22/41] OK      CP                    322 oss.  1946-01-01 -> 2026-04-01  (0.4s)
[23/41] OK      CPATAX                322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[24/41] OK      AAA                  1293 oss.  1919-01-01 -> 2026-09-01  (0.3s)
[25/41] OK      BAA                  1293 oss.  1919-01-01 -> 2026-09-01  (0.3s)
[26/41] OK      BAA10Y              10630 oss.  1986-01-02 -> 2026-09-30  (0.3s)
[27/41] OK      BUSLOANS              956 oss.  1947-01-01 -> 2026-08-01  (0.3s)
[28/41] OK      TOTBKCR              2803 oss.  1973-01-03 -> 2026-09-16  (0.4s)
[29/41] OK      BAMLH0A0HYM2          794 oss.  2023-10-02 -> 2026-09-30  (0.3s)
[30/41] OK      DRSFRMACBS            142 oss.  1991-01-01 -> 2026-04-01  (0.5s)
[31/41] OK      GFDEGDQ188S           241 oss.  1966-01-01 -> 2026-01-01  (0.2s)
[32/41] OK      NETEXP                322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[33/41] OK      DTWEXBGS             5410 oss.  2006-01-02 -> 2026-09-25  (0.5s)
[34/41] OK      JTSJOL                309 oss.  2000-12-01 -> 2026-08-01  (0.3s)
[35/41] OK      JTSQUR                309 oss.  2000-12-01 -> 2026-08-01  (1.5s)
[36/41] OK      VIXCLS               9587 oss.  1990-01-02 -> 2026-09-30  (0.4s)
[37/41] OK      DRTSCILM              146 oss.  1990-04-01 -> 2026-07-01  (0.3s)
[38/41] OK      CSUSHPINSA            619 oss.  1975-01-01 -> 2026-07-01  (0.3s)
[39/41] OK      MORTGAGE30US         2897 oss.  1971-04-02 -> 2026-10-01  (0.3s)
[40/41] OK      UMCSENT               886 oss.  1952-11-01 -> 2026-08-01  (0.3s)
[41/41] OK      NFCI                 2908 oss.  1971-01-08 -> 2026-09-25  (0.4s)

  scritte 41 serie in data/macro_serie.csv

========================================================================
SHILLER
========================================================================
  candidati trovati nella pagina: 0
  candidati totali da provare: 3
  OK      shiller ie_data      1868 righe  (0.7s)  https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-476

========================================================================
KEN FRENCH
========================================================================
  OK      french 12 industry   5250 righe  (0.7s)
```
