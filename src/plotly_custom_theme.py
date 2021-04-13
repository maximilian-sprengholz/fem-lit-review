import plotly.io as pio
import plotly.graph_objects as go

# Tol colors (https://personal.sron.nl/~pault/)
colors_hcontrast_opaque = [
    'rgba(255,255,255,1)',
    'rgba(221,170,51,1)',
    'rgba(187,85,102,1)',
    'rgba(0,68,136,1)',
    'rgba(0,0,0,1)']
colors_hcontrast_transp = [
    'rgba(255,255,255,0.5)',
    'rgba(221,170,51,0.5)',
    'rgba(187,85,102,0.5)',
    'rgba(0,68,136,0.5)',
    'rgba(0,0,0,0.5)']
colors_vibrant_opaque = [
    'rgba(0,119,187,1)',
    'rgba(51,187,238,1)',
    'rgba(0,153,136,1)',
    'rgba(238,119,51,1)',
    'rgba(204,51,17,1)',
    'rgba(238,51,119,1)',
    'rgba(187,187,187,1)']
colors_vibrant_transp = [
    'rgba(0,119,187,0.5)',
    'rgba(51,187,238,0.5)',
    'rgba(0,153,136,0.5)',
    'rgba(238,119,51,0.5)',
    'rgba(204,51,17,0.5)',
    'rgba(238,51,119,0.5)',
    'rgba(187,187,187,0.5)']
colors_paired_opaque = [
    'rgba(0,119,187,1)',
    'rgba(136,204,238,1)',
    'rgba(136,34,85,1)',
    'rgba(204,102,119,1)',
    'rgba(230,118,7,1)',
    'rgba(235,171,108,1)',
    'rgba(120,120,120,1)',
    'rgba(180,180,180,1)']
colors_paired_transp = [
    'rgba(0,119,187,0.5)',
    'rgba(136,204,238,0.5)',
    'rgba(136,34,85,0.5)',
    'rgba(204,102,119,0.5)',
    'rgba(230,118,7,0.5)',
    'rgba(235,171,108,0.5)',
    'rgba(120,120,120,0.5)',
    'rgba(180,180,180,0.5)']

# plotly theming (merge ggplot2, plotly and apply own styles)
plotly_template = pio.templates["plotly"]
pio.templates['outlined'] = go.layout.Template(
    layout = dict (
        coloraxis = plotly_template.layout.coloraxis,
        colorscale = plotly_template.layout.colorscale,
        colorway = colors_vibrant_transp,
        xaxis = dict(
                linecolor = 'black',
                linewidth = 2,
                mirror = True,
                ticks='outside',
                showline = True,
                tickwidth = 2,
                ticklabelposition = 'outside top',
        ),
        yaxis = dict(
                linecolor = 'black',
                linewidth = 2,
                mirror = True,
                ticks='outside',
                showline = True,
                tickwidth = 2
        ),
        legend = dict(
            bordercolor = 'black',
            borderwidth = 2,
            xanchor = 'left',
            bgcolor = 'white',
            x = 0.015,
            yanchor = 'top',
            y = 0.985,
            orientation = 'v',
            valign = 'middle'
        ),
        title = dict(
            x = 0,
            xref = 'paper',
            xanchor = 'left',
            yanchor = 'top',
            pad = dict(t = 0, b = 10, l = 0, r = 0),
        ),
        margin = dict(t = 60, b = 40, l = 0, r = 0),
    ),
)
pio.templates.default = "ggplot2+outlined"
