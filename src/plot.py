# -*- coding: utf-8 -*-

# imports
import sys
import re
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import eurostat as es

'''

This file automatically downloads, prepares, and plots data on:

- UNDESA:
  - Absolute number and share of immigrants living in European countries
  - Shares of 5 main origin countries among immigrant Population
    by destination country groups
- Eurostat:
  - For various labor market outcomes:
    - Gender and nativity gaps in aggeragte figures 2019 (overqualification: 2014)
    - Absolute figures 2019 (overqualification: 2014)
    - Time trend in gender and nativity gaps

All figures are disaggregated by sex and destination country, as far as possible
also by country of origin and year. At time of publication, the most recent year
is 2019 for which most of the plotting is done. If you want to change the base
year, adjust `baseyear = 2019` to your liking. Please note that the links to the
UNDESA data are hard-coded (they seem not to be API callable), so that adjusting
`baseyear` will only affect the Eurostat estimates.

'''

# set base year
baseyear = 2019

# working dir (Jupyter proof), add src to import search locations
try:
    wd = str(Path(__file__).parents[1].absolute()) + '/'
except NameError:
    wd = str(Path().absolute()) + '/'
    print('You seem to be using a Jupyter environment. Make sure this points to the repository root: ' + wd)
sys.path.append(wd + 'src')

### plotly
# custom theme including some Paul Tol color lists (https://personal.sron.nl/~pault/)
# colors_hcontrast_opaque / colors_hcontrast_transp (opacity 50%)
# colors_vibrant_opaque / colors_vibrant_transp (transp = default)
# colors_paired_opaque / colors_paired_transp (consecutive pairs similar colors)
import plotly_custom_theme as ptheme
# interactive content base settings and chunk regex
# exported html will be stripped of first set of <div> tags and leading and
# trailing whitespace for the remaining code
def phtml_chunk(figobj, figfile):
    # make bg transparent
    figobj.update_layout(paper_bgcolor = 'rgba(255,255,255,0)')
    # write figure
    figobj.write_html(
        figfile,
        default_height='100%',
        default_width='100%',
        full_html=False,
        include_plotlyjs=False # handled via pandoc to be included once
    )
    # regex file
    with open(figfile,'r') as file:
        filedata = file.read()
        filedata = re.sub('<div>\s*', '<div class="figure_wrap_plotly">', filedata)
        filedata = re.sub('\s*\s</div>', '</div>', filedata)
        filedata = re.sub('\s*<script', '<script', filedata)
        filedata = re.sub('\s*</script>', '</script>', filedata)
    with open(figfile,'w') as file:
        file.write(filedata)


################################################################################
###  UNDESA DATA  ##############################################################
################################################################################

###  FETCH & RECODE  ###########################################################
'''
Try/except approach in case the data becomes unavailable. In that case, a
local copy is loaded.
'''

#
# (1) total population share of immigrants across countries
#

try: # fetch from web
    df_tot = pd.read_excel(
        'https://www.un.org/en/development/desa/population/migration/data/estimates2/data/UN_MigrantStockTotal_' + str(baseyear) + '.xlsx',
        sheet_name='Table 3', usecols='B:L')
except: # fetch local copy (2019)
    df_tot = pd.read_excel(wd + 'data/raw/UN_MigrantStockTotal_2019.xlsx',
        sheet_name='Table 3', usecols='B:L')
    baseyear = 2019

df_tot = df_tot.iloc[0:298, [0,10]] # caution: original index maintained
df_tot['sex'] = 'TOTAL'
df_tot.columns = ['country', 'popshare_tot', 'sex']

#
# (2) total immigrant population by gender and origin groups (EU/TC)
#

