class VCP:
    def __init__(self,data,symbol):
        self.symbol = symbol
        self.data = data


    def CalculateRS(self,df):
        quarter = -63
        try:
            ThreeMthRS = 2* df['Close'][-1]/ df['Close'][-quarter*1-1] 
            SixMthRS =  df['Close'][-1]/df['Close'][-quarter*2-1] 
            NineMthRS = df['Close'][-1]/df['Close'][-quarter*3-1] 
            TwelveMthRS = df['Close'][-1]/df['Close'][0]

            RS_Rating = ThreeMthRS + SixMthRS + NineMthRS + TwelveMthRS

        except:
            print('[x] RS Rating Not caculated. Length of df' + str(len(df)))
            RS_Rating = 0

        return RS_Rating



    def Evaluate(self):
        df = self.data
        try:
            self.RS = self.CalculateRS(df)   
            sma = [50, 150, 200]
            for x in sma:
                # ClosingP = df.iloc[:,4]
                ClosingP = df.Close
                Rolled = ClosingP.rolling(window=x)
                Mean = Rolled.mean()
                df["SMA_"+str(x)] = round(Mean,2)

            currentClose = df["Adj Close"][-1]
            moving_average_50 = df["SMA_50"][-1]
            moving_average_150 = df["SMA_150"][-1]
            moving_average_200 = df["SMA_200"][-1]
            low_of_52week = min(df["Adj Close"][-260:])
            high_of_52week = max(df["Adj Close"][-260:])
            
            try:
                moving_average_200_20 = df["SMA_200"][-20]

            except Exception:
                moving_average_200_20 = 0

            Conditions = {
                '1':(currentClose > moving_average_150 > moving_average_200),
                '2': (moving_average_150 > moving_average_200),
                '3': (moving_average_200 > moving_average_200_20),
                '4': (moving_average_50 > moving_average_150 > moving_average_200),
                '5': (currentClose > moving_average_50),
                '6': (currentClose >= (1.3*low_of_52week)),
                '7': (currentClose >= (.75*high_of_52week)),
            }
            self.Conditions= Conditions

            #selectedConditions = [boolean for i,boolean in Conditions.items() if i in config['Conditions']['include']]
            selectedConditions = [boolean for i,boolean in Conditions.items()]

            if( False not in selectedConditions):
                self.isVCP = True
            else:
                self.isVCP = False 

                                
        except Exception as e:
            print (e)
            return e


        return self