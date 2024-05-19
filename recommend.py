import pandas as pd
from sklearn.decomposition import PCA
import numpy as np
from pandas import DataFrame as df
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('auto_data.csv')
def predict_most_influential_feature(data=df, targetName='Fraud'):
    seed = 1151
    np.random.seed(seed)

    # encode any categorical variables
    categorical_columns_object = df.select_dtypes(include=['object']).columns.tolist()  # list of column names
    df_encoded = pd.get_dummies(df, columns=categorical_columns_object)

    # set matrix of features and target
    features = df_encoded.drop(columns=[targetName], axis=1)
    target = df_encoded[targetName]

    # standardize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_encoded[features.columns])    

    # conduct pca
    pca = PCA(n_components=2, random_state=seed)
    X_pca = pca.fit_transform(scaled_features)
    pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
    loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2'], index=features.columns)

    # state the most influential features for the 2 principal components
    most_influential_features_pc1 = loadings['PC1'].abs().nlargest(2).index 
    most_influential_features_pc2 = loadings['PC2'].abs().nlargest(2).index
    
    liste = []
    for index_values in most_influential_features_pc1:
        liste.append(index_values)
    for index_values in most_influential_features_pc2:
        
        liste.append(index_values)
    
    return liste