for i, s in enumerate(['TOTAL','F','M'],1):

    try: # fetch from web
        df = pd.read_excel(
            'https://www.un.org/en/development/desa/population/migration/data/estimates2/data/UN_MigrantStockByOriginAndDestination_' + str(baseyear) + '.xlsx',
            sheet_name='Table '+ str(i), nrows=1992, index_col=None, header=[15]
            )
    except: # fetch local copy (2019)
        pd.read_excel(wd + 'data/raw/UN_MigrantStockByOriginAndDestination_2019.xlsx',
            sheet_name='Table 3', usecols='B:L')
        baseyear = 2019

    df.columns = np.append(['year', 'ID', 'country'], df.columns[3:])
    df = df[[col for col in df.columns if 'Unnamed:' not in col]] # omit empty and unnecessary cols

    # destination countries
    df = df.loc[df['ID'].isin(range(2019225,2019278))] # European destination countries
    df = df.drop(columns=['ID'])
    dest = ['Austria', 'Belgium', 'Croatia', 'Czechia', 'Denmark', 'Estonia',
        'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Montenegro', 'North Macedonia', 'Netherlands', 'Norway', 'Poland',
        'Portugal', 'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
        'Sweden', 'Switzerland', 'United Kingdom']
    df = df.loc[df['country'].isin(dest)]

    # origin countries grouping
    # distinction is made between EU and non-EU countries, but could also be Europe/non-Europe
    orig_eu = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden', 'United Kingdom']
    df['EU'] = df[orig_eu].sum(axis=1)
    df['Non-EU'] = df[df.columns.difference(np.append(orig_eu, ['year','country','Total','EU','Other North']))].sum(axis=1)
    df = df.drop(columns=['Other South']) # TC
    df = df.rename(columns={'Other North': 'Unknown'}) # Unknown if EU or TC

    # reshape (prepare stacking by sex)
    df['popshare_for'] = df['Total'] # placeholder for popshare_fors
    df = pd.melt(df,['year', 'country', 'popshare_for'], var_name='c_birth', value_name='pop')
    df['year'] = df['year'].astype(int)
    df['pop'] = df['pop'].astype(float)
    df['popshare_for'] = df['popshare_for'].astype(float)
    df['popshare_for'] = df['pop'].divide(df['popshare_for'], fill_value=0)

    # keep only top 5 origin countries and aggregates
    df['orig_rank'] = df.loc[df['c_birth'].isin(['Total', 'EU', 'Non-EU', 'Other']) == False].groupby(['country'])['pop'].rank(method="first", ascending=False)
    df = df[(df['orig_rank'].isin(list(range(1,6)))) | (df['c_birth'].isin(['Total', 'EU', 'Non-EU', 'Other']))]
    df = df.sort_values(by=['country','orig_rank'], axis=0)

    # add sex variable
    df['sex'] = s

    # append
    if i==1:
        df_undesa = df
    else:
        df_undesa = pd.concat([df_undesa, df])

# merge with total pop share data
df_undesa = df_undesa.merge(df_tot, on=['country','sex'], how='left')


###  PLOT  #####################################################################

# adjust labels
df_undesa.loc[df_undesa['country'].str.contains('Macedonia'), 'country'] = 'N. Macedonia'
df_undesa.loc[df_undesa['country'].str.contains('United Kingdom'), 'country'] = 'UK'

# gen country groups and make categorical for sorting and faceting
countries_nwe = ['Austria', 'Belgium', 'Denmark', 'Finland', 'France',
    'Germany', 'Iceland', 'Ireland', 'Luxembourg', 'Netherlands', 'Norway',
    'Sweden', 'Switzerland', 'UK']
countries_se = ['Greece', 'Malta', 'Italy', 'Portugal', 'Spain']
countries_cee = ['Croatia', 'Czechia', 'Estonia', 'Hungary', 'Latvia',
    'Lithuania', 'Montenegro', 'N. Macedonia', 'Poland', 'Romania',
    'Serbia', 'Slovakia', 'Slovenia']
c = pd.Categorical(df_undesa['country'],
    categories=countries_nwe + countries_se + countries_cee, ordered=True)
df_undesa['country'] = c.astype('category')
df_undesa['country_group'] = df_undesa['country'].apply(
    lambda x: 'North-Western Europe' if x in countries_nwe
    else ('Southern Europe' if x in countries_se else 'Central and Eastern Europe'))
c = pd.Categorical(df_undesa['country_group'],
    categories=['North-Western Europe', 'Southern Europe', 'Central and Eastern Europe'],
    ordered=True)
df_undesa['country_group'] = c.astype('category')


#
# (1) Stacked bar chart with immigrant population by country, origin group, gender
# and immigrant share of total population (y axis 2)

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

df_plot = df_undesa[
    (df_undesa['c_birth'].isin(['EU','Non-EU', 'Unknown'])) & (df_undesa['sex']!='TOTAL')
]

# add every trace manually and then stack
namelist = ['Women', 'Men']
k = 0
colorlist = ['rgba(0,119,187,0.5)', 'rgba(136,204,238,0.5)', 'rgba(136,34,85,0.5)',
    'rgba(204,102,119,0.5)', 'rgba(120,120,120,0.5)', 'rgba(180,180,180,0.5)']
for i, cb in enumerate(df_plot['c_birth'].unique()):
    for j, s in enumerate(df_plot['sex'].unique()):

        df_subplot = df_plot[
            (df_plot['c_birth']==cb) & (df_plot['sex']==s)
        ]

        fig.add_trace(
            go.Bar(
                name = cb + ' origin, ' + namelist[j],
                x = df_subplot['country'],
                y = df_subplot['pop'],
                hovertemplate = '<b>%{x}</b><br>Origin: ' + cb + '<br>Gender: ' + namelist[j] + '<br>Population: %{y:.3s}<extra></extra>',
                marker_color = colorlist[k],
                marker_line_width=0
            ),
            secondary_y=False,
        )

        k += 1

# sort by destination country group, descending within
sortlist = df_undesa[df_undesa['c_birth']=='Total'].sort_values(by=['country_group','pop'], ascending=[True, False], axis=0)
sortlist = sortlist['country'].unique()

