import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import numpy as np

def run_sim2_app():
    st.subheader("Interactive Keynesian Equilibrium Plot")

    instructions_expander = st.expander("**Instructions**")
    with instructions_expander:
        st.markdown("""
        
        1. **Autonomous Consumption (C0):** Use the slider on the left sidebar to adjust the level of autonomous consumption (C0).

        2. **Marginal Propensity to Consume (C1):** Adjust the slider to set the value of C1. 
                    
        3. **Taxation Rate (tax_rate):** Adjust the slider to set the tax rate.

        4. **Investment (I):** Use the slider labeled "Investment" to adjust the level of investment (I).

        5. **Government Spending (G):** Adjust the slider to set the level of government spending (G).

        6. **Propensity to Import (M1):** Use the slider to adjust the propensity to import (M1).


        7. **Exports (X):** Adjust the slider to set the level of exports (X).

        8. **Interpreting the Chart:** The plot shows different levels of aggregate demand (AD) based on the selected values of C0, C1, I, G, M1, M, and X.

        9. **Interpreting Equilibrium Points:** The intersection of any line with the 45-degree line represents the Keynesian equilibrium point.

        """)

    c0_expander = st.sidebar.expander("Autonomous Consumption")
    c0 = c0_expander.slider("Autonomous Consumption", min_value=0, max_value=100, value=20, key='c0')

    c1_expander = st.sidebar.expander("Marginal Propensity to Consume")
    c1 = c1_expander.slider("Marginal Propensity to Consume", min_value=0.0, max_value=1.0, value=0.9, step=0.1, key='c1')

    tax_rate_expander = st.sidebar.expander("Taxation Rate")
    tax_rate = tax_rate_expander.slider("Taxation Rate", min_value=0.0, max_value=1.0, value=0.3, step=0.1, key='tax_rate')

    I_expander = st.sidebar.expander("Investment")
    I = I_expander.slider("Investment", min_value=10, max_value=100, value=60, key='I')

    G_expander = st.sidebar.expander("Government Spending")
    G = G_expander.slider("Government Spending", min_value=10, max_value=100, value=100, key='G')

    M1_expander = st.sidebar.expander("Propensity to Import")
    M1 = M1_expander.slider("Propensity to Import", min_value=0.0, max_value=1.0, value=0.1, step=0.1, key='M1')

    X_expander = st.sidebar.expander("Exports")
    X = X_expander.slider("Exports", min_value=0, max_value=100, value=30, key='X')

    # Calculate T and Y based on the given conditions
    def calculate_T(Y):
        return tax_rate * Y

    def calculate_Y(T):
        return T / (1 - tax_rate)

    # Calculate C, Imports, and NX based on the given conditions
    def calculate_C(Y, T):
        return c0 + c1 * (Y - T)

    def calculate_Imports(Y, T):
        return M1 * (Y - T)

    def calculate_NX(X, Imports):
        return X - Imports

    # Calculate AD based on the given conditions
    def calculate_AD(Y, T):
        C = calculate_C(Y, T)
        Imports = calculate_Imports(Y, T)
        NX = calculate_NX(X, Imports)
        return C + I + G + NX

    # Income/output range
    Y = np.linspace(0, 700, 100)

    # Create the plot
    plt.figure(figsize=(10, 10))

    # Calculate T and Y based on the given conditions
    T = calculate_T(Y)
    Y = calculate_Y(T)

    # Calculate AD based on the given conditions
    AD = calculate_AD(Y, T)
    C = calculate_C(Y, T)
    C_I = C + I
    C_I_G = C + I + G
    C_I_G_NX = C + I + G + calculate_NX(X, calculate_Imports(Y, T))

    # Plot C
    plt.plot(Y, C, label='C (After Tax)')

    # Plot C + I
    plt.plot(Y, C_I, label='C + I (After Tax)')

    # Plot C + I + G
    plt.plot(Y, C_I_G, label='C + I + G (After Tax)')

    # Plot C + I + G + NX
    plt.plot(Y, C_I_G_NX, label='C + I + G + NX (After Tax)')

    # Plot the 45-degree line
    plt.plot(Y, Y, label='45 degree line (Y = AD)', linestyle='--', color='k')

    plt.xlabel('Income / Output (Y)')
    plt.ylabel('Aggregate Demand (AD)')
    plt.title('Keynesian Equilibrium')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt.gcf())  # Display the plot in streamlit

