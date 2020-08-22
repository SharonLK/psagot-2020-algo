import glob
import json
import math
import pathlib
import re
from typing import List, Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html

try:
    import plotly.graph_objects as go
except:
    from plotly import graph_objs as go

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.observation_post import ObservationPost
from algorithmics.enemy.radar import Radar
from algorithmics.navigator import navigate
from algorithmics.utils.coordinate import Coordinate


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = hex_color * 2
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def _generate_coordinate_scatter(coordinate: Coordinate, color: str = '#ff5500', text=None) -> go.Scatter:
    """Converts the give coordinate into a displayable plotly scatter

    :param coordinate: coordinate to display
    :param color: color of the coordinate
    :return: plotly scatter graphics object containing the circle
    """
    return go.Scatter(x=[coordinate.x], y=[coordinate.y], mode='markers',
                      hoverinfo='skip' if text is None else 'text', text=text,
                      marker=go.scatter.Marker(color=color, size=13))


def _generate_circle_scatter(center: Coordinate, radius: float, vertices_amount: int = 60,
                             color: str = '#ff5500', hover_text=None) -> go.Scatter:
    """Converts the given circle into a displayable plotly scatter

    :param center: circle's center
    :param radius: circle's radius
    :param vertices_amount: how many vertices the calculated circle will have (discretization factor)
    :return: plotly scatter graphics object containing the circle
    """
    xs = []
    ys = []
    for i in list(range(vertices_amount)) + [0]:  # Iterate again over 0 to close the circle
        angle = (360.0 / vertices_amount) * i
        delta_x = math.sin(math.radians(angle)) * radius
        delta_y = math.cos(math.radians(angle)) * radius

        xs.append(center.x + delta_x)
        ys.append(center.y + delta_y)

    return go.Scatter(x=xs, y=ys,
                      hoveron='fills',
                      hoverinfo='skip' if hover_text is None else 'text',
                      text=hover_text,
                      fill='toself',
                      fillcolor=f'rgba{(*_hex_to_rgb(color), 0.3)}',
                      line=go.scatter.Line(color=color, width=3))


def _generate_polygon_scatter(boundary: List[Coordinate], color: str = '#00ff00', hover_text=None) -> go.Scatter:
    """Converts the given polygon into a displayable plotly scatter

    :param boundary: polygon's boundary
    :param color: scatter's color
    :return: plotly scatter graphics object displaying the path
    """
    xs = [coordinate.x for coordinate in boundary] + [boundary[0].x]
    ys = [coordinate.y for coordinate in boundary] + [boundary[0].y]

    return go.Scatter(x=xs, y=ys,
                      hoverinfo='skip' if hover_text is None else 'text',
                      text=hover_text, fill='toself', mode='lines',
                      fillcolor=f'rgba{(*_hex_to_rgb(color), 0.3)}',
                      line=go.scatter.Line(color=color, width=3))


def _generate_path_scatter(path: List[Coordinate], color: str = '#47d147') -> go.Scatter:
    """Converts a path into a displayable plotly scatter

    :param path: path to be converted
    :param color: scatter's color
    :return: plotly scatter graphics object displaying the path
    """
    xs = [coordinate.x for coordinate in path]
    ys = [coordinate.y for coordinate in path]

    return go.Scatter(x=xs, y=ys, hoverinfo='skip', mode='lines+markers',
                      line=go.scatter.Line(color=color, width=3))


def _extract_scenario_number_from_path(path: str) -> int:
    """Extract the number of a scenario given its name in the file system

    For example, the file
        ../resources/scenarios/scenario_5.json

    Will be converted into the integer 5.

    :param path: path to scenario's JSON in the file system
    :return: scenario's number
    """
    return int(re.match(r'.*scenario_(\d+)\.json', path).group(1))


scenario_files = glob.glob('../resources/scenarios/scenario_*.json')

app = dash.Dash(__name__, assets_folder=pathlib.Path('..') / 'resources' / 'css')

app.layout = html.Div([
    html.H1('The Most Best Application Ever', style={'text-align': 'center', 'font-family': 'Courier New',
                                                     'font-weight': 'bold', 'font-size': '30px'}),
    dcc.RadioItems(id='scenario-radio-items',
                   options=[{'label': f'Scenario #{_extract_scenario_number_from_path(filename)}',
                             'value': filename}
                            for filename in scenario_files],
                   value=scenario_files[0],
                   labelStyle={'display': 'inline-block', 'font-family': 'Courier New', 'font-weight': 'bold',
                               'margin-bottom': '10px', 'color': '#ffffff', 'margin-right': '10px'}),
    dcc.Graph(
        id='graph',
        config={'scrollZoom': True},
        style={'height': '70vh', 'margin-bottom': '10px'}
    ),
    html.Button('Run Algorithm!', id='run-button', style={'color': 'white'}),
    html.Div([
        html.Div('Calculated path:',
                 style={'font-family': 'Courier New', 'font-weight': 'bold', 'margin-top': '5px',
                        'margin-bottom': '5px', 'color': '#ffffff'}),
        dcc.Input(id='calculated-path',
                  readOnly=True,
                  style={'font-family': 'Courier New', 'font-weight': 'bold', 'background-color': 'black',
                         'color': 'white', 'width': '100%'})
    ]),

    dcc.Store(id='store-path', data=[])
], style={'margin-top': '20px', 'margin-left': '10px', 'margin-right': '10px'})


@app.callback(dash.dependencies.Output('calculated-path', 'value'),
              [dash.dependencies.Input('store-path', 'data')])
def update_path_text(path: List[Tuple[float, float]]) -> str:
    coordinates = [f'({coordinate[0]}, {coordinate[1]})' for coordinate in path]
    return ', '.join(coordinates)


@app.callback(dash.dependencies.Output('graph', 'figure'),
              [dash.dependencies.Input('scenario-radio-items', 'value'),
               dash.dependencies.Input('store-path', 'data')])
def scenario_dropdown_value_changed(scenario_path: str, path: List[Tuple[float, float]]) -> go.Figure:
    # Convert path into a coordinate representation
    path = [Coordinate(c[0], c[1]) for c in path]

    with open(scenario_path, 'r') as f:
        raw_scenario = json.load(f)

    # Parse scenario JSON
    source = Coordinate(raw_scenario['source'][0], raw_scenario['source'][1])
    target = Coordinate(raw_scenario['target'][0], raw_scenario['target'][1])
    posts = [ObservationPost(Coordinate(raw_post['center'][0], raw_post['center'][1]), raw_post['radius'])
             for raw_post in raw_scenario['observation_posts']]
    asteroids = [AsteroidsZone([Coordinate(c[0], c[1]) for c in raw_zone['boundary']])
                 for raw_zone in raw_scenario['asteroids_zones']]
    radars = [Radar(Coordinate(raw_radar['center'][0], raw_radar['center'][1]), raw_radar['radius'])
              for raw_radar in raw_scenario['radars']]

    return go.Figure(data=[_generate_circle_scatter(post.center, post.radius, color='#ffa31a',
                                                    hover_text=f'Observation Post {i + 1}')
                           for i, post in enumerate(posts)] +
                          [_generate_polygon_scatter(zone.boundary, color='#4dc3ff',
                                                     hover_text=f'Asteroids Zone {i + 1}')
                           for i, zone in enumerate(asteroids)] +
                          [_generate_circle_scatter(radar.center, radar.radius, color='#ff0080',
                                                    hover_text=f'Radar {i + 1}')
                           for i, radar in enumerate(radars)] +
                          [_generate_path_scatter(path, color='#cccccc')] +
                          [_generate_coordinate_scatter(source, color='#bfff80',
                                                        text=f'Source ({source.x}, {source.y})'),
                           _generate_coordinate_scatter(target, color='#ff704d',
                                                        text=f'Target ({target.x}, {target.y})')],
                     layout=go.Layout(dragmode='pan',
                                      yaxis={'scaleanchor': 'x'},
                                      showlegend=False,
                                      template='plotly_dark',
                                      margin=go.layout.Margin(l=0, r=0, b=0, t=0)))


@app.callback(dash.dependencies.Output('store-path', 'data'),
              [dash.dependencies.Input('run-button', 'n_clicks')],
              [dash.dependencies.State('scenario-radio-items', 'value')])
def run_button_n_clicks_changed(n_clicks: int, scenario_path: str) -> List[Tuple[float, float]]:
    # Don't run the algorithm when the application boots up
    if n_clicks is None:
        return []

    with open(scenario_path, 'r') as f:
        raw_scenario = json.load(f)

    # TODO: remove the ugly code duplication
    # Parse scenario JSON
    source = Coordinate(raw_scenario['source'][0], raw_scenario['source'][1])
    target = Coordinate(raw_scenario['target'][0], raw_scenario['target'][1])
    posts = [ObservationPost(Coordinate(raw_post['center'][0], raw_post['center'][1]), raw_post['radius'])
             for raw_post in raw_scenario['observation_posts']]
    asteroids = [AsteroidsZone([Coordinate(c[0], c[1]) for c in raw_zone['boundary']])
                 for raw_zone in raw_scenario['asteroids_zones']]
    radars = [Radar(Coordinate(raw_radar['center'][0], raw_radar['center'][1]), raw_radar['radius'])
              for raw_radar in raw_scenario['radars']]

    # Dash doesn't support custom return types from callbacks, so we convert the path into a list of tuples
    return [(c.x, c.y) for c in navigate(source, target, posts, asteroids, radars)]


if __name__ == '__main__':
    app.run_server(port=7324, debug=False, dev_tools_silence_routes_logging=True)
