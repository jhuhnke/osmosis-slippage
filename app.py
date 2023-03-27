import matplotlib.pyplot as plt
import numpy as np
import requests
import json 
from shiny import ui, render, App, reactive, Inputs, Outputs, Session
from pandas import json_normalize
from pathlib import Path

# Get Liquidity Pool Data
pool_ids = requests.get("https://node-api.flipsidecrypto.com/api/v2/queries/355406c5-ed57-430d-8940-1bf4d11a64cc/data/latest")
pools = pool_ids.json()
pool_id = json_normalize(pools)

app_ui = ui.page_fixed(
    ui.tags.head(
        ui.tags.style(
            (Path(__file__).parent / "style.css").read_text(),
        ),
    ),
    ui.row(
        ui.tags.h2({"class": "title"}, "Osmosis Swap Simulator")
    ), 
    ui.row(
        ui.column(
            5, 
            ui.row(
                ui.tags.h5({"class": "heading"}, "Input Values"), 
            ), 
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    3, 
                    ui.input_select("pool", "Pool", pool_id['POOL_ID']), 
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("fee", "% Pool Fee", value = 0.2, step = 0.05), 
                ), 
                ui.column(
                    3, 
                ),
            ), 
        ), 
        ui.column(
            7, 
        ), 
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def symbol1(): 
        symbol1 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        return f"{symbol1}"
    
    @output
    @render.text
    def symbol2(): 
        symbol2 = pool_id.loc[int(input.pool()), "SYMBOL_2"]
        return f"{symbol2}"

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, debug=True, static_assets=www_dir)