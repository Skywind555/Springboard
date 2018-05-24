import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import os
import pandas as pd
from textwrap import dedent as d

# The data retrieval and processing module
import process

# The graph creation module
import graphs

# The parameters for filtering
from config import variables, crime_types, base_columns


app = dash.Dash(__name__)
app.title = 'Crime Analysis Dashboard'

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

# Get and process the data
df = process.get_data()


app.layout = html.Div(children=[

    # The controls
    html.Div([

        # The checkboxes
        html.Div([
            html.H5('Crime Types'),
            dcc.Checklist(
                id='crime_checks',
                options=[{'label': i, 'value': i} for i in crime_types],
                values=crime_types,
                labelStyle={'display': 'inline-block'
                            },
            ),

        ],
            style={'width': '49%', 'display': 'inline-block'}
        ),

        # The dropdowns
        html.Div([
            dcc.Markdown(d("""
                **Select Variables**
              """)),
            dcc.Dropdown(
                id='crossfilter-variable1-column',
                options=[{'label': i, 'value': i} for i in
                         variables],
                value=variables[0]
            ),
            dcc.RadioItems(
                id='crossfilter-variable1-type',
                options=[{'label': i, 'value': i} for i
                         in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),

            dcc.RadioItems(
                id='crossfilter-variable1-agg',
                options=[{'label': i, 'value': i} for i
                         in ['Avg', 'Sum']],
                value='Avg',
                labelStyle={
                    'display': 'inline-block',
                }
            )
        ],
            style={'width': '24%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-variable2-column',
                options=[{'label': i, 'value': i}
                         for i in variables],
                value=variables[1]
            ),
            dcc.RadioItems(
                id='crossfilter-variable2-type',
                options=[{'label': i, 'value': i}
                         for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),

            dcc.RadioItems(
                id='crossfilter-variable2-agg',
                options=[{'label': i, 'value': i} for i
                         in ['Avg', 'Sum']],
                value='Avg',
                labelStyle={
                    'display': 'inline-block',
                }
            )
        ], style={'width': '24%',
                  'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'}

    ),

    # The plots
    html.Div([

        # The map
        html.Div([
            dcc.Graph(
                id='crossfilter-state-map',
                clickData={'points': [{'customdata': 'TX'}]}
            ),
        ], className='one-thirdcolumn',
            style={'width': '47%',
                   # 'height': '90vh',
                   'display': 'inline-block',
                   'padding-top': '10px',
                   'padding-right': '20px',
                   'padding-bottom': '20px',
                   'padding-left': '20px'}
        ),


        # The time series
        html.Div([
            dcc.Graph(id='x-time-series'),
            dcc.Graph(id='y-time-series'),
        ], className='threecolumns',
            style={'width': '47%',
                   # 'height': '90vh',
                   'display': 'inline-block',
                   'padding-top': '10px',
                   'padding-right': '20px',
                   'padding-bottom': '20px',
                   'padding-left': '20px'}
        ),

        # The scatter plot
        html.Div([
            dcc.Graph(
                id='scatter1',
                style={
                    'width': '47%',
                    # 'height': '90vh',
                    'display': 'inline-block',
                    'padding-top': '10px',
                    'padding-right': '20px',
                    'padding-bottom': '10px',
                    'padding-left': '10px'}
            ),
            dcc.Graph(
                id='scatter2',
                style={
                    'width': '47%',
                    # 'height': '90vh',
                    'display': 'inline-block',
                    'padding-top': '10px',
                    'padding-right': '10px',
                    'padding-bottom': '10px',
                    'padding-left': '20px'}
            )
        ], className='threecolumns',
        ),
        html.Div([

            # The States Dropdown
            html.Div([
                dcc.Markdown(d("""
                **Select States**
              """)),
                dcc.Dropdown(
                    id='state_checks',
                    options=[{'label': i, 'value': i} for i in
                             df.State_Abbrev.unique()],
                    multi=True,
                    value=df.State_Abbrev.unique()
                ),
            ], style={'width': '100%',
                      'display': 'inline-block',
                      'padding-top': '10px',
                      'padding-right': '10px',
                      'padding-bottom': '10px',
                      'padding-left': '5px'}),

            # The line Input
            html.Div([
                dcc.Markdown(d("""
                **Input Year to draw line**
              """)),
                dcc.Input(
                    id='year_line',
                    placeholder='Enter a value...',
                    type='number',
                    min=df.Year.min(),
                    max=df.Year.max(),
                    size=200,
                    style={'display': 'inline-block',
                           'width': '30%',
                           'padding-top': '10px',
                           'padding-right': '10px',
                           'padding-bottom': '30px',
                           'padding-left': '20px'},
                    value=None
                ),
            ]),
            # The agg choice
            html.Div([
                dcc.RadioItems(
                    id='crossfilter-crimetype-agg',
                    options=[{'label': i, 'value': i} for i
                             in ['Avg', 'Sum']],
                    value='Avg',
                    labelStyle={
                        'display': 'inline-block',
                    }
                )
            ]),
            html.Div([
                # The Year Slider
                dcc.Markdown(d("""
                    **Select Year Range**
                  """)),
                dcc.Slider(
                    id='crossfilter-year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=df['Year'].max(),
                    step=None,
                    marks={str(year): str(year) for year in df['Year'].unique()}
                )], style={'width': '97%',
                           'display': 'inline-block',
                           'padding-top': '10px',
                           'padding-right': '10px',
                           'padding-bottom': '30px',
                           'padding-left': '20px'}),



        ], className='threecolumns',
            style={
            'display': 'inline-block',
            'width': '95%',
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding-top': '10px',
            'padding-right': '20px',
            'padding-bottom': '10px',
            'padding-left': '20px'},

        ),
        html.Div([
            # The total Crimes timeseries
            dcc.Graph(id='time-series')],
            className='threecolumns',
            style={
            'display': 'inline-block',
            'width': '97%',
            'padding-top': '0px',
            'padding-right': '20px',
            'padding-bottom': '10px',
            'padding-left': '20px'}),

        # The table
        html.Div([
            dt.DataTable(
                # Initialize the rows
                rows=df.to_dict('records'),
                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                id='table'
            ),
            html.Div(id='selected-indexes'),
        ], style={
            'width': '95%',
            'padding-top': '10px',
            'padding-right': '20px',
            'padding-bottom': '10px',
            'padding-left': '20px'},

            className='threecolumns'

        ),

    ]),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'})

])


@app.callback(
    dash.dependencies.Output('intermediate-value', 'children'),
    [dash.dependencies.Input('crime_checks', 'values')]
)
def update_df(crime_checks):
    
    dfm = df.copy()
    dfm = df[base_columns + variables + crime_checks]
    dfm['total_crimes'] = dfm[crime_checks].sum(axis=1)

    return dfm.to_json()


@app.callback(
    dash.dependencies.Output('crossfilter-state-map', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('crime_checks', 'values')]
)
def update_map(rows, crime_checks):
    
    dfm = pd.DataFrame(rows)
    dfm = dfm.groupby(['State_Abbrev', 'State']).sum()
    dfm = dfm.reset_index()

    return graphs.create_map(dfm, crime_checks)


@app.callback(
    dash.dependencies.Output('scatter1', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('crime_checks', 'values'),
     dash.dependencies.Input('crossfilter-variable1-column', 'value'),
     dash.dependencies.Input('crossfilter-variable1-type', 'value')
     ]
)
def update_scattter1(rows,
                     crime_checks,
                     variable1_column_name,
                     variable1_type_name):

    dfs = pd.DataFrame(rows)
    dfs, state_abbrev = process.get_state(dfs)

    return graphs.create_scatter(dfs, variable1_column_name,
                                 variable1_type_name, state_abbrev,
                                 None)


@app.callback(
    dash.dependencies.Output('scatter2', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('crime_checks', 'values'),
     dash.dependencies.Input('crossfilter-variable2-column', 'value'),
     dash.dependencies.Input('crossfilter-variable2-type', 'value')
     ]
)
def update_scattter2(rows,
                     crime_checks,
                     variable2_column_name,
                     variable2_type_name):

    dfs = pd.DataFrame(rows)

    dfs, state_abbrev = process.get_state(dfs)

    return graphs.create_scatter(dfs, variable2_column_name,
                                 variable2_type_name, state_abbrev,
                                 'rgb(84,39,143)')


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('crossfilter-variable1-column', 'value'),
     dash.dependencies.Input('crossfilter-variable1-type', 'value'),
     dash.dependencies.Input('crossfilter-variable1-agg', 'value')
     ])
def update_variable1_timeseries(rows,
                                variable1_column_name,
                                variable1_type_name,
                                variable1_agg_name):

    dfs = pd.DataFrame(rows)

    dfs, state_abbrev = process.get_state(dfs)

    dfs = dfs[['Year', variable1_column_name]]
    title = '{}'.format(variable1_column_name)
    return graphs.create_time_series(dfs, variable1_type_name,
                                     variable1_column_name, title,
                                     None, None, variable1_agg_name)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('crossfilter-variable2-column', 'value'),
     dash.dependencies.Input('crossfilter-variable2-type', 'value'),
     dash.dependencies.Input('crossfilter-variable2-agg', 'value')
     ])
