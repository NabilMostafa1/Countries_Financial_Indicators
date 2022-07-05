"""
this project covers building a dashboard using plotly and dash
the data used in this project is from the world bank data
this .py file does not contain any data cleaning or wrangling steps
you can find those steps in the data exploration notebook
"""

# first importing the used libraries.
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
pd.options.mode.chained_assignment = None

# importing the data into a pandas dataframe(this CSV file was created in the data exploration step).
df = pd.read_csv('Cleaned_Data.csv')
df.set_index('Country Name', inplace=True)

# creating lists for each continent containing some countries for easier access on the dashboard.
asia = ['Bangladesh', 'Cambodia', 'China', 'India', 'Indonesia', 'Iran, Islamic Rep.', 'Iraq', 'Japan', 'Korea, Rep.',
        'Kuwait', 'Malaysia',
        'Pakistan', 'Saudi Arabia', 'Qatar', 'Singapore', 'Thailand', 'United Arab Emirates', 'Vietnam', ]
africa = ['Algeria', 'Burundi', 'Cameroon', 'Chad', 'Congo, Dem. Rep.', 'Congo, Rep.', "Cote d'Ivoire",
          'Egypt, Arab Rep.', 'Ghana',
          'Ethiopia', 'Madagascar', 'Mali', 'Morocco', 'Niger', 'Nigeria', 'Senegal', 'Sudan', 'Rwanda', 'South Africa',
          'Tunisia',
          'Uganda', ]
n_america = ['Canada', 'Costa Rica', 'Cuba', 'Mexico', 'United States']
s_america = ['Argentina', 'Bolivia', 'Brazil', 'Ecuador', 'Paraguay', 'Peru', 'Uruguay', 'Venezuela, RB']
europe = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Denmark', 'Germany', 'Greece', 'Finland', 'France', 'Hungary',
          'Iceland', 'Italy',
          'Netherlands', 'Norway', 'Spain', 'Poland', 'Portugal', 'Russian Federation', 'Turkey', 'United Kingdom', ]
regions = ['World', 'Africa Eastern and Southern', 'Africa Western and Central', 'Arab World',
           'Central Europe and the Baltics',
           'East Asia & Pacific', 'Euro area', 'Europe & Central Asia', 'European Union', 'Latin America & Caribbean',
           'Middle East & North Africa', 'North America', 'Pacific island small states', 'Small states', 'South Asia',
           'Sub-Saharan Africa']
world = df.index.unique()

# setting the default value for selected countries to Egypt :D.
selected_countries = ["Egypt, Arab Rep."]

click = 0    # global click for the reset button value.


# first we create a dict containing simpler names for the 'Series Name' column as it's names are relatively complicated
indicator_dict = {'Consumer Prices Inflation': 'Inflation, consumer prices (annual %)',
                  'Inflation GDP Deflator': 'Inflation, GDP deflator (annual %)',
                  'Net National Income (USD)': 'Adjusted net national income (current US$)',
                  'Net National Income Growth (%)': 'Adjusted net national income (annual % growth)',
                  'Net National Income Growth Per Capita (%)': 'Adjusted net national income per capita (annual % growth)',
                  'Net National Income Growth Per Capita (USD)': 'Adjusted net national income per capita (current US$)',
                  'Income Share Held By Highest 10%': 'Income share held by highest 10%',
                  'Income Share Held By Highest 20%': 'Income share held by highest 20%',
                  'Income Taxes Per Total Taxes': 'Taxes on income, profits and capital gains (% of total taxes)',
                  'Income Taxes Per Revenue': 'Taxes on income, profits and capital gains (% of revenue)',
                  'Central Government Debt': 'Central government debt, total (% of GDP)',
                  'Unemployment': 'Unemployment, total (% of total labor force) (national estimate)',
                  'Unemployment, Males': 'Unemployment, male (% of male labor force) (national estimate)',
                  'Unemployment, Females': 'Unemployment, female (% of female labor force) (national estimate)',
                  'Poverty (Less Than $1.90 a Day)': 'Poverty headcount ratio at $1.90 a day (2011 PPP) (% of population)',
                  'Poverty (Less Than $3.20 a Day)': 'Poverty headcount ratio at $3.20 a day (2011 PPP) (% of population)',
                  'Poverty (Less Than $5.50 a Day)': 'Poverty headcount ratio at $5.50 a day (2011 PPP) (% of population)'
                  }


# main ploting function