# update layout
fig.update_layout(
    #title = '<b>Nativity and gender gaps in ' + vlbl + ' rates,' + plotyear + '</b>',
    legend_title_text = '<b> Origin and gender </b>',
    xaxis_title = 'Country',
    yaxis_title = 'Immigrant population (in millions)',
    barmode='stack',
    bargap=0.4,
    xaxis= dict(tickangle = -45,
        categoryorder = 'array',
        categoryarray = sortlist,
    ),
    xaxis_type='category',
    legend = dict(traceorder='reversed', x = 0.92, xanchor = 'right', y = 0.95),
    margin = dict(t = 30, b = 80, l = 0, r = 0)
)
fig.for_each_trace(
    lambda t: t.update(marker_color=t.marker.color.replace('0.5','0.8'))
)

# add separators between origin groups
fig.add_vline(x = 13.5, line_color='rgba(0, 0, 0, 1)', line_dash='dash', line_width=1)
fig.add_vline(x = 18.5, line_color='rgba(0, 0, 0, 1)', line_dash='dash', line_width=1)

# Add scatter with immigrant total pop share
df_plot = df_undesa[
    (df_undesa['c_birth']=='Total') & (df_undesa['sex']=='TOTAL')
]
fig.add_trace(
    go.Scatter(
        x = df_plot['country'],
        y = df_plot['popshare_tot'],
        mode = 'markers',
        marker_symbol = 'diamond',
        marker_color = 'rgba(255, 255, 255, 1)',
        marker_line_color = 'rgba(37, 37, 37, 1)',
        marker_line_width = 1,
        showlegend = True,
        name = 'Share of total population',
        hovertemplate = '<b>%{x}</b><br>Share (%): %{y:.1f}<extra></extra>',
    ),
    secondary_y=True,
)
fig.update_yaxes(title_text="Immigrant share of total population (%)", range=[0, 50], tick0=0, dtick=10, secondary_y=True)
fig.update_yaxes(range=[0,15000000], dtick=3000000, secondary_y=False)

# write html without hard-coding dimensions
phtml_chunk(fig, wd + 'results/figures/html/' + 'imgpop_' + str(baseyear) + '.html')
# write svg
fig.update_layout(
    width = 1000,
    height = 600
)
fig.write_image(wd + 'results/figures/' + 'imgpop_' + str(baseyear) + '.svg')
fig.write_image(wd + 'results/figures/' + 'imgpop_' + str(baseyear) + '.pdf')


#
# (2) Shares of top 5 origins relative to immigrant population in 2019 by gender
#
'''
Interactive: User can select country.
'''

df_plot = df_undesa[
    (df_undesa['sex']!='TOTAL') & (df_undesa['orig_rank'].notnull())
]

# start with empty facet plot
fig = make_subplots(
    rows=1, cols=2, subplot_titles=("Women", "Men"), shared_yaxes=False,
    horizontal_spacing=0.05
)

# info, selector
glist = ['Women', 'Men']
btn1 = []

# add country traces: base trace is Austria, fetch all if data available
clist = df_plot['country'].unique()
for c in clist:

    xdata = []
    ydata = []
    customdata = []

    if pd.isnull(df_plot['popshare_for']).all():
        print(c + ' has no values to plot. Excluded from figure.')
    else:
        # create figure by reliability subgroup to avoid additional legend grouping
        for j, s in enumerate(df_plot['sex'].unique()):
            df_subplot = df_plot.loc[
                (df_plot['sex']==s)
                & (df_plot['country']==c),
                ['country', 'sex','c_birth','popshare_for']
                ].sort_values('popshare_for', ascending=False)

            if c=='Austria':
                # add traces manually for first country
                trace = go.Bar(
                    x = df_subplot['popshare_for'],
                    y = df_subplot['c_birth'],
                    marker_color = ptheme.colors_paired_transp[j*2],
                    marker_line_width=0,
                    visible = True,
                    showlegend = False,
                    orientation='h',
                    text=df_subplot['c_birth'],
                    textposition='auto',
                    customdata = df_subplot['country'],
                    hovertemplate = '<b>%{customdata}</b><br>Gender: ' + glist[j] + '<br>Origin: %{y}<br>Share among immigrants: %{x:.1%}<extra></extra>',
                )
                fig.add_trace(trace, row=1, col=j+1)
            # store associated data for buttons
            xdata.append(df_subplot['popshare_for'])
            ydata.append(df_subplot['c_birth'])
            customdata.append(df_subplot['country'])
        # add to button dict
        # update only traces associated with each button
        btn1.append(dict(
                method = "restyle",
                args = [{'x': xdata, 'y': ydata, 'visible': True, 'showlegend': False, 'text': ydata, 'customdata': customdata}],
                label = c)
        )
# style
fig.update_layout(
    yaxis_title = '5 largest origin groups',
    bargap=0.4,
    margin = dict(t = 30, b = 70, l = 0, r = 0),
)
fig.for_each_trace(
    # make outlines opaque
    lambda t: t.update(marker_color=t.marker.color.replace('0.5','0.8'))
)
fig.for_each_annotation(
    # keep only labels as facet titles
    lambda a: a.update(text=a.text.split("=")[-1])
)

