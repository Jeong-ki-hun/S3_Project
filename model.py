import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from category_encoders import OrdinalEncoder
df = pd.read_csv("/Users/jeong-gihun/Desktop/Project_3/N_M.csv")

print(df.head())

X = df[["nc", "P", "Pr"]]
y = df["title"]

X_train = X
y_train = y


X_train = OrdinalEncoder().fit_transform(X_train)

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

pickle.dump(classifier, open("model.pkl", "wb"))