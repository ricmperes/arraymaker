import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from pmtarray import PMTarray

from arraymaker.utils.plotly_functions import (plot_circular_pmt_array,
                                               plot_square_pmt_array)
from arraymaker.utils.pmt_aux_functions import *


def get_customcallbacks(app):
    # Define callback to update the plot based on dropdown selection
    @app.callback(
        Output('custom-array-plot-custom', 'figure'),
        Output('text-result-custom', 'value'),
        Output('export-text-custom', 'value', allow_duplicate=True),
        [Input('dropdown-selection-custom', 'value'),
         Input('diameter-input-custom', 'value'),
         Input('margin-input-custom', 'value'),
         Input('intra-distance-input-custom', 'value'),
         Input('input-custom-width-package', 'value'),
         Input('input-custom-height-package', 'value'),
         Input('input-custom-width-tolerance', 'value'),
         Input('input-custom-height-tolerance', 'value'),
         Input('input-custom-width-active', 'value'),
         Input('input-custom-height-active', 'value'),
         Input('input-custom-D-corner-x-active', 'value'),
         Input('input-custom-D-corner-y-active', 'value'),
         Input('input-custom-packaging-diameter-sensor', 'value'),
         Input('input-custom-active-diameter-sensor', 'value'),
         Input('input-custom-diameter-tolerance-sensor', 'value'),
         Input('input-custom-active-area-correction', 'value'),]
    )
    def update_plot(type, array_diameter, margin, intra_distance,
                    width_package, height_package, width_tolerance,
                    height_tolerance, width_active, height_active,
                    D_corner_x_active, D_corner_y_active,
                    packaging_diameter_sensor, active_diameter_sensor,
                    diameter_tolerance_sensor, active_area_correction):
        
        if type == 'round': type = 'circular'
        elif type == 'rectangular': type = 'square'

        custom_params = {'type': type,
                         'name': 'The BEST sensor',
                         'diameter_packaging': packaging_diameter_sensor,
                         'active_diameter': active_diameter_sensor,
                         'diameter_tolerance': diameter_tolerance_sensor,
                         'qe': 0.24,
                         'active_area_correction': active_area_correction,
                         'width_package' : width_package,
                         'height_package' : height_package,
                         'width_tolerance' : width_tolerance,
                         'height_tolerance' : height_tolerance,
                         'width_active' : width_active,
                         'height_active' : height_active,
                         'D_corner_x_active' : D_corner_x_active,
                         'D_corner_y_active' : D_corner_y_active,
                         }

        # Update pmtarray based on the selected option
        updated_array = PMTarray(array_diameter=array_diameter,
                                 border_margin=-1*margin,
                                 pmt_model='custom',
                                 intra_pmt_distance=intra_distance,
                                 custom_unit_params=custom_params)
        
        properties_text = get_pmt_properties_to_print(updated_array)
        too_many = ''
        if updated_array.n_pmts > 10000:
            updated_array = PMTarray(array_diameter=array_diameter,
                                 border_margin=-1*margin,
                                 pmt_model=type,
                                 intra_pmt_distance=intra_distance,
                                 custom_unit_params=custom_params)
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

    # Disable/enable square/round-related inputs for circular sensors
    @app.callback(
        Output('div-custom-width-package', 'hidden'),
        Output('div-custom-height-package', 'hidden'),
        Output('div-custom-width-tolerance', 'hidden'),
        Output('div-custom-height-tolerance', 'hidden'),
        Output('div-custom-width-active', 'hidden'),
        Output('div-custom-height-active', 'hidden'),
        Output('div-custom-D-corner-x-active', 'hidden'),
        Output('div-custom-D-corner-y-active', 'hidden'),
        Output('div-custom-packaging-diameter-sensor', 'hidden'),
        Output('div-custom-active-diameter-sensor', 'hidden'),
        Output('div-custom-diameter-tolerance-sensor', 'hidden'),

        [Input('dropdown-selection-custom', 'value')]
    )
    def shape_buttons(shape):
        # TODO make array and check if circular
        if shape == 'round':
            return [True]*8 + [False]*3
        elif shape == 'rectangular':
            return [False]*8 + [True]*3
        else:
            raise PreventUpdate

    @app.callback(
        Output('export-text-custom', 'value', allow_duplicate=True),
        [Input("download-btn-active-corners-custom", "n_clicks"),
         Input("download-btn-packaging-corners-custom", "n_clicks"),
         Input("download-btn-centers-custom", "n_clicks"),
         Input('dropdown-selection-custom', 'value'),
         Input('diameter-input-custom', 'value'),
         Input('margin-input-custom', 'value'),
         Input('intra-distance-input-custom', 'value'),
         Input('input-custom-width-package', 'value'),
         Input('input-custom-height-package', 'value'),
         Input('input-custom-width-tolerance', 'value'),
         Input('input-custom-height-tolerance', 'value'),
         Input('input-custom-width-active', 'value'),
         Input('input-custom-height-active', 'value'),
         Input('input-custom-D-corner-x-active', 'value'),
         Input('input-custom-D-corner-y-active', 'value'),
         Input('input-custom-packaging-diameter-sensor', 'value'),
         Input('input-custom-active-diameter-sensor', 'value'),
         Input('input-custom-diameter-tolerance-sensor', 'value'),
         Input('input-custom-active-area-correction', 'value')]
    )
    def export_text(n_clicks_active, n_clicks_package, n_clicks_centers,
                    type, array_diameter, margin, intra_distance,
                    width_package, height_package, width_tolerance,
                    height_tolerance, width_active, height_active,
                    D_corner_x_active, D_corner_y_active,
                    packaging_diameter_sensor, active_diameter_sensor,
                    diameter_tolerance_sensor, active_area_correction
                    ):
        
        if n_clicks_active is None and n_clicks_package is None and n_clicks_centers is None:
            raise PreventUpdate
        else:

            if type == 'round': type = 'circular'
            elif type == 'rectangular': type = 'square'

            custom_params = {'type': type,
                            'name': 'The BEST sensor',
                            'diameter_packaging': packaging_diameter_sensor,
                            'active_diameter': active_diameter_sensor,
                            'diameter_tolerance': diameter_tolerance_sensor,
                            'qe': 0.24,
                            'active_area_correction': active_area_correction,
                            'width_package' : width_package,
                            'height_package' : height_package,
                            'width_tolerance' : width_tolerance,
                            'height_tolerance' : height_tolerance,
                            'width_active' : width_active,
                            'height_active' : height_active,
                            'D_corner_x_active' : D_corner_x_active,
                            'D_corner_y_active' : D_corner_y_active,
                            }
        
            ctx = dash.callback_context
            triggered_button_id = ctx.triggered_id

            if triggered_button_id == 'download-btn-active-corners-custom':
                return get_active_pmt_corners_csv(
                    new_model = 'custom', 
                    new_diameter = array_diameter, 
                    new_margin = margin,
                    new_intra_pmt_distance = intra_distance, 
                    new_custom_params = custom_params)

            elif triggered_button_id == 'download-btn-packaging-corners-custom':
                return get_package_pmt_corners_csv(
                    new_model = 'custom', 
                    new_diameter = array_diameter, 
                    new_margin = margin,
                    new_intra_pmt_distance = intra_distance, 
                    new_custom_params = custom_params)

            elif triggered_button_id == 'download-btn-centers-custom':
                return get_pmt_centers_csv(
                    new_model = 'custom', 
                    new_diameter = array_diameter, 
                    new_margin = margin,
                    new_intra_pmt_distance = intra_distance, 
                    new_custom_params = custom_params)

            else:
                raise PreventUpdate

    @app.callback(
        Output('coverage-warning-icon-custom', 'style'),
        [Input('margin-input-custom', 'value')]
    )
    def trigger_coverage_warning(margin_value):
        if margin_value <= 0:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'none'}
        else:
            return {'color': 'red', 'margin-top': '0.5rem',
                    'margin-left': '1rem', 'display': 'inline'}

    # Disable corner buttons for circular PMTs
    @app.callback(
        Output('download-btn-active-corners-custom', 'disabled'),
        Output('download-btn-packaging-corners-custom', 'disabled'),
        [Input('dropdown-selection-custom', 'value')]
    )
    def disable_corner_buttons(new_model):
        # TODO make array and check if circular
        if new_model == 'round':
            return True, True
        elif new_model == 'rectangular':
            return False, False