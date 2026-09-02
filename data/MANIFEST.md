# Manifest del ponte dati

Aggiornamento: **2026-09-02 10:13 UTC**

Fonte macro: **FRED API ufficiale**

Riuscite: 43 · Fallite: 1

Una serie FALLITA e' un dato ASSENTE: non va imputato, non va sostituito con un proxy, va dichiarato assente nel run.

```
========================================================================
SONDAGGIO FONTI MACRO — quale risponde da questo runner?
========================================================================
  FRED API ufficiale     HTTP 200    0.4s    88931 byte  UTILIZZABILE
  FRED fredgraph         FALLITO dopo  25.2s  ReadTimeout
  DBnomics v22           HTTP 404    0.5s      307 byte  nessuna serie nella risposta
  DBnomics search        HTTP 200    0.7s      131 byte  nessuna serie nella risposta

  --> fonte macro scelta: FRED API ufficiale

========================================================================
PRELIEVO MACRO — 41 serie via FRED API ufficiale
========================================================================
[ 1/41] OK      UNRATE                943 oss.  1948-01-01 -> 2026-07-01  (0.3s)
[ 2/41] OK      CIVPART               943 oss.  1948-01-01 -> 2026-07-01  (0.3s)
[ 3/41] OK      PAYEMS               1051 oss.  1939-01-01 -> 2026-07-01  (0.3s)
[ 4/41] OK      ICSA                 3112 oss.  1967-01-07 -> 2026-08-22  (0.2s)
[ 5/41] OK      CCSA                 3111 oss.  1967-01-07 -> 2026-08-15  (0.3s)
[ 6/41] OK      GDPC1                 318 oss.  1947-01-01 -> 2026-04-01  (0.2s)
[ 7/41] OK      INDPRO               1291 oss.  1919-01-01 -> 2026-07-01  (0.3s)
[ 8/41] OK      PNFI                  322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[ 9/41] OK      NEWORDER              702 oss.  1968-02-01 -> 2026-07-01  (0.3s)
[10/41] OK      CPIAUCSL              955 oss.  1947-01-01 -> 2026-07-01  (0.2s)
[11/41] OK      CPILFESL              835 oss.  1957-01-01 -> 2026-07-01  (0.2s)
[12/41] OK      PCEPILFE              811 oss.  1959-01-01 -> 2026-07-01  (0.4s)
[13/41] OK      PCEPI                 811 oss.  1959-01-01 -> 2026-07-01  (0.3s)
[14/41] OK      FEDFUNDS              866 oss.  1954-07-01 -> 2026-08-01  (0.2s)
[15/41] OK      TB3MS                1112 oss.  1934-01-01 -> 2026-08-01  (0.4s)
[16/41] OK      GS1                   881 oss.  1953-04-01 -> 2026-08-01  (0.2s)
[17/41] OK      GS2                   603 oss.  1976-06-01 -> 2026-08-01  (0.2s)
[18/41] OK      GS10                  881 oss.  1953-04-01 -> 2026-08-01  (0.3s)
[19/41] OK      T10Y3M              11652 oss.  1982-01-04 -> 2026-09-01  (0.3s)
[20/41] OK      T10Y2Y              13111 oss.  1976-06-01 -> 2026-09-01  (0.2s)
[21/41] OK      SP500                2608 oss.  2016-09-02 -> 2026-09-01  (0.2s)
[22/41] OK      CP                    322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[23/41] OK      CPATAX                322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[24/41] OK      AAA                  1292 oss.  1919-01-01 -> 2026-08-01  (0.2s)
[25/41] OK      BAA                  1292 oss.  1919-01-01 -> 2026-08-01  (0.2s)
[26/41] OK      BAA10Y              10608 oss.  1986-01-02 -> 2026-08-31  (0.2s)
[27/41] OK      BUSLOANS              955 oss.  1947-01-01 -> 2026-07-01  (0.2s)
[28/41] OK      TOTBKCR              2799 oss.  1973-01-03 -> 2026-08-19  (0.2s)
[29/41] OK      BAMLH0A0HYM2          793 oss.  2023-09-04 -> 2026-08-31  (0.2s)
[30/41] OK      DRSFRMACBS            142 oss.  1991-01-01 -> 2026-04-01  (0.4s)
[31/41] OK      GFDEGDQ188S           241 oss.  1966-01-01 -> 2026-01-01  (0.3s)
[32/41] OK      NETEXP                322 oss.  1946-01-01 -> 2026-04-01  (0.2s)
[33/41] OK      DTWEXBGS             5390 oss.  2006-01-02 -> 2026-08-28  (0.2s)
[34/41] OK      JTSJOL                308 oss.  2000-12-01 -> 2026-07-01  (0.3s)
[35/41] OK      JTSQUR                308 oss.  2000-12-01 -> 2026-07-01  (0.2s)
[36/41] OK      VIXCLS               9565 oss.  1990-01-02 -> 2026-08-31  (0.2s)
[37/41] OK      DRTSCILM              146 oss.  1990-04-01 -> 2026-07-01  (0.2s)
[38/41] OK      CSUSHPINSA            618 oss.  1975-01-01 -> 2026-06-01  (0.4s)
[39/41] OK      MORTGAGE30US         2892 oss.  1971-04-02 -> 2026-08-27  (0.3s)
[40/41] OK      UMCSENT               885 oss.  1952-11-01 -> 2026-07-01  (0.2s)
[41/41] OK      NFCI                 2903 oss.  1971-01-08 -> 2026-08-21  (0.2s)

  scritte 41 serie in data/macro_serie.csv

========================================================================
SHILLER
========================================================================
  candidati trovati nella pagina: 0
  candidati totali da provare: 3
  OK      shiller ie_data      1868 righe  (0.4s)  https://img1.wsimg.com/blobby/go/e5e77e0b-59d1-44d9-ab25-476

========================================================================
KEN FRENCH
========================================================================
  OK      french 12 industry   5240 righe  (0.3s)
```
