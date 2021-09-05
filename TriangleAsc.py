
from scipy.signal import argrelextrema
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

import streamlit as st


class TriangleAsc:
    def __init__(self,order=5,m=150,recursion=True,reduceTo=5,numExtrema=2):
        '''
        order:How many points on each side to use for the comparison to consider comparator(n, n+x) to be True.
        m: starts from
        reduceTo : recurrsively find extrema until redeceTo is met
        '''
        self.model_localmin = LinearRegression()
        self.model_localmax = LinearRegression()
        self.order = order
        self.m = m 
        self.recursion = recursion
        self.reduceTo = reduceTo
        self.numExtrema = numExtrema
        self.contractionPattern = []

    def findExtrema(self, x,y , mode='max',order=1, recursion=True):
        if mode == 'min':
            self.comparatator = np.less
        else:
            self.comparatator = np.greater
        localextrema = argrelextrema(np.array(y), self.comparatator,order=order)[0]
        localext_x = []
        localext_y = []
        for e in localextrema:
            localext_x.append(x[e])
            localext_y.append(y[e])

        if recursion and len(localextrema) > self.reduceTo:
            localext_x,localext_y = self.findExtrema(localext_x,localext_y,mode=mode,recursion=True)


    
        return localext_x,localext_y

    def Classify(self,y):
        #original
        x = np.linspace(1,len(y),len(y))
        #m= np.argmin(y)

        localmin_x,localmin_y = self.findExtrema(x,y,mode='min',recursion=self.recursion, order=self.order)
        localmax_x,localmax_y = self.findExtrema(x,y,mode='max',recursion=self.recursion, order=self.order)


        self.localmin_x = localmin_x
        self.localmin_y = localmin_y

        self.localmax_x = localmax_x
        self.localmax_y=localmax_y

        numExtrema = self.numExtrema
        self.model_localmin.fit(np.array(localmin_x[-numExtrema:]).reshape(-1,1),np.array(localmin_y[-numExtrema:]).reshape(-1,1))
        self.model_localmax.fit(np.array(localmax_x[-numExtrema:]).reshape(-1,1),np.array(localmax_y[-numExtrema:]).reshape(-1,1))


        return self.model_localmin.coef_[0][0] > self.model_localmax.coef_[0][0] and (self.model_localmin.coef_[0][0]>0)

    def Plot(self,y,title=''):

        fig, ax = plt.subplots()
        x = np.linspace(1,len(y),len(y))
        plt.plot(x,y)

        plt.title(title)
        x_new = np.linspace(self.m,len(y)-1,len(y)-self.m)
        y_new_min = self.model_localmin.predict(x_new[:, np.newaxis])
        y_new_max = self.model_localmax.predict(x_new[:, np.newaxis])
        

        m = self.m
        #local minima 
        plt.scatter(self.localmin_x[-m:],self.localmin_y[-m:],color='r')
        #local maxima
        plt.scatter(self.localmax_x,self.localmax_y,color='g')            


        plt.plot(x_new, y_new_min,label='support',color='r')
        plt.plot(x_new, y_new_max,label='resistance',color='g')
        plt.legend()
        return fig, ax



    def EstContraction(self,index):
        max_idx = index

        #cm here
        # st.write(self.localmax_x[index])
        # st.write(self.localmin_x[index])
        if self.localmax_x[max_idx] >  self.localmin_x[index]:
            max_idx = max_idx-1

        y_max = self.localmax_y[max_idx]
        y_min = self.localmin_y[index]

        x = [self.localmax_x[max_idx],self.localmin_x[index]]
        y1 = [y_max,y_max]
        y2 = [y_min,y_min]
        percent = (self.localmax_y[index]-self.localmin_y[index])/self.localmax_y[index] 
        return x, y1, y2, percent
        

    def PlotContraction(self,y,title=''):
        fig, ax = plt.subplots()
        x = np.linspace(1,len(y),len(y))
        plt.plot(x,y)
        plt.title(title)


        for idx in [-3,-2,-1]:
            try:
                x, y1, y2, percent = self.EstContraction(idx)
                self.contractionPattern.append(percent)
                plt.plot(x,y1,'-')
                plt.plot(x,y2,'-')
                label = f"{round(percent*100)}%" 
                st.write(len(x),len(y1),len(y2))
                plt.fill_between(x, y1, y2, where=(y1 > y2) , alpha=0.3, label=label)
            except Exception as e:
                print(e)
                st.write(e)
        plt.legend()
        return fig, ax
