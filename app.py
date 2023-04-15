import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
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

# Import Price Data - Current
token_price = requests.get("https://api.flipsidecrypto.com/api/v2/queries/d539a543-59c8-48e9-a60a-bc3b54998eea/data/latest")
prices = token_price.json()
price = json_normalize(prices)

## Import Price Data - Last 14 Days
tp = requests.get("https://api.flipsidecrypto.com/api/v2/queries/ca9e5cd1-410d-4577-a84c-4958a18c547c/data/latest")
p = tp.json()
pp = json_normalize(p)

## Import Pool Depth Information 
poold = requests.get("https://api.flipsidecrypto.com/api/v2/queries/a7caa828-df39-4216-9a4f-cbfc9048c26b/data/latest")
pool_depth = poold.json()
pool_depth = json_normalize(pool_depth)

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
                    6, 
                    ui.input_select("pool", "Pool", pool_id['POOL_NAME']), 
                ), 
                ui.column(
                    3, 
                ),
            ), 
            # Pool Fee Input Values
            ui.row(
                ui.column(
                    3, 
                ), 
                ui.column(
                    6, 
                    ui.input_numeric("pool_fee", "Percentage Swap Fee", value=0.2), 
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
            ## Last block updates
            ui.row(
                ui.column(
                    12, 
                    ui.output_text_verbatim("last_time"), 
                ), 
            ), 
            ## Last block 
            ui.row(
                ui.column(
                    12, 
                    ui.output_text_verbatim("last_block"), 
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
            ## Input Token In
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Token In"),
                ), 
                ui.column(
                    3, 
                    ui.input_text("t_in", None, value = 'ATOM'),
                ), 
                ui.column(
                    3, 
                    ui.input_numeric("t_in_amt", None, value = 1),
                ), 
                ui.column(
                    3, 
                ), 
            ), 
            ## Token Out 
            ## Input Number Of Tokens
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Token Out"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("t_out"),
                ), 
                ## Need to change this to output
                ui.column(
                    3, 
                    ui.output_text_verbatim("t_out_amt"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ## Slippage Losses
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Slippage"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("t_slip"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("usd_slip"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
            ## Fees Paid
            ui.row(
                ui.column(
                    3,
                    ui.tags.h6({"class": "col-label"}, "Fees Paid"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("fee_paid"),
                ), 
                ui.column(
                    3, 
                    ui.output_text_verbatim("usd_fee"),
                ), 
                ui.column(
                    3, 
                ), 
            ),
        ), 
        ## Right Hand Column
        ui.column(
            6,
            ## Pool Price
            ui.row(
                ui.tags.h5({"class": "pool-price"}, "Pool Price"), 
            ), 
            ui.row(
                ui.output_text_verbatim("pool_price"), 
            ), 
            ## Chart of Pool Price 
            ui.row(
                ui.output_plot("rel_pool_price")
            ),
            ## Line Break 
            ui.row(
                ui.hr()
            ),
            ## Pool Depth
            ui.row(
                ui.tags.h5({"class": "pool-price"}, "Pool Depth"), 
            ), 
            ui.row(
                ui.output_plot("rel_pool_depth")
            ),
        ), 
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    ## This Function Grabs The Current / Live Price
    @reactive.Calc
    async def get_price(): 
        if input.pool() == "": 
            return ""
        
        rel_price = 0
        ## Grab the asset symbols from the pool ID 
        asset0 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        asset1 = pool_id.loc[int(input.pool()), "SYMBOL_2"]

        ## Get the token price for each token
        price0 = sum(price.loc[price["SYMBOL"] == asset0, "PRICE"])
        price1 = sum(price.loc[price["SYMBOL"] == asset1, "PRICE"])

        if int(price0) < int(price1):
            rel_price = price1/price0
        else: 
            rel_price = price0/price1

        ## Grab the asset in & the amount, calculate the expected token amount
        if input.t_in() == asset0:
            if int(price0) < int(price1):
                out_exp_amt = input.t_in_amt()*(1 / rel_price)
            else: 
                out_exp_amt = input.t_in_amt()*rel_price
        else: 
            if int(price0) < int(price1): 
                out_exp_amt = input.t_in_amt()*rel_price
            else: 
                out_exp_amt = input.t_in_amt()*(1 / rel_price)

        ## Slippage calculations
        t_in = input.t_in()
        t_in_amt = input.t_in_amt()

        amt0 = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "TOKEN_0_AMOUNT"]
        amt1 = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "TOKEN_1_AMOUNT"]

        time = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "BLOCK_TIMESTAMP"]
        block = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "BLOCK_ID"]

        if input.t_in() == asset0: 
            t_out_amt1 = amt1.values - (amt0.values*amt1.values)/(amt0.values+input.t_in_amt())
            fee = t_out_amt1*input.pool_fee()/100
            t_out_amt = t_out_amt1 - fee
            usd_out_amt = price1*t_out_amt
            usd_fee = fee*price1
        else: 
            t_out_amt1 = amt0.values - (amt0.values*amt1.values)/(amt1.values+input.t_in_amt()) 
            fee = t_out_amt1*input.pool_fee()/100
            t_out_amt = t_out_amt1 - fee
            usd_out_amt = price0*t_out_amt
            usd_fee = fee*price0

        return price0, price1, rel_price, asset0, asset1, out_exp_amt, t_out_amt, usd_out_amt, time, block, fee, usd_fee
    
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
    
    @output
    @render.text
    async def pool_price(): 
        prices = await get_price()
        if prices[0] < prices[1]:
            return f"{round(prices[2], 3)} {prices[3]} per {prices[4]}"
        else: 
            return f"{round(prices[2], 3)} {prices[4]} per {prices[3]}"

    ## Output token 
    @output 
    @render.text 
    async def t_out(): 
        asset0 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        asset1 = pool_id.loc[int(input.pool()), "SYMBOL_2"]

        if input.t_in() == asset0: 
            return asset1
        else: 
            return asset0
    
    ## Calculate the amount of token received    
    @output
    @render.text 
    async def t_out_amt(): 
        prices = await get_price()
        return f"{round(prices[5] - prices[6][0], 3)}"
    
    ## Slippage Output 
    @output
    @render.text
    async def t_slip(): 
        prices = await get_price()
        return f"{round(prices[6][0], 3)}"
    
    @output 
    @render.text 
    async def usd_slip(): 
        prices = await get_price()
        return f"${round(prices[7][0], 3)}"
    
    ## Recency Outputs 
    @output
    @render.text
    async def last_time(): 
        prices = await get_price()
        return f"Last Pool Update: {prices[8][0]} UTC"
    
    @output
    @render.text
    async def last_block(): 
        prices = await get_price()
        return f"Last Block: {prices[9][0]}"
    
    ## Output fees paid 
    @output 
    @render.text
    async def fee_paid(): 
        prices = await get_price()
        return f"{round(prices[10][0], 5)}"
    
    @output
    @render.text
    async def usd_fee(): 
        prices = await get_price()
        return f"${round(prices[11][0], 5)}"
    
    
    ## Creates Relative Price Plot
    @output
    @render.plot()
    async def rel_pool_price(): 

        asset0 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        asset1 = pool_id.loc[int(input.pool()), "SYMBOL_2"]

       ## Mean Price 
        price0 = pp.loc[pp["SYMBOL"] == asset0, "MEAN_PRICE"]
        price1 = pp.loc[pp["SYMBOL"] == asset1, "MEAN_PRICE"]

        ## Min Price 
        min0 = pp.loc[pp["SYMBOL"] == asset0, "MIN_PRICE"]
        min1 = pp.loc[pp["SYMBOL"] == asset1, "MIN_PRICE"]
        if price0.iloc[0] < price1.iloc[1]:
            rel_min = min1.values / min0.values
        else: 
            rel_min = min0.values / min1.values

        # Max Price 
        max0 = pp.loc[pp["SYMBOL"] == asset0, "MAX_PRICE"]
        max1 = pp.loc[pp["SYMBOL"] == asset1, "MAX_PRICE"]
        if price0.iloc[0] < price1.iloc[1]:
            rel_max = max1.values / max0.values
        else: 
            rel_max = max0.values / max1.values

        date = pp.loc[pp["SYMBOL"]== asset0, "DATE"]
        x_d = date.values
        if price0.iloc[0] < price1.iloc[1]:
            rel_price = price1.values/price0.values
        else:
            rel_price = price0.values/price1.values
        err = rel_max - rel_min

        fig, ax=plt.subplots()
        ax.errorbar(x_d, rel_price, err, fmt='o')
        # Rotates and right-aligns the x labels so they don't crowd each other.
        for label in ax.get_xticklabels():
            label.set(rotation=30, horizontalalignment='right')
        for label in ax.xaxis.get_ticklabels()[::2]:
            label.set_visible(False)

        return fig
    
    ## Creates Pool Depth Plot
    @output
    @render.plot()
    async def rel_pool_depth(): 
        
        if input.pool() == "": 
            return ""
        
        asset0 = pool_id.loc[int(input.pool()), "SYMBOL_1"]
        asset1 = pool_id.loc[int(input.pool()), "SYMBOL_2"]

        amt0 = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "TOKEN_0_AMOUNT"]
        amt1 = pool_depth.loc[pool_depth["POOL_ID"] == int(input.pool())+1, "TOKEN_1_AMOUNT"]

        ## Create xy = k curve
        k = amt0*amt1
        amt0_new = []
        amt1_new = np.linspace(amt1/2, amt1+amt1/2, 200)
        for i in range(0, len(amt1_new)): 
            amt0_new.append(k/amt1_new[i])

        fig, ax=plt.subplots()
        ax.plot(amt0_new, amt1_new, '-', amt0, amt1, 'o')
        plt.xlabel(asset0)
        plt.ylabel(asset1)

        return fig

www_dir = Path(__file__).parent / "www"
app = App(app_ui, server, debug=True, static_assets=www_dir)