def plot_fig(indicator, countries):
    """
    plot_fig function is used for ploting line graphs
    args:
        indicators: a string coresponding to a value in the indicators dict
        countries: list of strings of countries which will be plotted
    return:
        fig: a plotly figure withe the plotted countries
    """
    global df, indicator_dict                           # 1st we define the dataframe and the indicators dict as global variables
    indicator_value = indicator_dict[indicator]         # 2nd we select the 'Series Name' coresponding to the input value
    udf = df[df['Series Name'] == indicator_value]      # 3rd we select the dataframe where the 'Series Name' match and save to a new datafeame
    udf.drop('Series Name', axis=1, inplace=True)       # 4th we drop the 'Series Name' column as it's no longer nedded
    udf = udf.transpose()                               # 5th we transpose the dataframe for easier access during plotting
    udf.index = map(int, udf.index)                     # 6th we change the index(years) to integers for clearer plots
    udf = udf[countries]                                # 7th we select only the input countries from th dataframe
    fig = go.Figure()                                   # then we start ploting
    for country in countries:                           # looping through the countries list and creating the plot layout
        fig.add_trace(go.Scatter(x=udf.index, y=udf[country], mode='lines+markers', name=country))
    fig.update_layout(title={'text': '<b>{}</b>'.format(indicator_value.split('(')[0].title()),
                             'x': 0.5, 'xanchor': 'center', 'font_size': 20},
                      yaxis_title='<b>{}</b>'.format(indicator_value.split('(')[1][:-1].title()),
                      xaxis_title='<b>Years</b>',
                      legend={'title': {'text': '<b>Countries</b>', 'font_size': 14, 'side': "top"},
                              'font_size': 10, 'borderwidth': 2, 'bordercolor':'#6ea6f7', 'bgcolor': 'rgba(0,0,0,0)'},
                      margin={'t': 50, 'b': 40, 'r': 40, 'l': 40})
    return fig


# creating a dropdown list for each continent list
items_ndd = [dcc.Dropdown(id='asia-ddl', options=[{'label': i, 'value': i} for i in asia], multi=True,
                          placeholder='Asia', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                     'align-items': 'center'}),
             dcc.Dropdown(id='africa-ddl', options=[{'label': i, 'value': i} for i in africa], multi=True,
                          placeholder='Africa', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                       'align-items': 'center'}),
             dcc.Dropdown(id='europe-ddl', options=[{'label': i, 'value': i} for i in europe], multi=True,
                          placeholder='Europe', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                       'align-items': 'center'}),
             dcc.Dropdown(id='na-ddl', options=[{'label': i, 'value': i} for i in n_america], multi=True,
                          placeholder='North America', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                              'align-items': 'center'}),
             dcc.Dropdown(id='sa-ddl', options=[{'label': i, 'value': i} for i in s_america], multi=True,
                          placeholder='South America', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                              'align-items': 'center'}),
             dcc.Dropdown(id='rgn-ddl', options=[{'label': i, 'value': i} for i in regions], multi=True,
                          placeholder='World Regions', style={'color': '#000000', "width": "280px", 'display': 'flex',
                                                              'align-items': 'center'}),
             # dcc.Dropdown(id='wrld-ddl', options=[{'label': i, 'value': i} for i in world],
             #              multi=True, placeholder='All World', style={'color': '#000000', "width": "280px",
             #                                                          'display': 'flex', 'align-items': 'center'}),
             ]


def create_card(indicator, country_list):
    """
    a function to create cards for each selected country.
    inputs:
        indicator: a string coresponding to a value in the indicators dict
        country_list: a list if all the selected contries
    return:
        a list of dash cards to be used as the children of the main card
    """
    global df, indicator_dict                           # 1st we define the dataframe and the indicators dict as global variables
    indicator_value = indicator_dict[indicator]         # 2nd we select the 'Series Name' coresponding to the input value
    udf = df[df['Series Name'] == indicator_value]      # 3rd we select the dataframe where the 'Series Name' match and save to a new datafeame
    udf.drop('Series Name', axis=1, inplace=True)       # 4th we drop the 'Series Name' column as it's no longer nedded
    udf = udf.transpose()                               # 5th we transpose the dataframe for easier access during plotting
    udf.index = map(int, udf.index)                     # 6th we change the index(years) to integers for clearer plots

    # the list that we will append the cards to containing the header as an initial value.
    cards = [html.Div(html.H3("Selected Countries", className="card-header mb-3"))]

    for i in country_list:                              # looping through the countries list
        min_data = udf[udf[i] == udf[i].min()][i]       # getting the max, min and mean values of the indicator
        max_data = udf[udf[i] == udf[i].max()][i]
        mean_val = udf[i].mean()
        ofst = 0
        # creating the country card with 4 rows containing the country name and the collected values
        # with their respected years
        try:
            x = dbc.Col(dbc.Card([
                dbc.CardBody([dbc.Row(html.Div(html.H5(i, className="card-header")), className="mb-1"),
                             dbc.Row(html.Div(html.H6(('Max:{} ------- Year:{}'.format(max_data[max_data.index[0]],
                                                                                       max_data.index[0])),
                                                      className="card-text"), className="mb-0")),
                             dbc.Row(html.Div(html.H6(('Min:{} ------- Year:{}'.format(min_data[min_data.index[0]],
                                                                                       min_data.index[0])),
                                                      className="card-text"), className="mb-0")),
                             dbc.Row(html.Div(html.H6('Average:{}'.format(mean_val), className="card-text"),
                                              className="mb-1"))],
                             className="card text-white bg-secondary")
            ]), xs=10, sm=10, md=10, lg=4, xl=4, width={'offset': 3*ofst})

            cards.append(x)  # appending the created card to the children list.
            ofst += 1
        except IndexError:
            pass

    return cards


