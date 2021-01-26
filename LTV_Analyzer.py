#!/usr/bin/env python
# coding: utf-8

# In[143]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob, os
class LTV_Analyzer:   
    def __init__(self, path, subscription_value = 9.99):
        self.data = pd.read_csv(path)
        self.data = self.data.sort_values(by = ['Event Date'])   #Ensuring that database is sorted by date
        self.subscription_value = subscription_value
    
    
    '''
    This function counts overall LTV with respect to comission given and income from each convertion
        def count_LTV(self, data)
        INPUT:
            data[pd.DataFrame] - database to analyze
        OUTPUT:
            income[np.array] - a 6-element numpy array which stores overall LTV 
                               and income from each new convertion (1st to 2nd, 2nd to 3rd and so on)
    '''
    def count_LTV(self, data, comission = 0.3):
        buys = np.array(data['Subscriber ID'].value_counts().value_counts())   # number of people on each buy
        unique_clients = len(data['Subscriber ID'].value_counts())             # number of unique clients 
        buys[0] = unique_clients                                               # setting that first buy (free week) was made by every person
        dev_proceeds = self.subscription_value*(1-comission)*unique_clients    # maximum LTV with substracted comission from income

        ###  Counting LTV and income by each convolution  ###
        income = [dev_proceeds, 0, 0, 0, 0, 0]       # output
        LTV = 0
        for i in range(1, len(buys)):
            conv_on_step = buys[i]/buys[i-1]         # fraction of people from previous buy to new one
            income[i] = round(income[i-1]*conv_on_step,2)     # income from people who got from i-1 to i week
            LTV += income[i]
        income[0] = LTV                   
        return income

    '''
    This function splits database in two: for Apple users and Android users
    and counts overall LTV and income with respect to comission of each platform
    (30% - Apple, 0% - Android)
        INPUT:
        
        OUTPUT:
            income[np.array] - a 6-element numpy array which stores overall LTV 
                               and income from each new convertion (1st to 2nd, 2nd to 3rd and so on)
    '''
    def get_LTV(self):
        data = self.data
        # Counting for apple users
        apple_data = data.loc[data['App Apple ID'] == 1]
        apple_LTV = [0.,0.,0.,0.,0.,0.]
        if (len(apple_data) > 0):
            apple_LTV = self.count_LTV(apple_data)
        # Counting for android users
        android_data = data.loc[data['App Apple ID'] != 1]
        android_LTV = [0.,0.,0.,0.,0.,0.]
        if (len(android_data) > 0):
            android_LTV = self.count_LTV(android_data, 0)
            
        overall_LTV = np.add(apple_LTV, android_LTV)
        return overall_LTV

    '''
    This function counts every convolution (from trial to 1st buy, from 1st to 2nd and so on)
        def count_convolutions(self, data)
        INPUT:
            data[pd.DataFrame] - database to analyze
        OUTPUT:
            convolutions[np.array] - a 5-element array representing convertions
    '''
    def count_convolutions(self):
        buys = np.array(self.data['Subscriber ID'].value_counts().value_counts())   # number of people on each buy
        unique_clients = len(self.data['Subscriber ID'].value_counts())             # number of unique clients 
        buys[0] = unique_clients                                               # setting that first buy (free week) was made by every person
        
        ###  Counting convolutions  ###
        convolutions = [0, 0, 0, 0, 0]
        for i in range(1, len(buys)):
            convolutions[i-1] = buys[i]/buys[i-1]         # fraction of people from previous buy to new one
        return convolutions
    
    '''
    Function used to count buys and trial starts by weekdays
    Needed in get_and_save_plots function (plot №3)
        INPUT:
            self
        OUTPUT:
            count_for_trial + count_for_buys (list)  -  first seven numbers(count_for_trial): number of trials for every weekday,
                                                        last seven numbers(count_for_buys): number of buys for every weekday.
    '''
    def count_buys_by_weekdays(self):
        days_for_trial = []        # list to save weekdays of a trial starts
        days_for_buy = []          # list ot save weekdays when buy is made
        for i in range(len(self.data)):
            # If Subscription Offer Type is Free Trial then save to days_for_trial, else save to days_for_buy
            if self.data['Subscription Offer Type'].iloc[i] == 'Free Trial':
                days_for_trial.append(datetime.datetime(int(self.data['Event Date'].iloc[i][:4]), int(self.data['Event Date'].iloc[i][5:7]), int(self.data['Event Date'].iloc[i][8:])).weekday())            
            else:
                days_for_buy.append(datetime.datetime(int(self.data['Event Date'].iloc[i][:4]), int(self.data['Event Date'].iloc[i][5:7]), int(self.data['Event Date'].iloc[i][8:])).weekday())           
        # Counting by days itself
        count_for_trial = []
        count_for_buys = []
        for day in range(0,7):
            # Count weekdays when trial had started      
            count_for_trial.append(days_for_trial.count(day))
            # Count weekdays when user bought subscription
            count_for_buys.append(days_for_buy.count(day))
            
        return count_for_trial + count_for_buys
            
    
    '''
    This function builds and saves different plots based on the database
        INPUT:
            self
        OUTPUT:
            photos_paths(list) - paths to all plots
    '''
    def get_and_save_plots(self):
        # clearing out the photos directory
        files = glob.glob('data/photos/*')
        for f in files:
            os.remove(f)
            
        photos_paths = []
        #Plots for convolutions and income by convolutions
        names = ['Конволюція 1', 'Конволюція 2','Конволюція 3','Конволюція 4','Конволюція 5']
       
        convolutions = self.count_convolutions()
        fig, ax = plt.subplots(figsize=(11.5, 5.5))
        ax.bar(names, convolutions, color='b')
        plt.suptitle('Усі конволюції', size = 24)
        fig.savefig('data/photos/photo1.png')
            
        income = self.get_LTV()
        fig, ax = plt.subplots(figsize=(11.5, 5.5))
        ax.plot(names, income[1:], color='b', linewidth=2, markersize=12, marker = 'o')
        plt.suptitle('Заробіток с кожної конволюції', size = 24)
        fig.savefig('data/photos/photo2.png')
        
        
        #Plot for date/weekday statistics
        names = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'НД']
        days = self.count_buys_by_weekdays()
        days[7:] = (i * (-1) for i in days[7:])
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, days[:7], color='r', label = 'Кількість пробних періодів')
        ax.bar(names, days[7:], color='b', label = 'Кількість купівель')
        ax.legend(bbox_to_anchor=(1, 0), loc='lower center', ncol=1)
        plt.suptitle('Кількість купівель та пробних періодів у кожен день тижня', size = 16)
        fig.savefig('data/photos/photo3.png')
        
        
        # Plot for number of proceeds for every currency
        num_of_proceeds = self.data['Proceeds Currency'].value_counts()
        names = num_of_proceeds.index
        fig, ax = plt.subplots(figsize=(16, 5.5))
        ax.bar(names, num_of_proceeds, color='b')
        plt.suptitle('Кількість купівель по кожній валюті', size = 24)
        fig.savefig('data/photos/photo4.png')
        
        
        # Plot for device distribution
        device_distributon = self.data['Device'].value_counts()
        names = device_distributon.index
        fig, ax = plt.subplots(figsize=(11.5, 5.5))
        ax.bar(names, device_distributon, color='b')
        plt.suptitle('Розподілення користувачів за девайсами', size = 24)
        fig.savefig('data/photos/photo5.png')
        
        for i in range(1, 6):
            photos_paths.append('data/photos/photo' + str(i) + '.png')
        return photos_paths


# In[ ]:




