# Manifest del ponte dati

Aggiornamento: **2026-08-07 14:33 UTC**

Fonte macro: **FRED API ufficiale**

Riuscite: 42 · Fallite: 2

Una serie FALLITA e' un dato ASSENTE: non va imputato, non va sostituito con un proxy, va dichiarato assente nel run.

```
========================================================================
SONDAGGIO FONTI MACRO — quale risponde da questo runner?
========================================================================
  FRED API ufficiale     HTTP 200    0.5s    88931 byte  UTILIZZABILE
  FRED fredgraph         FALLITO dopo  25.2s  ReadTimeout
  DBnomics v22           HTTP 404    0.7s      307 byte  nessuna serie nella risposta
  DBnomics search        HTTP 200    0.7s      131 byte  nessuna serie nella risposta

  --> fonte macro scelta: FRED API ufficiale

========================================================================
PRELIEVO MACRO — 41 serie via FRED API ufficiale
========================================================================
[ 1/41] OK      UNRATE                943 oss.  1948-01-01 -> 2026-07-01  (2.2s)
[ 2/41] OK      CIVPART               943 oss.  1948-01-01 -> 2026-07-01  (2.7s)
[ 3/41] OK      PAYEMS               1051 oss.  1939-01-01 -> 2026-07-01  (3.5s)
[ 4/41] OK      ICSA                 3109 oss.  1967-01-07 -> 2026-08-01  (1.1s)
[ 5/41] OK      CCSA                 3108 oss.  1967-01-07 -> 2026-07-25  (1.7s)
[ 6/41] OK      GDPC1                 318 oss.  1947-01-01 -> 2026-04-01  (1.6s)
[ 7/41] OK      INDPRO               1290 oss.  1919-01-01 -> 2026-06-01  (2.3s)
[ 8/41] OK      PNFI                  322 oss.  1946-01-01 -> 2026-04-01  (1.5s)
[ 9/41] OK      NEWORDER              701 oss.  1968-02-01 -> 2026-06-01  (1.3s)
[10/41] OK      CPIAUCSL              954 oss.  1947-01-01 -> 2026-06-01  (1.1s)
[11/41] OK      CPILFESL              834 oss.  1957-01-01 -> 2026-06-01  (1.2s)
[12/41] OK      PCEPILFE              810 oss.  1959-01-01 -> 2026-06-01  (0.6s)
[13/41] OK      PCEPI                 810 oss.  1959-01-01 -> 2026-06-01  (0.6s)
[14/41] OK      FEDFUNDS              865 oss.  1954-07-01 -> 2026-07-01  (0.3s)
[15/41] OK      TB3MS                1111 oss.  1934-01-01 -> 2026-07-01  (0.5s)
[16/41] OK      GS1                   880 oss.  1953-04-01 -> 2026-07-01  (0.2s)
[17/41] OK      GS2                   602 oss.  1976-06-01 -> 2026-07-01  (0.4s)
[18/41] OK      GS10                  880 oss.  1953-04-01 -> 2026-07-01  (0.2s)
[19/41] OK      T10Y3M              11634 oss.  1982-01-04 -> 2026-08-06  (1.1s)
[20/41] OK      T10Y2Y              13093 oss.  1976-06-01 -> 2026-08-06  (0.3s)
[21/41] OK      SP500                2609 oss.  2016-08-08 -> 2026-08-06  (0.2s)
[22/41] OK      CP                    321 oss.  1946-01-01 -> 2026-01-01  (2.2s)
[23/41] OK      CPATAX                321 oss.  1946-01-01 -> 2026-01-01  (0.9s)
[24/41] OK      AAA                  1291 oss.  1919-01-01 -> 2026-07-01  (0.6s)
[25/41] OK      BAA                  1291 oss.  1919-01-01 -> 2026-07-01  (0.7s)
[26/41] OK      BAA10Y              10590 oss.  1986-01-02 -> 2026-08-05  (0.3s)
[27/41] OK      BUSLOANS              954 oss.  1947-01-01 -> 2026-06-01  (0.3s)
[28/41] OK      TOTBKCR              2795 oss.  1973-01-03 -> 2026-07-22  (0.3s)
[29/41] OK      BAMLH0A0HYM2          795 oss.  2023-08-07 -> 2026-08-05  (0.3s)
[30/41] OK      DRSFRMACBS            141 oss.  1991-01-01 -> 2026-01-01  (0.4s)
[31/41] OK      GFDEGDQ188S           241 oss.  1966-01-01 -> 2026-01-01  (0.2s)
[32/41] OK      NETEXP                322 oss.  1946-01-01 -> 2026-04-01  (0.3s)
[33/41] OK      DTWEXBGS             5370 oss.  2006-01-02 -> 2026-07-31  (0.8s)
[34/41] OK      JTSJOL                307 oss.  2000-12-01 -> 2026-06-01  (0.2s)
[35/41] OK      JTSQUR                307 oss.  2000-12-01 -> 2026-06-01  (0.2s)
[36/41] OK      VIXCLS               9548 oss.  1990-01-02 -> 2026-08-06  (0.5s)
[37/41] OK      DRTSCILM              146 oss.  1990-04-01 -> 2026-07-01  (0.3s)
[38/41] OK      CSUSHPINSA            617 oss.  1975-01-01 -> 2026-05-01  (0.3s)
[39/41] OK      MORTGAGE30US         2889 oss.  1971-04-02 -> 2026-08-06  (0.2s)
[40/41] OK      UMCSENT               884 oss.  1952-11-01 -> 2026-06-01  (0.8s)
[41/41] OK      NFCI                 2900 oss.  1971-01-08 -> 2026-07-31  (0.2s)

  scritte 41 serie in data/macro_serie.csv

========================================================================
SHILLER
========================================================================
  candidati trovati nella pagina: 0
  FALLITA shiller            RuntimeError: nessun link .xls nell'HTML grezzo (pagina resa via JS?)

========================================================================
KEN FRENCH
========================================================================
  OK      french 12 industry   5240 righe  (1.0s)
```
