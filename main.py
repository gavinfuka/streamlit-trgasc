import streamlit as st
from TriangleAsc import TriangleAsc
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
yf.pdr_override()

from VCP import VCP

# Title
st.title("VCP Finder")


# Sidebar input
st.sidebar.title("Ticker")
symbol = st.sidebar.text_input("Symbol")
region = st.sidebar.selectbox(
'Region',
('HK', 'US'))

if region == 'HK':
    symbol = str(symbol).zfill(4) + '.HK' 



# Sidebar clsf setting 
st.sidebar.markdown(
'''
# Triangular Ascending Parameters
- order:How many points on each side to use for the comparison to consider comparator(n, n+x) to be True.
- reduceTo : recurrsively find extrema until redeceTo is met
'''
)
order = st.sidebar.slider("Order",min_value=1,max_value=10,value=4)
#recursion options
recursion=st.sidebar.checkbox("recursion",value=False)
reduceTo = 3 
if recursion:
    reduceTo = st.sidebar.slider("reduceTo",min_value=1,max_value=10,value=5,step=1)

m = st.sidebar.slider("Starts From",min_value=100,max_value=250,value=200,step=10)
numExtrema = st.sidebar.slider("No. of Extrema",min_value=2,max_value=10,value=2,step=1)



if (symbol=="0000.HK"):
    st.markdown(
        '''
        ## Input Ticker to Begin!
        '''
    )

else:
    #yahoo finance API
    # @st.cache
    def fetch_yahoo(symbol):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()
        yahoo_data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        return yahoo_data

    yahoo_data = fetch_yahoo(symbol)
    # st.dataframe(yahoo_data)

    if len(yahoo_data['Close'])==0:
        st.markdown(
            '''
            ## No Record found!
            '''
        )

    else:

        # load model
        clsf = TriangleAsc(order=order,m=m,recursion=recursion,reduceTo=reduceTo,numExtrema=numExtrema)

        # if symbol in priceDict:
        # Classify
        isTrgAsc = clsf.Classify(yahoo_data['Close'])

        #VCP Conditions
        with st.expander("See conditions"):
            vcp = VCP(yahoo_data,symbol).Evaluate()
            st.write("Current Price > 150 SMA and > 200 SMA: ",vcp.Conditions["1"])
            st.write("Condition 2: 150 SMA and > 200 SMA: ",vcp.Conditions["1"])
            st.write("Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months): ",vcp.Conditions["1"])
            st.write("Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA: ",vcp.Conditions["1"])
            st.write("Condition 5: Current Price > 50 SMA: ",vcp.Conditions["1"])
            st.write("Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation): ",vcp.Conditions["1"])
            st.write("Condition 7: Current Price is within 25% of 52 week high: ",vcp.Conditions["1"])
            st.write("Condition 8: is Triangular Ascending: ",isTrgAsc)

        # st.write(vcp.isVCP)

        st.write("Is VCP",vcp.isVCP and isTrgAsc)
        if (vcp.isVCP and isTrgAsc):
            st.write("Rating:",vcp.RS)



        # Plot
        fig, ax = clsf.Plot(yahoo_data['Close'],symbol)
        st.pyplot(fig)















