import streamlit as st
from load_data import *
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
from bokeh.plotting import figure
from bokeh.sampledata.autompg import autompg as df
import plotly.express as px
from Statistics import *



def main_page():
    st.title("Stock Dashboard\n "
             "## Portfolio analysis" )


    target = st.text_input('Enter stock symbol: ')
    target = target.upper()
    amount = st.text_input('Enter amount: ')

    if target and amount:
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

        st.write(portfolio)
        # df = portfolio.copy()
        # df['Weight'] = df['Weight'] * 100
        # fig = px.pie(df[['Weight']], names=df.index.values, title='Portfolio Weight', color_discrete_sequence=px.colors.sequential.RdBu)
        # st.plotly_chart(fig)

        fig2,ax2 = plt.subplots(1,1,figsize=(5,5))
        ax2 = plt.pie(portfolio.Weight*100, labels=portfolio.index.values, autopct='%1.1f%%', startangle=90)
        st.pyplot(fig2,width=200,height=200)

        portfolio_beta = round(portfolio['Adjbeta'].sum(), 4)
        portfolio_std = round(portfolio['AdjStd'].sum(), 4)
        st.write(f"""##### Portfolio Beta: {portfolio_beta}""")
        st.write(f'##### Portfolio Standard Deviation: {portfolio_std}%')




def sidebar_page():
    st.sidebar.write('This is a sidebar')



if __name__ == '__main__':
    main_page()
    sidebar_page()


