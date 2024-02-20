import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from pmtarray import PMTarray

from arraymaker.utils.plotly_functions import (plot_circular_pmt_array,
                                               plot_square_pmt_array)
from arraymaker.utils.pmt_aux_functions import *

# Initial PMTarray
initial_model = '3in'
initial_diameter = 300
initial_margin = 0
initial_intra_pmt_distance = 10
array = build_updated_pmt_array(initial_model, initial_diameter,
                                initial_margin, initial_intra_pmt_distance)

# Initial text
n_pmts = array.n_pmts
active_area = array.total_pmt_active_area
coverage = array.pmt_coverage
text_result_string = (f'Number of sensors: {n_pmts}\n'
                      f'Active area: {active_area:.2f} mm2\n'
                      f'Coverage: {coverage:.2f} %')

text_active_corners = ''


def get_pmtcallbacks(app):
    # Define callback to update the plot based on dropdown selection
    @app.callback(
        Output('pmt-array-plot-pmt', 'figure'),
        Output('text-result-pmt', 'value'),
        Output('export-text-pmt', 'value', allow_duplicate=True),
        [Input('dropdown-selection-pmt', 'value'),
         Input('diameter-input-pmt', 'value'),
         Input('margin-input-pmt', 'value'),
         Input('intra-distance-input-pmt', 'value')]
    )
    def update_plot(new_model, new_diameter, new_margin, new_intra_pmt_distance):

        # Update pmtarray based on the selected option
        updated_array = PMTarray(array_diameter=new_diameter,
                                 border_margin=-1*new_margin,
                                 pmt_model=new_model,
                                 intra_pmt_distance=new_intra_pmt_distance)
        properties_text = get_pmt_properties_to_print(updated_array)
        too_many = ''
        if updated_array.n_pmts > 10000:
            updated_array = PMTarray(array_diameter=initial_diameter,
                                     border_margin=-1*initial_margin,
                                     pmt_model=initial_model)
            too_many = '\nToo many PMTs! Display not updated.'
        elif updated_array.n_pmts > 100000:
            too_many = '\nToo many PMTs! Display not updated.'
            # raise('Waaay too many PMTs!')
        # Plot the updated PMTarray
        fig = go.Figure()
        if updated_array.pmtunit.type == 'square':
            fig = plot_square_pmt_array(updated_array, fig)
        elif updated_array.pmtunit.type == 'circular':
            fig = plot_circular_pmt_array(updated_array, fig)

        return fig, properties_text + too_many, ''

    # Disable corner buttons for circular PMTs
    @app.callback(
        Output('download-btn-active-corners-pmt', 'disabled'),
        Output('download-btn-packaging-corners-pmt', 'disabled'),
        [Input('dropdown-selection-pmt', 'value')]
    )
    def disable_corner_buttons(new_model):
        # TODO make array and check if circular
        if new_model == '3in':
            return True, True
        elif new_model == '2in':
            return False, False

    @app.callback(
        Output('export-text-pmt', 'value', allow_duplicate=True),
        [Input("download-btn-active-corners-pmt", "n_clicks"),
         Input("download-btn-packaging-corners-pmt", "n_clicks"),
         Input("download-btn-centers-pmt", "n_clicks"),
         Input('dropdown-selection-pmt', 'value'),
         Input('diameter-input-pmt', 'value'),
         Input('margin-input-pmt', 'value'),
         Input('intra-distance-input-pmt', 'value')]
    )
    def export_text(n_clicks_active, n_clicks_package, n_clicks_centers,
                    new_model, new_diameter, new_margin, new_intra_pmt_distance):
        if n_clicks_active is None and n_clicks_package is None and n_clicks_centers is None:
            raise PreventUpdate
        else:
            ctx = dash.callback_context
            triggered_button_id = ctx.triggered_id

            if triggered_button_id == 'download-btn-active-corners-pmt':
                return get_active_pmt_corners_csv(new_model, new_diameter,
                                                  new_margin, new_intra_pmt_distance)

            elif triggered_button_id == 'download-btn-packaging-corners-pmt':
                return get_package_pmt_corners_csv(new_model, new_diameter,
                                                   new_margin, new_intra_pmt_distance)

            elif triggered_button_id == 'download-btn-centers-pmt':
                return get_pmt_centers_csv(new_model, new_diameter,
                                           new_margin, new_intra_pmt_distance)

            else:
                raise PreventUpdate

    @app.callback(
        Output('coverage-warning-icon-pmt', 'style'),
        [Input('margin-input-pmt', 'value')]
    )
    def trigger_coverage_warning(margin_value):
        if margin_value <= 0:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'none'}
        else:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'inline'}
