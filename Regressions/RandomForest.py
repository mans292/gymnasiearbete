# Import necessary libraries
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import get_scorer_names

df = pd.read_csv('Lägenheter_med_koordinater_slutgiltig.csv', sep=',')



df_list = [
    df
]
for df in df_list:

    X = df[['Antal rum', 'Boarea', 'Finns_hiss', 'Driftkostnad', 'Avgift', 'Våning', 'Uteplats', 'medelinkomst_månad', 'postnummer', 'latitude', 'longitude']]
    y = (df['slutpris'])

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42)


    train_data = X_train.join(y_train)
    train_data['Avgift'] = train_data['Avgift'] + 1
 
    train_data['kvm/rum'] = train_data['Boarea'] / train_data['Antal rum']
    train_data['kvm/driftkostnad'] = train_data['Boarea'] / train_data['Driftkostnad']
    train_data['medelinkomst/driftkostnad'] = train_data['medelinkomst_månad'] / train_data['Driftkostnad']
    train_data['total_kostnad'] = train_data['Avgift'] * 12 + train_data['Driftkostnad']
    train_data['medelinkomst/avgift'] = train_data['medelinkomst_månad']/train_data['Avgift']
    train_data['Våning'] = train_data['Våning'] + 3


    test_data = X_test.join(y_test)
    test_data['Avgift'] = test_data['Avgift'] + 1
    
    test_data['kvm/rum'] = test_data['Boarea'] / test_data['Antal rum']
    test_data['kvm/driftkostnad'] = test_data['Boarea'] / (test_data['Driftkostnad'])
    test_data['medelinkomst/driftkostnad'] = test_data['medelinkomst_månad'] / (test_data['Driftkostnad'])
    test_data['total_kostnad'] = test_data['Avgift'] * 12 + test_data['Driftkostnad']
    test_data['medelinkomst/avgift'] = test_data['medelinkomst_månad']/test_data['Avgift']
    test_data['Våning'] = test_data['Våning'] + 3


 
 
    X_train, y_train = train_data.drop(columns=['slutpris', 'Finns_hiss', 'Uteplats']), train_data['slutpris']
    X_test, y_test = test_data.drop(columns=['slutpris', 'Finns_hiss', 'Uteplats']), test_data['slutpris']


    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    rf_model = RandomForestRegressor(n_estimators=200, random_state=42, verbose=True)

    '''''
    plt.figure(figsize=(15,8))
    sns.heatmap(train_data.corr(), annot=True)
    plt.show()
    '''''

    rf_model.fit(X_train, y_train)
    rf_y_pred = rf_model.predict(X_test)


    mae_rf = mean_absolute_error((y_test), rf_y_pred)
    r2_rf = r2_score((y_test), rf_y_pred)

   
    print(f'MAE - rf: {mae_rf}')
    print(f'R^2 Score - rf: {r2_rf}')




