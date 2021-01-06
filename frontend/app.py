import base64
import io
import json

import requests
import os
import time
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Output, Input, State
import pandas as pd

# Get environment variables
url_path = os.getenv("API_HOST")
url_port = os.getenv("API_PORT")
endpoint = f"http://{url_path}:{url_port}"
# define app
app = dash.Dash()
app.layout = html.Div(children=[
    dcc.Tabs(id="my-menu", value="tab-1", children=[
        dcc.Tab(label="classify sms", value="tab-1"),
        dcc.Tab(label="classify multiple sms", value="tab-2"),
        dcc.Tab(label="stats for database", value="tab-3")

    ]),
    html.Div(id="tab-info")
])


def render_content_tab_1():
    return html.Div([
        html.Hr(),
        dcc.Input(id="input-tab-1", placeholder="SMS", style={"width": "100%", "height": "60px"}),
        html.Hr(),
        html.Button(id="button-tab-1", children="Submit", style={"width": "100%", "height": "60px"}, n_clicks=0),
        html.Hr(),
        html.H1(id="label-tab-1", children="Set the SMS and press submit",
                style={"width": "100%", "height": "55%", "align": "center"})
    ])


def render_content_tab_2():
    return html.Div([
        html.Hr(),
        html.Div([
            html.Div(
                dcc.Upload(id="upload-file",
                           children=html.Button('Upload File', style={"width": "50%", "height": "60px",
                                                                      })), style={"width": "50%", "height": "60px",
                                                                                  'display': 'inline-block'}),
            html.Div(
                html.Label(id="name_file", children="Select a file to continue",
                           style={"width": "30%", "height": "60px"}), style={"width": "30%", "height": "60px",
                                                                             'display': 'inline-block'})
        ]),
        html.Hr(),
        html.Button(id="button-tab-2", children="Submit", style={"width": "100%", "height": "60px"}),

        dash_table.DataTable(id="datatable-tab-2", columns=[{"name": i, "id": i} for i in ["text", "prediction"]])
    ])


def render_content_tab_3():
    return html.Div([

    ])


@app.callback(Output("tab-info", "children"), [Input("my-menu", "value")])
def render_content(tab):
    if tab == "tab-1":
        return render_content_tab_1()
    if tab == "tab-2":
        return render_content_tab_2()
    if tab == "tab-3":
        return render_content_tab_3()


@app.callback(Output("label-tab-1", "children"), [Input("button-tab-1", "n_clicks")], [State("input-tab-1", "value")])
def button_tab_1_pressed(n_clicks, input_text):
    if n_clicks > 0:
        return requests.post(f"{endpoint}/predict", params={"data": input_text}).text
    else:
        return ""


@app.callback(Output("name_file", "children"), [Input("upload-file", "filename")])
def get_filename(filename):
    return filename


@app.callback(Output("datatable-tab-2", "data"), [Input("button-tab-2", "n_clicks")],
              [State("upload-file", "contents")])
def button_tab_2_pressed(n_clicks, data):
    if n_clicks and n_clicks > 0:
        content_type, content_string = data.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
        predictions = requests.post(f"{endpoint}/predict_multiple", data=json.dumps(list(df["text"])))
        result = pd.DataFrame()
        result["text"] = df["text"]
        result["prediction"] = json.loads(predictions.content)
        return result.to_dict("rows")
    else:
        return pd.DataFrame().to_dict("rows")


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", debug=False)
    # time.sleep(10)a
    # print(url_path, url_port)
    # print(requests.post(f"http://{url_path}:{url_port}/predict", params={"data": "hello its me mario"}).text)