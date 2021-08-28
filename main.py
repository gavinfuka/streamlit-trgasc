import streamlit as st
from TriangleAsc import TriangleAsc
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
yf.pdr_override()



# Title
st.title("Triangular Ascending")


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
# Alorithm Parameters
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
    @st.cache
    def fetch_yahoo(symbol):
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.date.today()
        yahoo_data = pdr.get_data_yahoo(symbol, start=start_date, end=end_date)
        return yahoo_data

    yahoo_data = fetch_yahoo(symbol)
    st.dataframe(yahoo_data)

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


        # Plot
        fig, ax = clsf.Plot(yahoo_data['Close'],symbol)
        st.pyplot(fig)


        #Results
        st.write("Is triangular ascending:")
        st.write(isTrgAsc)




















# %%
# clsf = TriangleAsc(order=20,m=150,recursion=False,reduceTo=5)

# priceDict = {}

# for d in data:
#     try:
#         symbol, close, *_ = d.split(':')
#         symbol, close, *_ = d.split(':')
#         close = json.loads(close)
#         priceDict[symbol] = close
#     except Exception as e :
#         print(e)       
# for symbol in filterList['Stock']:
#     try:
#         close = priceDict[symbol]
#         clsf.Classify(close)
#         clsf.Plot(close,title=symbol)
#     except Exception as e: 
#         print(e)
# #%%

# clsf.Plot(priceDict['0558.HK'],title=symbol)