def update_variable2_timeseries(rows,
                                variable2_column_name,
                                variable2_type,
                                variable2_agg_name):

    dfs = pd.DataFrame(rows)

    dfs, state_abbrev = process.get_state(dfs)

    dfs = dfs[['Year', variable2_column_name]]
    title = '{}'.format(variable2_column_name)
    return graphs.create_time_series(dfs, variable2_type,
                                     variable2_column_name, title,
                                     'rgb(84,39,143)', None, variable2_agg_name)


@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [dash.dependencies.Input('intermediate-value', 'children'),
     dash.dependencies.Input('state_checks', 'value'),
     dash.dependencies.Input('crossfilter-year-slider', 'value')])
def update_rows(jsonified_update_df, state_checks, year_value):

    dfs = pd.read_json(jsonified_update_df)
    dfs = dfs[dfs['Year'] <= year_value]
    dfs = process.get_state_dropdown(dfs, state_checks)

    return dfs.to_dict('records')


@app.callback(
    dash.dependencies.Output('time-series', 'figure'),
    [dash.dependencies.Input('table', 'rows'),
     dash.dependencies.Input('year_line', 'value'),
     dash.dependencies.Input('crossfilter-crimetype-agg', 'value')
     ])
def update_crimetype_timeseries(rows,
                                year_line_value,
                                crimetype_agg_name):

    dfs = pd.DataFrame(rows)
    title = 'Total Crimes'

    return graphs.create_time_series(dfs, 'linear',
                                     'total_crimes', title,
                                     'rgb(142, 109, 37)', year_line_value,
                                     crimetype_agg_name)

app.css.append_css({
    "external_url": "https://cdn.rawgit.com/jkarakas/assets/4b97dd17/app.css"})


if __name__ == '__main__':
    app.run_server(debug=True)
