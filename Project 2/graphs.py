import plotly.graph_objs as go
import process
from pandas.api.types import is_numeric_dtype


def create_map(dfm, crime_checks):
    
    # convert to int for formatting consistency
    for col in crime_checks:
        dfm[col] = dfm[col].astype(int)

    # Plotly requirement
    for col in dfm.columns:
        dfm[col] = dfm[col].astype(str)

    # Create hover text
    dfm['text'] = dfm['State'] + '<br>' + '<br>' +\
        'Total Crimes: ' + dfm['total_crimes'] + '<br>' + '<br>'

    for col in crime_checks:
        dfm['text'] += col + ': ' + dfm[col] + '<br>'

    data = [dict(
        type='choropleth',
        colorscale='Viridis',
        autocolorscale=False,
        locations=dfm['State_Abbrev'],
        z=dfm['total_crimes'].astype(float),
        locationmode='USA-states',
        text=dfm['text'],
        hoverinfo='text',
        marker=dict(
            line=dict(
                color='rgb(255,255,255)',
                width=2
            )
        ),
        colorbar=dict(
            title="",
            autotick=False,
            tickprefix='',
            reverse=True
        )
    )]

    layout = dict(
        title='Crimes per State',
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
            bgcolor='rgb(250, 250, 250)'
        ),
        legend=dict(
            orientation='h'
        ),
        paper_bgcolor='rgb(250, 250, 250)'
    )

    fig = dict(data=data, layout=layout)

    return fig


def create_scatter(dfs, variable, variable_type, state_abbrev, color):
    ''''''

    dfs = dfs[['State', 'Year', 'total_crimes', variable]]
    dfs = process.drop_rows_with_zeros(dfs)

    # Round and change columns to strings
    for col in dfs.columns:
        if is_numeric_dtype(dfs[col]):
            dfs[col] = dfs[col].round(2)
        dfs[col] = dfs[col].astype(str)

    # Create hover text
    dfs['text'] = 'State: ' + dfs['State'] + '<br>' +\
        'Year: ' + dfs['Year'] + '<br>' +\
        variable + ': ' + dfs[variable] + '<br>' +\
        'Total Crimes: ' + dfs['total_crimes']

    fig = {
        'data': [go.Scatter(
            x=dfs['total_crimes'],
            y=dfs[variable],
            mode='markers',
            text=dfs['text'],
            hoverinfo='text',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
                'color': color
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Total Crimes',
                'type': 'linear' if variable_type == 'Linear' else 'log'
            },
            yaxis={
                'title': variable,
                'type': 'linear' if variable_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            
            height=400,
            hovermode='closest',
            plot_bgcolor='rgb(250, 250, 250)'
        )
    }

    return fig


def create_time_series(dfs, axis_type, yaxis_column_name, title, color,
                       year_line, agg):
    ''''''
    if agg == 'Sum':
        dfpiv = dfs.groupby('Year').sum().reset_index()
    else:
        dfpiv = dfs.groupby('Year').mean().reset_index()

    # Get the minimumm without zeros to draw the vertical line
    line_min = dfpiv[dfpiv[yaxis_column_name] > 0][yaxis_column_name].min()

    shapes = []

    if year_line:
        shapes +=\
            [
                # Vertical line
                {
                    'type': 'line',
                    'x0': year_line,
                    'y0': line_min,
                    'x1': year_line,
                    'y1': dfpiv[yaxis_column_name].max(),
                    'line': {
                        'color': 'rgb(55, 128, 191)',
                        'width': 3,
                    },
                }]

    return {
        'data': [go.Scatter(
            x=dfpiv['Year'],
            y=dfpiv[yaxis_column_name],
            mode='lines+markers',
            marker={
                'color': color
            }
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 60, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False},
            'plot_bgcolor': 'rgb(250, 250, 250)',
            'shapes': shapes
        }
    }