# Single label for y and x
fig.update_xaxes(showticklabels=True, dtick=0.1, tickformat='.0%', title='')
fig.update_yaxes(showticklabels=False, ticks='')

# add centered x axis label
fig.add_annotation(text='Share among immigrant population', font=dict(size=14),
    xanchor='center', xref='paper', x=0.5, yanchor='top', yref='paper', y=-0.1, showarrow=False)

# add button for country selection
fig.update_layout(
    updatemenus=[
        dict(active=0,
            buttons=btn1,
            xanchor = 'left',
            x = 1.025,
            yanchor = 'top',
            y = 1,
            bgcolor = '#fff',
            bordercolor = '#000',
            borderwidth = 2,
            pad = dict(r=4))
  ]
)

# write html without hard-coding dimensions
phtml_chunk(fig, wd + 'results/figures/html/' + 'imgpop_top5_' + str(baseyear) + '.html')


################################################################################
###  EUROSTAT DATA  ############################################################
################################################################################

###  FETCH DATA  ###############################################################
'''
Try/except approach in case the data becomes unavailable or adopts a different
format. In that case, a local copy is loaded (processed 2019 data).
'''

try: # try recode with directly fetched data

    # request data by table name (you'll get all available years)
    lfp = es.get_data_df('lfsa_argacob', True)
    unemp = es.get_data_df('lfsa_urgacob', True)
    pt = es.get_data_df('lfsa_eppgacob', True)
    temp = es.get_data_df('lfsa_etpgacob', True)
    overq = es.get_data_df('lfso_14loq', True)


    ###  RECODE  ###############################################################

    '''
    4 datasets (except overq) are all of the same structure and
    can be looped over. overq is altered to have the same structure.
    '''

    vars = {
        'labor force participation': (lfp, 'lfp'),
        'unemployment': (unemp, 'unemp'),
        'part time employment': (pt, 'pt'),
        'temporary employment': (temp, 'temp'),
        'overqualification': (overq, 'overq')
        }
    dfs = {}

    for idx, var in enumerate(vars.items()):

        vname = var[1][1]
        df = var[1][0]

        if (vname != 'overq'):

            # create dict entry with selection
            dfs[vname] = df[
                (df['age']=='Y15-64') &
                (df['c_birth'].isin(3)) &
                (df['geo\\time'].isin(['EA19', 'EU15', 'EU27_2020']) == False) &
                (df['sex'].isin(['F', 'M']))
            ]
            # drop, rename
            dfs[vname] = dfs[vname].drop(columns=['unit','age'])
            dfs[vname] = dfs[vname].rename(columns={'geo\\time': 'country'})

        else:
            # achieves the same structure for the overq dataset
            # create dict entry with selection
            dfs[vname] = df[
                (df['age']=='Y15-64') &
                (df['mgstatus'].isin(['NBO', 'FBO'])) &
                (df['isced11'].isin(['TOTAL'])) &
                (df['sex'].isin(['F', 'M']))
            ]
            # drop, reshape
            dfs[vname] = dfs[vname].drop(columns=['unit','isced11', 'age', 'time\\geo'])
            cols1 = [col for col in dfs[vname].columns if 'value' in col]
            cols2 = [col for col in dfs[vname].columns if 'flag' in col]
            part1 = pd.melt(dfs[vname], ['mgstatus', 'sex'], cols1, var_name='country')
            part2 = pd.melt(dfs[vname], ['mgstatus', 'sex'], cols2, var_name='country', value_name='flag')
            dfs[vname]= part1.join(part2['flag'])
            # rename, filter
            dfs[vname] = dfs[vname].rename(columns={'mgstatus': 'c_birth'})
            dfs[vname]['c_birth'] = dfs[vname]['c_birth'].apply(lambda x: 'NAT' if 'NBO' in x else 'FOR')
            dfs[vname]['country'] = dfs[vname]['country'].apply(lambda x: x[:2])

        # order
        col_order = ['country', 'c_birth', 'sex']
        cols_ordered = col_order + (dfs[vname].columns.drop(col_order).tolist())
        dfs[vname] = dfs[vname][cols_ordered]

        # row index
        dfs[vname] = dfs[vname].sort_values(by=['country','c_birth','sex'], axis=0)
        c = dfs[vname].country
        cb = dfs[vname].c_birth
        s = dfs[vname].sex
        dfs[vname].index = [c,cb,s]
        dfs[vname] = dfs[vname].drop(columns=['sex','c_birth','country'])

        # column index
        cols = list(dfs[vname].columns)
        colnames1 = []
        colnames2 = []
        colnames3 = []
        colnames4 = []
        for c in cols:
            colnames1 = np.append(colnames1, [vname]) # indicator
            colnames2 = np.append(colnames2, [c[:4] if vname!='overq' else '2014']) # extract year
            colnames3 = np.append(colnames3, ['avg']) # measurement (add gaps later)
            colnames4 = np.append(colnames4, [c[5:] if vname!='overq' else c]) # extract info
        dfs[vname].columns = [colnames1, colnames2, colnames3, colnames4]
        dfs[vname].columns.names = ['var', 'year', 'measure', 'info']

        # stack/unstack
        dfs[vname] = dfs[vname].unstack('c_birth')
        dfs[vname] = dfs[vname].unstack('sex')
        dfs[vname] = dfs[vname].stack('year')

        # calculate gaps and add as constant per gender, add flags
        if (vname != 'overq'):
            cblist = ['FOR', 'EU28_FOR', 'NEU28_FOR']
        else:
            cblist = ['FOR']
        for cb in cblist:
            for g in ['F', 'M']:
                # immigrant women vs. native men
                dfs[vname][vname, 'iwnw', 'value', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'value', cb, 'F')]
                    - dfs[vname].loc[:, (vname, 'avg', 'value', 'NAT', 'F')]
                    )
                dfs[vname][vname, 'iwnw', 'flag', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'flag', cb, 'F')]
                    + dfs[vname].loc[:, (vname, 'avg', 'flag', 'NAT', 'F')]
                    )
                # immigrant women vs. immigrant men
                dfs[vname][vname, 'iwim', 'value', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'value', cb, 'F')]
                    - dfs[vname].loc[:, (vname, 'avg', 'value', cb, 'M')]
                    )
                dfs[vname][vname, 'iwim', 'flag', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'flag', cb, 'F')]
                    + dfs[vname].loc[:, (vname, 'avg', 'flag', cb, 'M')]
                    )
                # immigrant women vs. native men
                dfs[vname][vname, 'iwnm', 'value', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'value', cb, 'F')]
                    - dfs[vname].loc[:, (vname, 'avg', 'value', 'NAT', 'M')]
                    )
                dfs[vname][vname, 'iwnm', 'flag', cb, g] = (
                    dfs[vname].loc[:, (vname, 'avg', 'flag', cb, 'F')]
                    + dfs[vname].loc[:, (vname, 'avg', 'flag', 'NAT', 'M')]
                    )

        # stack/unstack
        dfs[vname] = dfs[vname].stack('c_birth')
        dfs[vname] = dfs[vname].stack('sex')

        # merge datasets to ensure the same dimensions for each var (although this
        # should be true anyhow). Order of dict irrelevant here.
        if (idx == 0):
            df_eurostat = dfs[vname]
        else:
            df_eurostat = df_eurostat.join(dfs[vname], how='outer')

    # save dataset
    df_eurostat.to_pickle(wd + 'data/processed/eurostat.pkl')

