import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px  # noqa:  F401
import plotly.graph_objs as go
import seaborn as sn
from sklearn.linear_model import LinearRegression


# This function uses plotly.express
def compare_passenger_capacity_exp(preprocessed_shuttles: pd.DataFrame):
    return (
        preprocessed_shuttles.groupby(["shuttle_type"])
        .mean(numeric_only=True)
        .reset_index()
    )


# This function uses plotly.graph_objects
def compare_passenger_capacity_go(preprocessed_shuttles: pd.DataFrame):

    data_frame = (
        preprocessed_shuttles.groupby(["shuttle_type"])
        .mean(numeric_only=True)
        .reset_index()
    )
    fig = go.Figure(
        [
            go.Bar(
                x=data_frame["shuttle_type"],
                y=data_frame["passenger_capacity"],
            )
        ]
    )

    return fig


def create_confusion_matrix(companies: pd.DataFrame):
    actuals = [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1]
    predicted = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1]
    data = {"y_Actual": actuals, "y_Predicted": predicted}
    df = pd.DataFrame(data, columns=["y_Actual", "y_Predicted"])
    confusion_matrix = pd.crosstab(
        df["y_Actual"], df["y_Predicted"], rownames=["Actual"], colnames=["Predicted"]
    )
    sn.heatmap(confusion_matrix, annot=True)
    return plt


def create_actual_predicted_plot(X: pd.DataFrame, y: pd.Series, model: LinearRegression):
    # calculate Y Prediction
    y_pred = model.predict(X)
    # Ensure y_test and y_pred are 1D
    y_test = np.ravel(y)
    y_pred = np.ravel(y_pred)
    
    # Scatter plot of actual vs. predicted values
    plt.scatter(y_test, y_pred, s=5)
    
    # Labels and title
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title(f'Actual vs Predicted Ticket Price')
    
    # Fit a line to the data (best-fit line)
    fit = np.polyfit(y_test, y_pred, 1)  # Linear fit (degree = 1)
    fit_line = np.poly1d(fit)
    
    # Generate x values for plotting the best-fit line
    x_vals = np.linspace(min(y_test), max(y_test), 100)
    plt.plot(x_vals, fit_line(x_vals), color='red', linestyle='--', label='Best Fit Line')
    
    # Add legend
    plt.legend()
    
    return plt
