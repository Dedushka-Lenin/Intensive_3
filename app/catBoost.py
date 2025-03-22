from catboost import CatBoostRegressor

def catBoost(X_train, y_train, X_test):

    model = CatBoostRegressor(iterations=500, learning_rate=0.2, depth=4, verbose=0)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return y_pred