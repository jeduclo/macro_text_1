# Core pkgs
import streamlit as st
import streamlit.components.v1 as stc

# Import Mini Apps
#from stock_app import run_stock_app
#from stock_tsx import run_tsx_app
from gdp import run_gdp_app
from sim import run_sim_app
from sim2 import run_sim2_app


HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">On National Accounts App</h1>
    </div>
    """
stc.html(HTML_BANNER)

def run_home_app():
    
    st.write("""
    Welcome to the Expenditure-Output Model and GDP Data Exploration!

    This application provides a comprehensive overview of National Output (GDP) and an interactive Expenditure-Output Model for Canada. The data is sourced from Statistics Canada and allows you to explore the most recent GDP data through charts and the possibility to download it in a format compatible with Microsoft Excel for further analysis.

    **GDP Section:**
    In the GDP section, you can explore Gross Domestic Product (GDP) data. Charts are available to visualize the trends and composition of GDP over time. You can analyze the contributions of different sectors, such as consumption, investment, government spending, and net exports to the overall GDP.

    **Simulation-1: Interactive Expenditure-Output Model with Taxation Amount:**
    In Simulation-1, you can interact with an Expenditure-Output Model that considers taxation amount as a parameter. By adjusting the sliders for autonomous consumption, marginal propensity to consume, taxation amount, investment, government spending, and net exports, you can observe the effects on the equilibrium output level in the economy. This simulation helps you understand the impact of different factors on aggregate demand and output.

    **Simulation-2: Interactive Expenditure-Output Model with Tax Rate & Propensity to Import:**
    Simulation-2 presents an Expenditure-Output Model that considers tax rate and the propensity to import. By adjusting the sliders for autonomous consumption, marginal propensity to consume, tax rate, investment, government spending, and propensity to import, you can analyze the effects on equilibrium output. This simulation allows you to explore the influence of tax policy and international trade on aggregate demand and output.

    We hope that this application provides valuable insights into the Expenditure-Output Model and helps you analyze GDP data effectively. Enjoy exploring the different sections and simulations!

    """)






def main():
    menu = ["Home","GDP","Simulation-1","Simulation-2"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        run_home_app()
    elif choice == "GDP":
        run_gdp_app()
    elif choice == "Simulation-1":
        run_sim_app()
    elif choice == "Simulation-2":
        run_sim2_app()
    else:
        run_home_app()


if __name__ == '__main__':
    main() 
