---
title:
  'Online Appendix: The labor market integration of immigrant women in Europe. A review.'
subtitle: "Version <b>0.2.3</b>"
date: "2021-08-05"
titleDelim: .
figureTemplate: __$$figureTitle$$ A$$i$$$$titleDelim$$__ $$t$$
subfigureTemplate: __$$figureTitle$$ $$i$$$$titleDelim$$__ $$t$$
subfigureChildTemplate: __($$i$$)__ $$t$$
tableTemplate: __$$tableTitle$$ $$i$$$$titleDelim$$__ $$t$$
ccsTemplate: ""
figPrefix:
  - "figure"
  - "figures"
tblPrefix:
  - "table"
  - "tables"
subfigureRefIndexTemplate: $$i$$$$suf$$$$s$$

---

<div id="atotop"><a href="#title-block-header">&#x25B2;</a></div>
<div id="js_msg">Some functions of this webpage need JavaScript <a href="https://www.enable-javascript.com/">enabled.</a></div>

---

# Introduction

## Scope

This online appendix supplements the literature review _The labor market integration of immigrant women in Europe. A review_ by [Bentley Schieckoff](mailto:bentley.schieckoff@uni-konstanz.de), University of Konstanz, and [Maximilian Sprengholz](mailto:maximilian.sprengholz@hu-berlin.de), Humboldt-Universität zu Berlin (2021, mimeo). We provide descriptive statistics on:

1. Immigrant population in Europe (2019)
    - Immigrant population by gender and origin group (EU vs. non-EU) across destination countries
    - Top 5 countries of origin by gender and destination country
2. Labor market outcomes of immigrants
    - Outcomes and gaps in outcomes by nativity and gender across destination countries (2019/2014)
    - Trends in nativity and gender gaps by origin groups across destination countries (1995-2019)
    - Outcomes:
        - Labor force participation rates (2019, trend)
        - Unemployment rates (2019, trend)
        - Part-time employment rates (2019, trend)
        - Temporary employment rates (2019, trend)
        - Overqualification rates (2014 only)

We highlight just a few facets of the presented data in the manuscript, a lot more can be explored here.

## Data

<p class="warn">
We define immigrants as persons who reside in a country in which they were not born (For). In some cases, we additionally differentiate by immigrant origin group: EU-born (EU) or non-EU born (TC). Natives (Nat) are not foreign-born.
</p>

