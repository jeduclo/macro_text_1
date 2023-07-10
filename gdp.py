import streamlit as st
from stats_can import StatsCan
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff  # Add this line
import pandas as pd
import datetime



def run_gdp_app():
    # import and clean Data
    @st.cache_data
    def clean_data():
        sc = StatsCan()
        dp = sc.table_to_df("36-10-0104-01")

        # Rename columns, and filter rows based on 'Seasonal adjustment', 'Prices' and 'UOM'
        df = (dp.rename(columns={'REF_DATE': 'date', 'Estimates': 'component', 'VALUE': 'value'})
                .loc[dp['Seasonal adjustment'] == 'Seasonally adjusted at annual rates']
                .loc[dp['Prices'] == 'Chained (2012) dollars']
                .loc[dp['UOM'] == 'Dollars']
                .reset_index(drop=True))

        # Keep only the 'date', 'component' and 'value' columns
        df = df[['date','component','value']].copy()

        # Reset index
        df = df.reset_index(drop=True)

        # Keep only rows where 'component' is in the provided list
        df = df.loc[df['component'].isin(['Final consumption expenditure',
                                            'Gross fixed capital formation',
                                            'Investment in inventories',
                                            'Exports of goods and services',
                                            'Less: imports of goods and services',
                                            'Statistical discrepancy',
                                            'Gross domestic product at market prices',
                                            'Final domestic demand'])].copy()

        # Reset index
        df = df.reset_index(drop=True)
        return df
    
    start_date = pd.Timestamp(st.sidebar.date_input("Start date", datetime.date(2020, 1, 1)))
    end_date = pd.Timestamp(st.sidebar.date_input("End date", datetime.date.today()))

    if start_date > end_date:
        st.sidebar.error("The end date must fall after the start date.")

    def filter_by_date(df, start_date, end_date):
        # ensure dates are in the right format
        df['date'] = pd.to_datetime(df['date'])

        # filter by date range
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        df_filtered = df.loc[mask]

        df_filtered['date'] = pd.to_datetime(df_filtered['date']).dt.date

        return df_filtered

    # you need to call the function and pass the dataframes returned by clean_data() function 
    df = clean_data()
    df_filtered = filter_by_date(df, start_date, end_date)

    ###
    df_filtered=df_filtered.reset_index(drop=True)

    @st.cache_data
    def convert_df_to_csv(df_filtered):
        return df_filtered.to_csv().encode("utf-8")


    ############
    st.subheader("Canadian Economic Indicators: National Accounts Data Visualization")
    



    #########
    ## data preview part
    data_exp = st.expander("Preview of National Accounting Data.")
    data_exp.dataframe(df_filtered)

    csv_file = convert_df_to_csv(df_filtered)
    data_exp.download_button(
        label="Download selected as CSV",
        data=csv_file,
        file_name="can_gdp.csv",
        mime="text/csv",
    )
            
            
    st.subheader("National Accounting Analysis")

    # Calculate monthly change in cpi by region and product
    default_components = ['Gross domestic product at market prices'] 
    components = st.multiselect('Choose components', options=list(df['component'].unique()),default=default_components)

    questions = ['1- What are the trends in different components of the national account over time?',
                '2- Which component has the highest average yearly growth rate?',
                '3- Which component has the highest value for the last quarter?',
                '4- What are the trends in growth rate of the different components over time?',
                '5- What is the correlation between different components of national accounts?'
                ]


    
    question = st.selectbox("Select a question to answer", questions)

    if not components:
         st.error("Please select at least one component.")
    else:
        None
    # Now based on the selected question, display the corresponding plot
    if question == '1- What are the trends in different components of the national account over time?':
        fig = go.Figure()
        for component in components:
            component_df = df_filtered[df_filtered['component'] == component]
            fig.add_trace(go.Scatter(x=component_df['date'], y=component_df['value'], name=component))
        fig.update_layout(autosize=True, title='Component Trends Over Time',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1))

        st.plotly_chart(fig)

        fig = go.Figure()
        for component in components:
            component_df = df_filtered[df_filtered['component'] == component]
            fig.add_trace(go.Bar(x=component_df['date'], y=component_df['value'], name=component))
        fig.update_layout(autosize=True, barmode='stack',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1))

        st.plotly_chart(fig)

    elif question == '2- Which component has the highest average yearly growth rate?':
        df1 = df_filtered.copy()

        # Filter data for selected components
        filtered_df1 = df1[df1['component'].isin(components)]
        # Calculate yearly change in value for each component
        filtered_df1['yearly_change'] = filtered_df1.groupby('component')['value'].pct_change(4)
        # Calculate average yearly change for each component
        avg_yearly_change = filtered_df1.groupby('component')['yearly_change'].mean().reset_index()
        # Create bar chart
        fig = px.bar(avg_yearly_change, x='component', y='yearly_change')
        st.plotly_chart(fig)

    elif question == '3- Which component has the highest value for the last quarter?':
        df = df_filtered.copy()
        max_date = df['date'].max()

        # Filter data for selected components and the last quarter
        filtered_df = df[(df['component'].isin(components)) & (df['date'] == max_date)]
        
        # Create bar chart
        fig = px.bar(filtered_df, x='component', y='value')
        st.plotly_chart(fig)

    elif question == '4- What are the trends in growth rate of the different components over time?':
        # Compute yearly change (growth rate) for each component
        df_filtered['yearly_change'] = df_filtered.groupby('component')['value'].pct_change(4) * 100  # multiply by 100 to get percentage

        # Filter dataframe based on selected components
        filtered_df = df_filtered[df_filtered['component'].isin(components)]

        # Create line plot for each component
        fig = go.Figure()
        for component in components:
            component_df = filtered_df[filtered_df['component'] == component]
            fig.add_trace(go.Scatter(x=component_df['date'], y=component_df['yearly_change'], name=component))

        # Update layout to place the legend below the chart
        fig.update_layout(autosize=True, title='Yearly Change in Component Values Over Time',
                        legend=dict(orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1))

        st.plotly_chart(fig)


    elif question == '5- What is the correlation between different components of national accounts?':
        # Pivot the data to get components as columns
        pivot_df = df_filtered.pivot(index='date', columns='component', values='value')
        
        # Compute correlation matrix
        correlation_matrix = pivot_df.corr()

        # Create a heatmap
        fig = ff.create_annotated_heatmap(
            z=correlation_matrix.values,
            x=list(correlation_matrix.columns),
            y=list(correlation_matrix.index),
            annotation_text=correlation_matrix.round(2).values,
            colorscale='Blues',
            showscale=True)

        # Update layout
        fig.update_layout(
            #title='Correlation Between Different Components of National Accounts',
            xaxis_nticks=len(correlation_matrix.columns),
            yaxis_nticks=len(correlation_matrix.columns),
            autosize=False,
            width=800, 
            height=600,
            margin=dict(t=100, b=100, l=100, r=100),
        )
        st.plotly_chart(fig)

    
