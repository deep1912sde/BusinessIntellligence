import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pyodbc

# Connect to the AdventureWorks2019 database
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-79VIGL8U\\SQLEXPRESS;DATABASE=DWAdventureWorks;UID=sa;PWD=3692587')

# Create a cursor object
cursor = cnxn.cursor()


query = """
SELECT TOP 10 JobTitle, COUNT(*) as TotalEmployees
FROM [DWAdventureWorks].[dbo].[Humanresource_dim]
GROUP BY JobTitle
ORDER BY TotalEmployees DESC
"""

# execute the query and store the results in a Pandas DataFrame
df11 = pd.read_sql_query(query, cnxn)

query4 = '''
SELECT TOP 10
    p.[Name] AS ProductName,
    SUM(od.[OrderQty]) AS TotalQuantity
FROM 
    [DWAdventureWorks].[dbo].[sales_fact] od
    
GROUP BY 
    p.[Name]
ORDER BY 
    SUM(od.[OrderQty]) DESC
'''

# Execute the query and store the results in a pandas dataframe
df0 = pd.read_sql_query(query4, cnxn)


query1 = """
SELECT YEAR(OrderDate) AS Year, SUM(TotalDue) AS TotalSales
FROM [DWAdventureWorks].[dbo].[OutPutTable]
GROUP BY YEAR(OrderDate)
ORDER BY YEAR(OrderDate)
"""

gender_query = '''SELECT Gender, COUNT(*) as NumEmployees FROM [DWAdventureWorks].[dbo].[Humanresource_dim] GROUP BY Gender'''
gender_df = pd.read_sql(gender_query, cnxn)

query = "SELECT YEAR(OrderDate) as Year, COUNT(*) as NumOrders FROM [DWAdventureWorks].[dbo].[OutPutTable] GROUP BY YEAR(OrderDate) ORDER BY Year"
orders_df = pd.read_sql(query, cnxn)
orders_df['Year'] = orders_df['Year'].astype(str).str.replace(',', '')

# Read data into a pandas dataframe
sales_df1 = pd.read_sql(query1, cnxn)

# Remove commas from the Year column
sales_df1['Year'] = sales_df1['Year'].astype(str).str.replace(',', '')

query = "SELECT ProductCategory.Name, SUM(SafetyStockLevel) AS TotalSafetyStock FROM [DWAdventureWorks].[dbo].[production_dim] GROUP BY ProductCategory.Name;"
df = pd.read_sql_query(query, cnxn)


# Define the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    # Header
    html.H1(children='Business Intelligence 2023', style={'textAlign': 'center'}),

    # Dropdown menu for selecting the page
    dcc.Dropdown(
        id='page-dropdown',
        options=[
            {'label': 'Employees', 'value': 'employees'},
            {'label': 'Production', 'value': 'production'},
            {'label': 'Orders', 'value': 'orders'},

        ],
        value='employees'
    ),

    # Div for displaying the page content
    html.Div(id='page-content'),


])

# Define the style for the left and right graphs
graph_style = {
    'width': '49%',
    'height': '400px',
    'display': 'inline-block',
    'text-align': 'center',
    'vertical-align': 'top'
}


# Define the page 1 layout
page1_layout = html.Div(children=[
    # First graph
    dcc.Graph(
        id='graph1-page1', style=graph_style,
            figure=px.pie(gender_df, values=gender_df['NumEmployees'], names=gender_df['Gender'])
    ),


    # Second graph
    dcc.Graph(
        id='graph2-page1',style=graph_style,
            figure=px.bar(df11, x='JobTitle', y='TotalEmployees')



    )
])

# Define the page 2 layout
page2_layout = html.Div(children=[
    # First graph
    dcc.Graph(
        id='graph1-page2',style=graph_style,
        figure=px.line(sales_df1, x=sales_df1['Year'], y=sales_df1['TotalSales'])
    ),

    # Second graph
    dcc.Graph(
        id='graph2-page2',style=graph_style,
        figure=px.bar(df0, x='ProductName', y='TotalQuantity')
    )
])

# Define the page 3 layout
page3_layout = html.Div(children=[
    # First graph
    dcc.Graph(
        id='graph1-page3',style=graph_style,
        figure=px.line(orders_df, x='Year', y='NumOrders')
    ),

    # Second graph
    dcc.Graph(
        id='graph2-page3',style=graph_style,
            figure=px.bar(df, x=df['Name'], y= df['TotalSafetyStock'])
    )
])

# Callback for displaying the page content based on the dropdown menu
@app.callback(
    Output('page-content', 'children'),
    Input('page-dropdown', 'value')
)
def display_page(page):
    if page == 'employees':
        return page1_layout
    elif page == 'production':
        return page2_layout
    elif page == 'orders':
        return page3_layout


if __name__ == '__main__':
    app.run_server(debug=True)
