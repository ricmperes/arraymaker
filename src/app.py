import dash
from layout import get_layout
from callbacks import get_callbacks


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Define the layout of the Dash app
app = dash.Dash(__name__, prevent_initial_callbacks="initial_duplicate",
                external_stylesheets=external_stylesheets)

app.layout = get_layout()
get_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server()
