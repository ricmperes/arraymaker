import dash
import dash_bootstrap_components as dbc

from sipmarray_interactive.callbacks.merge_callbacks import get_all_callbacks

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.FLATLY, dbc.icons.BOOTSTRAP]

# Define the layout of the Dash app
app = dash.Dash(__name__,
                prevent_initial_callbacks="initial_duplicate",
                external_stylesheets=external_stylesheets,
                routes_pathname_prefix='/arraymaker/',
                use_pages=True)
app.title = 'SiPM array display'
# app.layout = get_layout()

get_all_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=2024)
