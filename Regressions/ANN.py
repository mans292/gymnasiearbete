import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler




df = pd.read_csv('final_houses.csv', sep=',')



X = df[['medelinkomst_månad', 'Antal_rum', 'Boarea', 'Biarea', 'Tomtarea', 'Driftkostnad']]
poly = PolynomialFeatures(interaction_only=True, include_bias=False)
X_interactions = poly.fit_transform(X)
y = np.log1p(df['slutpris'])




X_train, X_test, y_train, y_test = train_test_split(X_interactions, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


model = MLPRegressor(hidden_layer_sizes=(16, 16), max_iter=5000, random_state=42, 
                      learning_rate_init=0.001, activation='logistic', verbose=True, alpha=0.01)

model.fit(X_train_scaled, y_train)


y_pred = model.predict(X_test_scaled)


mae = mean_absolute_error(np.expm1(y_test), np.expm1(y_pred))  
r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))

print(f'Error: {mae}')
print(f'R^2 Score: {r2}')





