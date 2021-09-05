import streamlit as st
from TriangleAsc import TriangleAsc
from pandas_datareader import data as pdr
import yfinance as yf
import datetime
yf.pdr_override()

from VCP import VCP

# Title
st.title("Stock Suggestor")


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
            st.write("Condition 1: Current Price > 150 SMA and > 200 SMA")
            st.write("Condition 2: Condition 2: 150 SMA and > 200 SMA")
            st.write("Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)")
            st.write("Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA")
            st.write("Condition 5: Current Price > 50 SMA")
            st.write("Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before coming out of consolidation)")
            st.write("Condition 7: Current Price is within 25% of 52 week high")
            st.write("Condition 8: is Triangular Ascending")

        #VCP Conditions
        with st.expander("See results"):
            vcp = VCP(yahoo_data,symbol).Evaluate()
            st.write("Condition 1: ",vcp.Conditions["1"])
            st.write("Condition 2: ",vcp.Conditions["2"])
            st.write("Condition 3: ",vcp.Conditions["3"])
            st.write("Condition 4: ",vcp.Conditions["4"])
            st.write("Condition 5: ",vcp.Conditions["5"])
            st.write("Condition 6: ",vcp.Conditions["6"])
            st.write("Condition 7: ",vcp.Conditions["7"])
            st.write("Condition 8: ",isTrgAsc)

        if (vcp.isVCP):
            if (isTrgAsc):
                st.write("All Conidtions Met")
            else:
                st.write("Conidtions 1 - 7 Met")
            st.write("Rating:",vcp.RS)

        else:
            st.write(" Not Reccomended !")


        # Plot
        fig, ax = clsf.Plot(yahoo_data['Close'],symbol)
        st.pyplot(fig)


        Contraction = "-->".join([f"{round(i*100)}%" for i in clsf.contractionPattern])
        st.title ("Contraction Pattern")
        st.write(Contraction)


        fig, ax = clsf.PlotContraction(yahoo_data['Close'],symbol)
        st.pyplot(fig)










