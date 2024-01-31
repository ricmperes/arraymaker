import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from sipmarray import SiPMarray

from arraymaker.utils.plotly_functions import plot_sipm_array
from arraymaker.utils.sipm_aux_functions import *

# Initial SiPMarray
initial_model = 'tile'
initial_diameter = 160
initial_margin = 10
array = build_updated_sipm_array(
    initial_model, initial_diameter, initial_margin)

# Initial text
initial_model = 'tile'
initial_diameter = 300
initial_margin = 10
array = build_updated_sipm_array(
    initial_model, initial_diameter, initial_margin)
text_active_corners = ''


def get_sipmcallbacks(app):
    # Define callback to update the plot based on dropdown selection
    @app.callback(
        Output('sipm-array-plot-sipm', 'figure'),
        Output('text-result-sipm', 'value'),
        Output('export-text-sipm', 'value', allow_duplicate=True),
        [Input('dropdown-selection-sipm', 'value'),
         Input('diameter-input-sipm', 'value'),
         Input('margin-input-sipm', 'value')]
    )
    def update_plot(new_model, new_diameter, new_margin):

        # Update SiPMarray based on the selected option
        updated_array = SiPMarray(array_diameter=new_diameter,
                                  border_margin=-1*new_margin,
                                  sipm_model=new_model)
        properties_text = get_sipm_properties_to_print(updated_array)
        too_many = ''
        if updated_array.n_sipms > 10000:
            updated_array = SiPMarray(array_diameter=initial_diameter,
                                      border_margin=-1*initial_margin,
                                      sipm_model=initial_model)
            too_many = '\nToo many SiPMs! Display not updated.'
        elif updated_array.n_sipms > 100000:
            too_many = '\nToo many SiPMs! Display not updated.'
            # raise('Waaay too many SiPMs!')
        # Plot the updated SiPMarray
        fig = go.Figure()
        fig = plot_sipm_array(updated_array, fig)

        return fig, properties_text + too_many, ''

    @app.callback(
        Output('export-text-sipm', 'value', allow_duplicate=True),

        [Input("download-btn-active-corners-sipm", "n_clicks"),
         Input("download-btn-packaging-corners-sipm", "n_clicks"),
         Input("download-btn-centers-sipm", "n_clicks"),
         Input('dropdown-selection-sipm', 'value'),
         Input('diameter-input-sipm', 'value'),
         Input('margin-input-sipm', 'value')]
    )
    def export_text(n_clicks_active, n_clicks_package, n_clicks_centers,
                    new_model, new_diameter, new_margin):
        if n_clicks_active is None and n_clicks_package is None and n_clicks_centers is None:
            raise PreventUpdate

        else:
            ctx = dash.callback_context
            triggered_button_id = ctx.triggered_id

            if triggered_button_id == 'download-btn-active-corners-sipm':
                return get_active_sipm_corners_csv(new_model, new_diameter, new_margin)

            elif triggered_button_id == 'download-btn-packaging-corners-sipm':
                return get_package_sipm_corners_csv(new_model, new_diameter, new_margin)

            elif triggered_button_id == 'download-btn-centers-sipm':
                return get_sipm_centers_csv(new_model, new_diameter, new_margin)

            else:
                raise PreventUpdate

    @app.callback(
        Output('coverage-warning-icon-sipm', 'style'),
        [Input('margin-input-sipm', 'value')]
    )
    def trigger_coverage_warning(margin_value):
        if margin_value <= 0:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'none'}
        else:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'inline'}

# # To download a csv file
# @app.callback(
#     Output("download-active-corners", "data"),
#     [Input("download-btn-active-corners", "n_clicks"),
#     Input('dropdown-selection', 'value'),
#     Input('diameter-input', 'value'),
#     Input('margin-input', 'value')]
# )
# def download_active_corners(n_clicks,new_model, new_diameter, new_margin):
#     if n_clicks is None:
#         raise PreventUpdate

#     else:
#         updated_array = SiPMarray(array_diameter= new_diameter,
#                                   border_margin=-1*new_margin,
#                                   sipm_model=new_model)

#         updated_array.export_corners_active(file_name='corners_active.csv')
#         with open('corners_active.csv', 'r') as f:
#             download_content= f.read()
#         return dict(content = download_content, filename = 'corners_active.csv')