"""
The dashboard layout will contain 3 main rows 
1st row: the title of the dashboard.
2nd row: this will contain 2 main columns:
    1st column: this will have the controls for selecting the wanted parameters grouped in a card and will contain:
        1st row: the controls header
        2nd row: the dropdown for selecting the indicator
        3rd row: the dropdown for selecting the countries.
        4th row: a button for reseting the selected countries
    2nd column: this will be the graph area put in a card
3rd row: is for the country cards
"""

# the control card
left_card = dbc.Card([
    dbc.CardBody([
        dbc.Row(html.Div(html.H3("Controls", className="card-header")), className="mb-3"),
        dbc.Row(html.Div(html.H5("Choose Indicator Type:", className="card-text"), className="mb-3")),
        # 1st row is for the first dropdown menu for the graph type (1 of 17 graphs)
        dbc.Row([
            dbc.Select(id='graph-type', options=[{'label': k, 'value': k} for k, v in indicator_dict.items()],
                       value='Net National Income (USD)', className='btn btn-info dropdown-toggle',
                       style={'textAlign': "left"})
        ], className="mb-3"),
        dbc.Row(html.Div(html.H5("Choose Countries:", className="card-text"), className="mb-3")),
        # 2nd row is a multi select dropdown grouped into continents and items_ndd used as it's children
        dbc.Row([
            dbc.DropdownMenu(id='countries-ddl', label="Countries List", children=items_ndd,
                             color="info", className='btn-group dropdown-menu m-0',
                             style={"color": '#000000', "width": "280px", 'display': 'flex'}),
        ], style={"display": "flex", "flexWrap": "wrap", "width": "280px"}, className="mb-2"),
        # 3rd row is a button for reseting the selection
        dbc.Row([
            dbc.Button("Reset Selected Countries", id='reset', outline=True, color="dark", className="me-1 mt-2")
        ])
    ], className="card text-white bg-secondary"),
], className='mb-2')

# the graph card
right_card = dbc.Card([
    dbc.CardBody([dcc.Graph(id='kpi-graph')], className="card text-white bg-secondary")
])

country_cards = create_card('Net National Income (USD)', selected_countries)

# the country cards
btm_card = dbc.Card(
    dbc.CardBody(id='countries-cards',
                 children=dbc.Row(country_cards)),
    className="card text-white bg-secondary"
)

# initializing the app instance
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
                )
app.title = 'Country Financial Indicator Dashboard'
app._favicon = ("arrow.ico")

server = app.server

# building the app layout
app.layout = dbc.Container([
    # 1st row is for the title
    dbc.Row(dbc.Col(html.H1("Check Your Country's Finance",
                            className='text-center text-primary text-white mt-3 mb-4'), width=12)),
    # 2nd row is for controls and graph
    dbc.Row([
        # 1st column is for all the controls
        dbc.Col([left_card], xs=12, sm=12, md=12, lg=3, xl=3),
        # 2nd column is for the graph
        dbc.Col([right_card], xs=12, sm=12, md=12, lg=9, xl=9)
    ], className="mb-3"),
    # 3rd row is for country cards
    dbc.Row(dbc.Col(btm_card, width={'size': 12, 'offset': 0}))
], fluid=True)


# the callback and the callback function
@app.callback(
    Output('kpi-graph', 'figure'),
    Output('countries-cards', 'children'),
    Input('graph-type', 'value'),
    Input('africa-ddl', 'value'),
    Input('asia-ddl', 'value'),
    Input('europe-ddl', 'value'),
    Input('na-ddl', 'value'),
    Input('sa-ddl', 'value'),
    Input('rgn-ddl', 'value'),
    # Input('wrld-ddl', 'value'),
    Input('reset', 'n_clicks')
)
def update_graph(indicator, africa_s, asia_s, europe_s, na_s, sa_s, rgn_s, clicks):
    global selected_countries, click
    if clicks is None or clicks == click:
        for i in [africa_s, asia_s, europe_s, na_s, sa_s, rgn_s]:
            if i is None:
                continue
            else:
                for c in i:
                    if c not in selected_countries:
                        selected_countries.append(c)
                    else:
                        continue
    elif clicks is not None:
        if clicks > click:
            click = clicks
            selected_countries = []

    fig = plot_fig(indicator, selected_countries)
    country_card = create_card(indicator, selected_countries)
    cards = [dbc.Row(country_card)]

    return fig, cards


if __name__ == '__main__':
    app.run_server(debug=True)
