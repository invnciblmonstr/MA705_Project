import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
player = pd.read_csv('players_21.csv')
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def player_information(player_name):
    iplayer = player[player['short_name'] == player_name].reset_index(drop=True)
    full_name = iplayer.loc[0,'long_name']
    date_of_birth = iplayer.loc[0,'dob']
    nationality = iplayer.loc[0,'nationality']
    height = iplayer.loc[0,'height_cm']
    weight = iplayer.loc[0,'weight_kg']
    club = iplayer.loc[0,'club_name']
    position = iplayer.loc[0,'team_position']
    jersey = int(iplayer.loc[0,'team_jersey_number'])
    value = int(iplayer.loc[0,'value_eur'])
    ovr = int(iplayer.loc[0,'overall'])
    age = int(iplayer.loc[0,'age'])
    return html.Div(
        [
            html.H4(full_name),
            html.P("Overall Score: " + str(ovr)),
            html.P(f"Age:{age}"),
            html.P(f"Date of Birth: {date_of_birth}"),
            html.P("Nationality: " + nationality),
            html.P("Club: " + club),
            html.P("Weight: " + str(weight) + ' KG'),
            html.P("Height: " + str(height) + ' CM'),
            html.P("Positions: " + position),
            html.P("Jersey Number: " + str(jersey)),
            html.P("Value (EUR): " + str(value)),
        ]
    )

def spider_chart(player_name):
    stats = player[['short_name', 'team_position', 'pace' , 'shooting' , 'passing' , 'dribbling' , 'defending' , 'physic' ,'gk_diving' , 'gk_handling'  ,'gk_kicking' , 'gk_reflexes' , 'gk_speed' , 'gk_positioning']]
    playst = stats[stats.short_name == player_name].reset_index(drop=True)
    if playst.loc[0,'team_position'] != 'GK':
        playstt = playst.iloc[:,2:8].T
        playstt['theta'] = playstt.index
    else:
        playstt = playst.iloc[:,8:].T
        playstt['theta'] = playstt.index

    fig = px.line_polar(playstt, r=0, theta='theta', line_close=True)
    fig.update_traces(fill='toself', fillcolor = 'red', opacity = 0.4)
    fig.update_layout(
    polar = dict(radialaxis = dict(visible = False, showgrid = False, showline = False, showticklabels = False,
                                                     range = (0,100), layer = "above traces"), gridshape = 'linear'),
             )
    return fig

def counrtymap(name):
    iplayer = player[player['short_name'] == name].reset_index(drop=True)
    country = iplayer.loc[0,'nationality']
    fig = px.choropleth( locations= [country], locationmode= 'country names',
                           color_continuous_midpoint= 'red',
                          width= 500,
               height= 250)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}
                      # , paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='rgba(0,0,0,0)'
                      )
    fig.update_geos(fitbounds="locations", visible=True)
    return fig

card1 = dbc.Card(dbc.CardBody(
                    [
                        dbc.CardHeader("Select player 1 Here"),
                        dcc.Dropdown(id="dropdown1", options=[{"label": i, "value": i}for i in list(player.short_name)],clearable=True,searchable=True,value="L. Messi",style = {"color":"black"}),
                        dbc.Row(children=[html.Div(id="profile-about-section",style={"padding-left": "5%","padding-top": "10%",},)]),
                    ], style={"width": "32rem"},
                ),
         # inverse= True,
            outline= False)
card2  = dbc.Card(dbc.CardBody(
                    [
                        dbc.CardHeader("Select player 2 Here"),
                        dcc.Dropdown(id="dropdown2", options=[{"label": i, "value": i}for i in list(player.short_name)],clearable=True,searchable=True,value="Sergio Busquets",style = {"color":"black"}),
                        dbc.Row(children=[html.Div(id="profile-about-section2",style={"padding-left": "5%","padding-top": "10%",},)]),
                    ], style={"width": "32rem"},
                ),
        color= 'dark', inverse= True
            ,outline= False)

card3 = dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.CardHeader("Player 1 Stats"),
                        dcc.Graph(id='spider-chart1', style={"width": "440px"})
                    ], style={"width": "30rem"},
                ))
card6 = dbc.Card(
                dbc.CardBody(
                    children=[
                        dbc.CardHeader("Player 2 Stats"),
                        dcc.Graph(id='spider-chart2', style={"width": "440px"})
                    ], style={"width": "30rem"},
                )
            )
card4 = dbc.Card(
                dbc.CardBody(
                    children=[dbc.CardHeader("Player 1's Country"),
                        dcc.Graph(id='p1nation', style={"width": "400px"})
                    ], style={"width": "25rem"},
                )
            )

card5 = dbc.Card(
                dbc.CardBody(
                    children=[dbc.CardHeader("Player 2's Country"),
                        dcc.Graph(id='p2nation', style={"width": "400px"})
                    ],
                )
            )

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
app.layout = dbc.Container([
    html.H1('FIFA Player Comparison Dashboard', style={'textAlign' : 'center'}),
    dbc.Row([dbc.Col(card1), dbc.Col(card2)], justify= 'around'),
    dbc.Row([dbc.Col(card3), dbc.Col(card6)], justify= 'around'),
    dbc.Row([dbc.Col(card4), dbc.Col(card5)], justify= 'around'),

])




@app.callback(
    dash.dependencies.Output("profile-about-section", "children"), [dash.dependencies.Input("dropdown1", "value")]
)
def get_driver_profile_section(name):
    if name is not None:
        return player_information(name)
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output("profile-about-section2", "children"), [dash.dependencies.Input("dropdown2", "value")]
)
def get_driver_profile_section(name):
    if name is not None:
        return player_information(name)
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output("spider-chart1", "figure"),
    [dash.dependencies.Input("dropdown1", "value")],
)
def get_spider_chart(name):
    if name is not None:
        return spider_chart(name)
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output("spider-chart2", "figure"),
    [dash.dependencies.Input("dropdown2", "value")],
)
def get_spider_chart(name):
    if name is not None:
        return spider_chart(name)
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output("p1nation", "figure"),
    [dash.dependencies.Input("dropdown1", "value")],
)
def get_country_map2(name):
    if name is not None:
        return counrtymap(name)
    else:
        raise PreventUpdate

@app.callback(
    dash.dependencies.Output("p2nation", "figure"),
    [dash.dependencies.Input("dropdown2", "value")],
)
def get_country_map1(name):
    if name is not None:
        return counrtymap(name)
    else:
        raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
    
