import streamlit as st
from load_data import *
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from Statistics import *
from Charting import *
import plotly.express as px


def main_page():
    st.title("Stock Dashboard\n "
             "## Portfolio analysis" )


    target = st.text_input('Enter stock symbol (eg: HAH,MSN,...): ')
    target = target.upper()
    amount = st.text_input('Enter amount (eg: 100,100,...): ',)
    with st.expander('Some information'):
        st.write("""
        - Correlation Matrix: Correlation between the stocks can indicate the "trend" between the stocks. 
        For example, if the correlation between the stocks is high, it means that the stocks are in the same direction.
        On the other hand, if the correlation is low, it means that the stocks are in different direction. 
        Therefore, if the portfolio have many stocks that are highly correlated, it can be a little bit too risky.
        - Weight: The weight of each stock in the portfolio. The weight is the amount of money that the stock is worth.
        - Beta: The tendency of the stock to move in the same direction as the index.
        - Adjusted beta (AdjBeta): Weight * Beta
        - Standard Deviation (Std): 68% return values lie within 1 standard deviation of the mean. 95% lie within 2 standard deviations. 
        - Adjusted Standard Deviation (AdjStd): Weight * Std 
        
        """)


    if target and amount :
        company_list = target.split(',')

        number_of_shares = amount.split(',')
        number_of_shares = [int(i) for i in number_of_shares]

        d = {}
        for name in company_list:
            d[name] = load_stock_data(name)

        data = d.copy()

        for name in company_list:
            data[name]['Pctchange'] = data[name].close.pct_change()
            data[name] = data[name]['Pctchange'].values

        # create dataframe from dictionary
        df_change = pd.DataFrame({name: list(pct_change) for name, pct_change in data.items()})
        df_change.dropna(inplace=True)
        df_change = df_change.clip(lower=-0.07)


        st.write("""
        ### Stock Statistics""")
        #correlation matrix
        corr = df_change.corr()
        st.write("""Correlation Matrix""",width = 1000)

        st.write(corr.style.background_gradient(cmap='BrBG_r'))

        st.write("""
        #
        """)

        #plot distribution of pct change
        fig, axes = plt.subplots(1, len(company_list) , figsize=(30, 10))
        for name, x in zip(company_list, range(len(company_list))):
            sns.histplot(data=df_change[name], ax=axes[x], kde=True, bins=35)
            # sns.lineplot(x=df_change[name], y=norm_cdf[name], ax=axes[1,x])
        st.pyplot(fig)


        #Portfolio monitoring
        st.write("""
                #
                """)
        st.write("""
        ### Portfolio monitoring""")
        lastestPrice = pd.DataFrame(columns=['Lastest Price', 'Number of Shares', 'Weight'], index=company_list)
        i = 0
        data = d.copy()
        for name in company_list:
            x = float(data[name].close.iloc[-1].values)
            lastestPrice['Lastest Price'].iloc[i] = x
            i += 1

        lastestPrice['Number of Shares'] = number_of_shares
        for i in range(len(company_list)):
            lastestPrice['Weight'].iloc[i] = round(
                (lastestPrice['Number of Shares'].iloc[i] * lastestPrice['Lastest Price'].iloc[i]) / sum(
                    lastestPrice['Number of Shares'] * lastestPrice['Lastest Price']), 4)
        portfolio = pd.DataFrame(index=company_list, columns=['Weight', 'Beta', 'Adjbeta', 'Std', 'AdjStd'])
        portfolio.Weight = lastestPrice.Weight
        # Collecting data and calculate beta for each symbol
        index = 'VN'
        start = '2020-01-01'
        # create dictionary for company's beta
        Risk_indicator = {}
        for name in company_list:
            company = risk_analysis(name, index, start)
            beta = float(company.calculate_beta())
            std = float(company.calculate_std())
            Risk_indicator[name] = beta, std
        x = Risk_indicator.copy()
        df_risk = pd.DataFrame.from_dict(Risk_indicator, orient='index', columns=['Beta', 'Std'])
        portfolio['Beta'] = df_risk.Beta.values
        portfolio['Adjbeta'] = portfolio['Beta'] * portfolio['Weight']
        portfolio['Std'] = df_risk.Std.values
        portfolio['AdjStd'] = portfolio['Std'] * portfolio['Weight']

        st.write(portfolio, use_container_width=True)

        # fig2,ax2 = plt.subplots(1,1,figsize=(5,5))
        # ax2 = plt.pie(portfolio.Weight*100, labels=portfolio.index.values, autopct='%1.1f%%', startangle=90)
        # st.pyplot(fig2,width=200,height=200)
        pie = px.pie(portfolio.Weight*100, values='Weight', names=portfolio.index, title='Portfolio Weight', color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(pie, use_container_width=True)
        portfolio_beta = round(portfolio['Adjbeta'].sum(), 4)
        portfolio_std = round(portfolio['AdjStd'].sum(), 4)
        st.write(f"""##### Portfolio Beta: {portfolio_beta}""")
        st.write(f'##### Portfolio Standard Deviation: {portfolio_std}%')
    else:
        st.write("Missing stock or number of stock")



def sidebar_page():
    st.markdown(
        f'''
            <style>
                .sidebar .sidebar-content {{
                    width: 150px;
                }}
            </style>
        ''',
        unsafe_allow_html=True
    )
    st.sidebar.write("""
    ### Some notes
    Although there are lots og problem with this program such as:\n
    - The data is not well organized
    - Some missing data can lead to wrong result or even not working
    
    However, this program can help people to understand the concept of portfolio and how to use it to make a better decision.
    Risk monitoring is the main purpose of this program.
        
    ***
    To use this program:
    - Choose the stocks and amount of stocks, there must be at least 2 stocks and the number of stocks must be bigger than 100
    
    ***
    Info: [Github](https://github.com/hungha11)
    """)



if __name__ == '__main__':
    st.set_page_config(page_title='Portfolio Risk Monitoring', page_icon='📈',layout='wide')
    main_page()
    sidebar_page()

