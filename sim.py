import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import numpy as np

def run_sim_app():
    st.subheader("Interactive Expenditure-Output Model with Taxation Amount")

    instructions_expander = st.expander("**Instructions**")
    with instructions_expander:
        st.markdown("""
        
        1. **Autonomous Consumption (C0):** Use the slider on the left sidebar to adjust the level of autonomous consumption (C0).

        2. **Marginal Propensity to Consume (C1):** Adjust the slider to set the value of C1. 
                    
        3. **Taxation Amount (T):** Adjust the slider to set the value of T.           

        4. **Investment (I):** Use the slider labeled "Investment" to adjust the level of investment (I).

        5. **Government Spending (G):** Adjust the slider to set the level of government spending (G).

        6. **Net Exports (NX):** Use the slider to adjust the level of net exports (NX).

        7. **Interpreting the Chart:** The plot shows different levels of aggregate demand (AD) based on the selected values of C0, C1, I, G, and NX.

        8. **Interpreting Equilibrium Points:** The intersection of any line with the 45-degree line represents the Keynesian equilibrium point.

        """)

    c0_expander = st.sidebar.expander("Autonomous Consumption")
    c0 = c0_expander.slider("Autonomous Consumption", min_value=0, max_value=100, value=50, key='c0')

    c1_expander = st.sidebar.expander("Marginal Propensity to Consume")
    c1 = c1_expander.slider("Marginal Propensity to Consume", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key='c1')

    T_expander = st.sidebar.expander("Taxation")
    T = T_expander.slider("", min_value=0, max_value=100, value=20, key='t0')

    
    I_expander = st.sidebar.expander("Investment")
    I = I_expander.slider("Investment", min_value=10, max_value=100, value=50, key='I')
    
    G_expander = st.sidebar.expander("Government spending")
    G = G_expander.slider("Government spending", min_value=10, max_value=100, value=20, key='G')
    
    NX_expander = st.sidebar.expander("Net exports")
    NX = NX_expander.slider("Net exports", min_value=10, max_value=100, value=50, key='NX')



    # Income/output range
    Y = np.linspace(0, 700, 100)

    # 45-degree line for Y = AD
    degree45_line = Y

    # Create the plot
    plt.figure(figsize=(10, 10))

    # Define aggregate demands
    AD_C = (c0 - T) + c1*Y
    AD_C_I = (c0 - T) + c1*Y + I
    AD_C_I_G = (c0 - T) + c1*Y + I + G
    AD_C_I_G_NX = (c0 - T) + c1*Y + I + G + NX


    # Plot for C only
    plt.plot(Y, AD_C, label='C (After Tax)')
    # Equilibrium point
    eq_x = np.interp(0, AD_C[::-1] - Y[::-1], Y[::-1])
    plt.annotate(f"Equilibrium (C (After Tax)",
                (eq_x, eq_x),
                textcoords="offset points", xytext=(-10,-10),
                ha='center', arrowprops=dict(facecolor='black', arrowstyle="->"))
    
    # Plot for C + I
    plt.plot(Y, AD_C_I, label='C + I (After Tax)')
    # Equilibrium point
    plt.annotate(f"Equilibrium (C + I (After Tax))",
                (np.interp(0, AD_C_I[::-1] - Y[::-1], Y[::-1]), np.interp(0, AD_C_I[::-1] - Y[::-1], Y[::-1])),
                textcoords="offset points", xytext=(-10,-10),
                ha='center', arrowprops=dict(facecolor='black', arrowstyle="->"))

    # Plot for C + I + G
    plt.plot(Y, AD_C_I_G, label='C + I + G (After Tax)')
    # Equilibrium point
    plt.annotate(f"Equilibrium (C + I + G (After Tax))",
                (np.interp(0, AD_C_I_G[::-1] - Y[::-1], Y[::-1]), np.interp(0, AD_C_I_G[::-1] - Y[::-1], Y[::-1])),
                textcoords="offset points", xytext=(-10,-10),
                ha='center', arrowprops=dict(facecolor='black', arrowstyle="->"))

    # Plot for C + I + G + NX
    plt.plot(Y, AD_C_I_G_NX, label='C + I + G + NX (After Tax)')
    # Equilibrium point
    plt.annotate(f"Equilibrium (C + I + G + NX (After Tax))",
                (np.interp(0, AD_C_I_G_NX[::-1] - Y[::-1], Y[::-1]), np.interp(0, AD_C_I_G_NX[::-1] - Y[::-1], Y[::-1])),
                textcoords="offset points", xytext=(-10,-10),
                ha='center', arrowprops=dict(facecolor='black', arrowstyle="->"))

    # Plot the 45-degree line
    plt.plot(Y, degree45_line, label='45 degree line (Y = AD)', linestyle='--', color='k')

    plt.xlabel('Income / Output (Y)')
    plt.ylabel('Aggregate Demand (AD)')
    plt.title('Keynesian Equilibrium')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt.gcf())  # Display the plot in streamlit


