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

# Import Price Data 
token_price = requests.get("https://api.flipsidecrypto.com/api/v2/queries/d539a543-59c8-48e9-a60a-bc3b54998eea/data/latest")
prices = token_price.json()
price = json_normalize(prices)

app_ui = ui.page_fixed(
    ui.tags.head(
        ui.tags.style(
            (Path(__file__).parent / "style.css").read_text(),
        ),
    ),
    ## Title / Heading 
    ui.row(
        ui.column(
            6, 
            ui.tags.h2({"class": "title"}, "Osmosis Swap Simulator")
        ), 
        ui.column(
            3, 
        ), 
        ui.column(
            3, 
            ui.tags.h4({"class": "plug"}, "Data By Flipside")
        )
    ), 
    ## Line Break 
    ui.row(
        ui.hr()
    ),
    ## Row With Main Content
    ui.row(
        ## Pool Information Column
        ui.column(
            5, 
            ui.row(
                ui.tags.h5({"class": "heading"}, "Pool Information"), 
            ), 
            # Pool Info Input Values
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
            ## Token 1 & Token 2 Labels
            ui.row(
                ui.column(
                    3, 
                ), 
                  ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 1"),
                ), 
                ui.column(
                    3, 
                    ui.tags.h6({"class": "output_text"}, "Token 2"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ## Output the Tokens in the Pool 
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    3,
                    ui.output_text_verbatim("symbol0"),
                ),
                ui.column(
                    3, 
                    ui.output_text_verbatim("symbol1"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ## Get Current Token Price 
            ui.row(
                ui.column(
                    3, 
                    ui.tags.h6({"class": "col-label"}, "Token Price (USD)"), 
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("price0"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("price1"),
                ), 
                ui.column(
                    3, 
                ), 
            ), 
            ## Line Break 
            ui.row(
                ui.hr()
            ),
            ## Section Title
            ui.row(
                ui.tags.h5({"class": "heading"}, "Swap Parameters"), 
            ), 
            ## Input Number Of Tokens
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "# Tokens"),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("t1", None, value = 1),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("t2", None, value = 1),
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
    @reactive.Calc
    async def get_price(): 
        if input.pool() == "": 
            return ""
        
        ## Grab the asset symbols from the pool ID 
        asset0 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        asset1 = pool_id.loc[int(input.pool()), "SYMBOL_2"]

        ## Get the token price for each token
        price0 = sum(price.loc[price["SYMBOL"] == asset0, "PRICE"])
        price1 = sum(price.loc[price["SYMBOL"] == asset1, "PRICE"])

        return price0, price1
    
    @output
    @render.text
    async def symbol0(): 
        symbol1 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        return f"{symbol1}"
    
    @output
    @render.text
    async def symbol1(): 
        symbol2 = pool_id.loc[int(input.pool()), "SYMBOL_2"]
        return f"{symbol2}"
    
    @output 
    @render.text
    async def price0(): 
        prices = await get_price()
        return f"${round(prices[0], 3)}"
    
    @output 
    @render.text
    async def price1(): 
        prices = await get_price()
        return f"${round(prices[1], 3)}"

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, debug=True, static_assets=www_dir)