except: # if recode fails with the fetched data, use processed 2019 data

    df_eurostat = pd.read_pickle(wd + 'data/processed/eurostat.pkl')
    baseyear = 2019

###  PLOT  #####################################################################

# get labels
country_label = es.get_dic('geo')

vars = {
    'labor force participation': 'lfp',
    'unemployment': 'unemp',
    'part time employment': 'pt',
    'temporary employment': 'temp',
    'overqualification': 'overq'
    }

# plot in loop
for idx, var in enumerate(vars.items()):

    vname = var[1]
    vlbl = var[0]

    # reshape, reset index, and clean flags for plot (keep only: u = unreliable)
    df = df_eurostat[vname].stack('measure').reset_index()
    df = df.rename(columns={'flag': 'reliability'})
    df['reliability'] = df['reliability'].apply(lambda x: 'Low' if 'u' in x else 'Ok')
    c = pd.Categorical(df['reliability'], categories=['Ok', 'Low'], ordered=True)
    df['reliability'] = c.astype('category')

    # label countries
    df['country_label'] = df['country'].apply(lambda x: country_label[x])
    df.loc[df['country_label'].str.contains('Germany'), 'country_label'] = 'Germany'
    df.loc[df['country_label'].str.contains('European Union'), 'country_label'] = 'EU28'
    df.loc[df['country_label'].str.contains('Macedonia'), 'country_label'] = 'N. Macedonia'
    df.loc[df['country_label'].str.contains('United Kingdom'), 'country_label'] = 'UK'

    # gen country groups and make categorical for sorting and faceting
    countries_nwe = ['Austria', 'Belgium', 'Denmark', 'Finland', 'France',
        'Germany', 'Iceland', 'Ireland', 'Luxembourg', 'Netherlands', 'Norway',
        'Sweden', 'Switzerland', 'UK']
    countries_se = ['Greece', 'Malta', 'Italy', 'Portugal', 'Spain']
    countries_cee = ['Croatia', 'Czechia', 'Estonia', 'Hungary', 'Latvia',
        'Lithuania', 'Montenegro', 'N. Macedonia', 'Poland', 'Romania',
        'Serbia', 'Slovakia', 'Slovenia']
    c = pd.Categorical(df['country_label'],
        categories=countries_nwe + countries_se + countries_cee, ordered=True)
    df['country_label'] = c.astype('category')
    df = df.dropna(subset=['country_label']) # restrict to defined regions
    df['country_group'] = df['country_label'].apply(
        lambda x: 'North-Western Europe' if x in countries_nwe
        else ('Southern Europe' if x in countries_se else 'Central and Eastern Europe'))
    c = pd.Categorical(df['country_group'],
        categories=['North-Western Europe', 'Southern Europe', 'Central and Eastern Europe'],
        ordered=True)
    df['country_group'] = c.astype('category')

    # make origin categorical to allow ordering and label
    c = pd.Categorical(df['c_birth'],
        categories=['NAT', 'FOR', 'EU28_FOR', 'NEU28_FOR'], ordered=True)
    c = c.rename_categories({'NAT': 'Nat', 'FOR': 'For', 'EU28_FOR': 'EU', 'NEU28_FOR': 'TC'})
    df['c_birth'] = c.astype('category')

    # make measure categorical to allow ordering in plot
    c = pd.Categorical(df['measure'], categories=['iwnw', 'iwim', 'iwnm'], ordered=True)
    df['measure_cat'] = c.astype('category')

    # sort
    df = df.sort_values(by=['country_label', 'year', 'c_birth'], axis=0)
    # set year to integer dtype
    c = df['year']
    df['year'] = c.astype('int32')

    #
    # (1) plot gaps for 2019 (2014) in one plot per outcome
    #

    plotyear = 2014 if (vname == 'overq') else baseyear

    fig = go.Figure()

    df_plot = df[
        (df['measure']!='avg') & (df['year']==plotyear) & (df['sex']=='F')
        & (df['c_birth']=='For')
    ]

    # add every trace manually
    # create figure by reliability subgroup to avoid additional legend grouping
    markerlist = ['diamond', 'x', 'circle']
    labelDict = {'iwnw': 'Native women', 'iwim': 'Immigrant men', 'iwnm': 'Native men'}
    legendShowDict = {'Ok': True, 'Low': False}
    for i, rel in enumerate(df_plot['reliability'].unique()):
        for j, mcat in enumerate(df_plot['measure_cat'].unique()):
            # to reserve the space all unused values to missing instead of subsetting
            df_subplot = df_plot.copy()
            df_subplot['value'].where(
                (df_subplot['reliability']==rel) & (df_subplot['measure_cat']==mcat),
                np.NaN, inplace=True
            )
            fig.add_trace(
                go.Scatter(
                    x = df_subplot['country_label'],
                    y = df_subplot['value'],
                    mode = 'markers',
                    marker_symbol = markerlist[j],
                    marker_color = ptheme.colors_paired_transp[i+j*2],
                    legendgroup = mcat,
                    showlegend = legendShowDict[rel],
                    name = labelDict[mcat],
                    hovertemplate = '<b>%{x}</b><br>Gap (pp.): %{y}<br>Immigrant women<br>vs. ' + labelDict[mcat] + '<extra></extra>',
                )
            )
    fig.add_hline(y=0, line_color='rgba(0, 0, 0, 1)', line_width=1)
    fig.add_vline(
        x = 13.5 if vname!= 'overq' else 9.5,
        line_color='rgba(0, 0, 0, 1)', line_dash='dash', line_width=1)
    fig.add_vline(
        x = 18.5 if vname!= 'overq' else 14.5,
        line_color='rgba(0, 0, 0, 1)', line_dash='dash', line_width=1)
    fig.update_layout(
        #title = '<b>Nativity and gender gaps in ' + vlbl + ' rates,' + plotyear + '</b>',
        legend_title_text = '<b> Immigrant women vs. </b>',
        xaxis_title = 'Country',
        yaxis_title = 'Gap in ' + vlbl + ' rates (pp)',
        xaxis = dict(tickangle = -45),
        legend = dict(traceorder='reversed',
            x = 0.015 if vname != 'pt' else 0.985,
            xanchor = 'left' if vname != 'pt' else 'right',
            y = 0.97),
        margin = dict(t = 30, b = 80, l = 0, r = 0)
    )
    fig.for_each_trace(
        lambda t: t.update(marker_line_color=t.marker.color.replace('0.5','1'), marker_line_width=1.5, marker_size=9)
    )
    # write html without hard-coding dimensions
    phtml_chunk(fig, wd + 'results/figures/html/' + 'dd_' + str(plotyear) + '_' + vname + '.html')
    # write svg
    fig.update_layout(
        width = 1000,
        height = 600
    )
    fig.write_image(wd + 'results/figures/' + 'dd_' + str(plotyear) + '_' + vname + '.svg')
    fig.write_image(wd + 'results/figures/' + 'dd_' + str(plotyear) + '_' + vname + '.pdf')

    #
    # (2) plot absolute values for 2019 (2014) by origin, one plot per country
    #

    plotyear = 2014 if (vname == 'overq') else baseyear
    plotfacetcols = 4 if (vname == 'overq') else 3

    # subset to absolute values
    df_plot = df[
        (df['measure']=='avg') & (df['year']==plotyear)
    ]
    # start with facet plot
    fig = px.scatter(df_plot, x='c_birth', y='value', color='reliability', symbol='sex',
                facet_col='country_label', facet_col_wrap=plotfacetcols,
                facet_row_spacing=0.035, # default is 0.07 when facet_col_wrap is used
                facet_col_spacing=0.08, # default is 0.03
                hover_data=['reliability', 'sex']
    )
    fig.update_traces(
        hovertemplate = 'Region of birth: %{x}<br>Gender: %{customdata[1]}<br>Value: %{y}<br>Reliability:  %{customdata[0]}<extra></extra>'
    )
    fig.update_layout(
        # title = '<b>' + vlbl.capitalize() + ' rates by gender and origin group,' + plotyear + '</b>',
        margin = dict(t = 30, b = 40, l = 75, r = 5),
        legend_title_text = '<b> Gender: </b>',
        legend = dict(
            xanchor = 'right',
            x = 1,
            yanchor = 'bottom',
            y = 0,
            orientation = 'v',
            valign = 'bottom',
        ),
    )
    fig.for_each_trace(
        # make outlines opaque
        lambda t: t.update(
            marker_color = ptheme.colors_paired_transp[1] if 'Low' in t.legendgroup else t.marker.color,
            marker_line_color=t.marker.color.replace('0.5','1'),
            marker_line_width=1.5,
            marker_size=6,
            showlegend = False if 'Low' in t.legendgroup else t.showlegend,
            name = 'Women' if 'F' in t.legendgroup else 'Men',
            legendgroup = 'F' if 'F' in t.legendgroup else 'M'
            )
    )
    fig.for_each_annotation(
        # keep only labels as facet titles
        lambda a: a.update(text=a.text.split("=")[-1])
    )
    # Single label for y and x
    fig.update_xaxes(showticklabels=True, title='')
    fig.add_annotation(
        text = 'Region of birth', align = 'center',
        xref = 'paper', yref = 'paper', xanchor = 'center', yanchor='bottom',
        x = 0.5, y=-0.04, showarrow=False, font=dict(size=14)
    )
    fig.update_yaxes(showticklabels=True, title='', dtick=20, tick0=0)
    fig.add_annotation(
        text = vlbl.capitalize() + ' rate (in percent)', align = 'center',
        xref = 'paper', yref = 'paper', xanchor = 'right', yanchor='middle',
        x = -0.055, y=0.5, showarrow=False, textangle=-90, font=dict(size=14)
    )
    # write html without hard-coding dimensions
    phtml_chunk(fig, wd + 'results/figures/html/' + 'abs_' + str(plotyear) + '_' + vname + '.html')
    # write svg
    fig.update_layout(
        width = 1000,
        height = 1000
    )
    fig.write_image(wd + 'results/figures/' + 'abs_' + str(plotyear) + '_' + vname + '.svg')
    fig.write_image(wd + 'results/figures/' + 'abs_' + str(plotyear) + '_' + vname + '.pdf')

    #
    # (3) plot trends in gaps by origin over time, one plot per country
    #
    '''
    To be fun to use, the user should be able to choose two of the countries
    to compare them.
    '''
    if (vname != 'overq'):
        df_plot = df[
            (df['measure']!='avg') & (df['sex']=='F') & (df['c_birth']!='Nat') & (df['year'].isin(range(1995, baseyear+1)))
        ]

        # start with empty facet plot
        dummy_df = pd.DataFrame({
            'Year': [2000,2000,2000], 'y': [0,0,0],
            'c_birth': ['Foreign born', 'EU born', 'Non-EU born (TC)']
        })
        # caution: order is somehow reversed via the express function (decrement in loop!)
        fig = px.scatter(dummy_df, x='Year', y='y', facet_row='c_birth', facet_row_spacing=0.1)
        fig.data = [] # only layout needed
        # fig.update_traces(showlegend=False, visible=False)

        # styling/functionality items
        markerlist = ['diamond', 'x', 'circle']
        linelist = ['dash', 'dot', 'solid']
        labelDict = {'iwnw': 'Native women', 'iwim': 'Immigrant men', 'iwnm': 'Native men'}
        legendvis = [True, False, False, False, False, False] * 3
        btn1 = []
        btn2 = []

        # add country traces: base trace is Austria, fetch all if data available
        clist = df_plot['country_label'].unique()
        for c in clist:

            xdata = []
            ydata = []
            hoverdata = []

            if pd.isnull(df_plot['value']).all():
                print(c + ' has no values to plot. Excluded from figure.')
            else:
                # create figure by reliability subgroup to avoid additional legend grouping
                for j, mcat in enumerate(df_plot['measure_cat'].unique()):
                    for i, rel in enumerate(df_plot['reliability'].unique()):
                        for k, bcat in enumerate(df_plot['c_birth'].unique()):
                            df_subplot = df_plot.loc[
                                (df_plot['reliability']==rel)
                                & (df_plot['measure_cat']==mcat)
                                & (df_plot['c_birth']==bcat)
                                & (df_plot['country_label']==c),
                                ['country_label', 'year','value','c_birth']]
                            if c=='Austria':
                                # add traces manually for first country
                                trace = go.Scatter(
                                    x = df_subplot['year'],
                                    y = df_subplot['value'],
                                    mode = 'lines+markers',
                                    marker_symbol = markerlist[j],
                                    marker_color = ptheme.colors_paired_transp[i],
                                    line_color = ptheme.colors_paired_transp[i],
                                    line_width = 2,
                                    line_dash = linelist[j],
                                    connectgaps = True,
                                    visible = True,
                                    legendgroup = mcat,
                                    showlegend = True if (i==0 and k==0) else False, # show only first set
                                    name = labelDict[mcat],
                                    text = df_subplot['country_label'],
                                    hovertemplate = '<b>%{text}</b><br>Year: %{x}<br>Gap (pp.): %{y}<br>Immigrant women<br>vs. ' + labelDict[mcat] + '<extra></extra>',
                                )
                                fig.add_trace(trace, row=3-k, col=1)
                                # add traces one by one (second set)
                                trace = go.Scatter(
                                    x = df_subplot['year'],
                                    y = df_subplot['value'],
                                    mode = 'lines+markers',
                                    marker_symbol = markerlist[j],
                                    marker_color = ptheme.colors_paired_transp[i+2],
                                    line_color = ptheme.colors_paired_transp[i+2],
                                    line_width = 2,
                                    line_dash = linelist[j],
                                    connectgaps=True,
                                    visible = False,
                                    legendgroup = mcat,
                                    showlegend = False,
                                    name = labelDict[mcat],
                                    text = df_subplot['country_label'],
                                    hovertemplate = '<b>%{text}</b><br>Year: %{x}<br>Gap (pp.): %{y}<br>Immigrant women<br>vs. ' + labelDict[mcat] + '<extra></extra>',
                                )
                                fig.add_trace(trace, row=3-k, col=1)
                            # store associated data for buttons
                            xdata.append(df_subplot['year'])
                            ydata.append(df_subplot['value'])
                            hoverdata.append(df_subplot['country_label'])
                # add to button dict
                # update only traces associated with each button
                btn1.append(dict(
                        method = "restyle",
                        args = [{'x': xdata, 'y': ydata, 'visible': True, 'showlegend': legendvis, 'text': hoverdata}, np.arange(0,len(xdata)*2,2)],
                        label = c)
                )
                btn2.append(dict(
                        method = "restyle",
                        args = [{'x': xdata, 'y': ydata, 'visible': True, 'showlegend': legendvis, 'text': hoverdata}, np.arange(1,len(xdata)*2,2)],
                        label = c)
                )
        # style
        fig.update_layout(
            # title = '<b>Trend in nativity and gender gaps in ' + vlbl + ' by origin group</b>',
            xaxis_title = 'Year',
            legend_title_text = '<b> Immigrant women vs. </b>',
            margin = dict(t = 30, b = 50, l = 0, r = 0),
            legend = dict(
                xanchor = 'left',
                x = 1.045,
                yanchor = 'middle',
                y = 0.5,
                orientation = 'v',
                valign = 'middle',
            ),
        )
        fig.for_each_trace(
            # make outlines opaque
            lambda t: t.update(marker_line_color=t.marker.color.replace('0.5','1'), marker_line_width=1, marker_size=6)
        )
        fig.for_each_annotation(
            # keep only labels as facet titles
            lambda a: a.update(text=a.text.split("=")[-1])
        )
        # Single label for y and x
        fig.update_xaxes(showticklabels=True, dtick=5)
        fig.layout.yaxis['title']=''
        fig.layout.yaxis2['title'] = 'Gap in ' + vlbl + ' rates (pp)'
        fig.layout.yaxis3['title']=''
        fig.update_yaxes(showticklabels=True)
        # zero line
        fig.add_hline(y=0, line_color='rgba(0, 0, 0, 1)', line_width=1)
        # add buttons for country selection
        # Button 1 always active with Austria preselected
        # Button 2 is disabled but allows selection of second country
        btn2.insert(0, dict(
                method = "restyle",
                args = [{'x': [0], 'y': [0], 'visible': False, 'showlegend': False}, np.arange(1,len(xdata)*2,2)],
                label = 'Compare to...'
            )
        )
        fig.update_layout(
            updatemenus=[
                dict(active=0,
                    buttons=btn1,
                    xanchor = 'left',
                    x = 1.045,
                    yanchor = 'top',
                    y = 1,
                    bgcolor = '#fff',
                    bordercolor = '#000',
                    borderwidth = 2),
               dict(buttons=btn2,
                    xanchor = 'left',
                    x = 1.045,
                    yanchor = 'top',
                    y = 0.9,
                    bgcolor = '#fff',
                    bordercolor = '#000',
                    borderwidth = 2)
          ]
        )
        # write html without hard-coding dimensions
        phtml_chunk(fig, wd + 'results/figures/html/' + 'dd_trend_' + vname + '.html')
