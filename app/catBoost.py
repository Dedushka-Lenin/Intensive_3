from joblib import load

def catBoost(X_test):

    model = load('app\model\catBoostModel.joblib')  # Загружаем модель, она готова к использованию.

    y_pred = model.predict(X_test)

    return y_pred