We use two different datasets. Immigrant population estimates are based on [UNDESA data](https://www.un.org/en/development/desa/population/migration/data/estimates2/estimates19.asp) and are not restricted by age. Data on labor market outcomes come from Eurostat for individuals between age 15 and 64, see data for [labor force participation](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_argacob), [unemployment](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_urgacob), [part-time employment](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_eppgacob), [temporary employment](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_etpgacob), and [overqualification](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfso_14loq).

We provide some additional notes on the respective samples and measures in the figure notes. For measurement details, please see the documentations provided on the linked webpages.

The order of presentation of destination countries corresponds to a (history based) grouping into north-western Europe (NWE), southern Europe (SE), and central and eastern Europe (CEE). We restrict destinations to countries for which data is available from both UNDESA and Eurostat:

| Destination Country Group | Countries |
| ------------- | -------------------------------------- |
| North-western Europe | Austria, Belgium, Denmark, Finland, France, Germany, Iceland, Ireland, Luxembourg, the Netherlands, Norway, Sweden, Switzerland, UK |
| Southern Europe | Greece, Malta, Italy, Portugal, Spain |
| Central and eastern Europe | Croatia, Czech Republic, Estonia, Hungary, Latvia, Lithuania, Montenegro, North Macedonia, Poland, Romania, Serbia, Slovakia, Slovenia |

---

# Immigrant population across Europe

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/imgpop_2019.html

![Immigrant population across Europe by gender and origin groups, 2019](){#fig:imgpop_2019 class="dummy"}

<p class="fignote">
The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right.<br />
Source: [UNDESA](https://www.un.org/en/development/desa/population/migration/data/estimates2/estimates19.asp)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure">

!include ../results/figures/html/imgpop_top5_2019.html

![Main countries of origin by gender and destination country, 2019](){#fig:imgpop_top5_2019 class="dummy"}

<p class="fignote">
The share is relative to the total population of immigrants conditional on gender.<br />
Source: [UNDESA](https://www.un.org/en/development/desa/population/migration/data/estimates2/estimates19.asp)
</p>
</div>


---

# Labor force participation

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_2019_lfp.html

![Nativity and gender gaps in labor force participation rates by country, 2019](){#fig:dd_2019_lfp class="dummy"}

<p class="fignote">
Age 15-64. Immigrants include all immigrants for which there is data available, irrespective of origin. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_argacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure portrait">

!include ../results/figures/html/abs_2019_lfp.html

![Labor force participation rates by country, gender and origin group, 2019](){#fig:abs_2019_lfp class="dummy"}

<p class="fignote">
Age 15-64. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_argacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_trend_lfp.html

![Trend in nativity and gender gaps in labor force participation rates by country, gender and origin group, 2019](){#fig:dd_trend_lfp class="dummy"}

<p class="fignote">
Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. Lighter shades of markers represent the Eurostat flag 'low reliability'. Values for EU- and non-EU-immigrants refer to EU28, but in many cases there are also Eurostat figures available for EU15 (including earlier years), see source.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_argacob)
</p>
</div>

---

# Unemployment

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_2019_unemp.html

![Nativity and gender gaps in unemployment rates by country, 2019](){#fig:dd_2019_unemp class="dummy"}

<p class="fignote">
The unemployment rate represents a share of the population active on the labor market. Immigrants include all immigrants for which there is data available, irrespective of origin. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_urgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure portrait">

!include ../results/figures/html/abs_2019_unemp.html

![Unemployment rates by country, gender and origin group, 2019](){#fig:abs_2019_unemp class="dummy"}

<p class="fignote">
The unemployment rate represents a share of the population active on the labor market. Age 15-64. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_urgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_trend_unemp.html

![Trend in nativity and gender gaps in unemployment rates by country, gender and origin group, 2019](){#fig:dd_trend_unemp class="dummy"}

<p class="fignote">
The unemployment rate represents a share of the population active on the labor market. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_urgacob)
</p>
</div>

---

# Part-time employment

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_2019_pt.html

![Nativity and gender gaps in part-time employment rates by country, 2019](){#fig:dd_2019_pt class="dummy"}

<p class="fignote">
Part-time employment largely based on respondents self-assessment. Immigrants include all immigrants for which there is data available, irrespective of origin. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_eppgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure portrait">

!include ../results/figures/html/abs_2019_pt.html

![Part-time employment rates by country, gender and origin group, 2019](){#fig:abs_2019_pt class="dummy"}

<p class="fignote">
Part-time employment largely based on respondents self-assessment. Age 15-64. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_eppgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_trend_pt.html

![Trend in nativity and gender gaps in part-time employment rates by country, gender and origin group, 2019](){#fig:dd_trend_pt class="dummy"}

<p class="fignote">
Part-time employment largely based on respondents self-assessment. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. Lighter shades of markers represent the Eurostat flag 'low reliability'. Values for EU- and non-EU-immigrants refer to EU28, but in many cases there are also Eurostat figures available for EU15 (including earlier years), see source.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_eppgacob)
</p>
</div>


---

# Temporary employment

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_2019_temp.html

![Nativity and gender gaps in temporary employment rates by country, 2019](){#fig:dd_2019_temp class="dummy"}

<p class="fignote">
Temporary employment indicates no permanent work contract. Immigrants include all immigrants for which there is data available, irrespective of origin. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_etpgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure portrait">

!include ../results/figures/html/abs_2019_temp.html

![Temporary employment rates by country, gender and origin group, 2019](){#fig:abs_2019_temp class="dummy"}

<p class="fignote">
Temporary employment indicates no permanent work contract. Age 15-64. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_etpgacob)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_trend_temp.html

![Trend in nativity and gender gaps in temporary employment rates by country, gender and origin group, 2019](){#fig:dd_trend_temp class="dummy"}

<p class="fignote">
Temporary employment indicates no permanent work contract. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. Lighter shades of markers represent the Eurostat flag 'low reliability'. Values for EU- and non-EU-immigrants refer to EU28, but in many cases there are also Eurostat figures available for EU15 (including earlier years), see source.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfsa_etpgacob)
</p>
</div>

---

# Overqualification

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure qhd">

!include ../results/figures/html/dd_2014_overq.html

![Nativity and gender gaps in overqualification rates by country, 2019](){#fig:dd_2014_overq class="dummy"}

<p class="fignote">
Overqualification measure based on respondent's self-assessment that qualifications and skills would allow more
demanding tasks than current job. Immigrants include all immigrants for which there is data available, irrespective of origin. Age 15-64. Markers represent the values obtained by subtracting the comparison group value from the value for immigrant women. The dashed vertical lines separate northern-western Europe (NWE) on the left, southern Europe (SE) in the center, and central and eastern Europe (CEE) on the right. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfso_14loq)
</p>
</div>

<!-- Hack for html based figures. External html is included via pandoc-filter. Dummy image triggers pandoc-crossref. -->
<div class="figure portrait">

!include ../results/figures/html/abs_2014_overq.html

![Overqualification rates by country, gender and origin group, 2019](){#fig:abs_2014_overq class="dummy"}

<p class="fignote">
Overqualification measure based on respondent's self-assessment that qualifications and skills would allow more
demanding tasks than current job. Age 15-64. Lighter shades of markers represent the Eurostat flag 'low reliability'.<br />
Source: [Eurostat](https://ec.europa.eu/eurostat/web/products-datasets/product?code=lfso_14loq)
</p>
</div>



---

# References
