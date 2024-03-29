import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from sipmarray import SiPMarray
from sipmarray_interactive.utils.plotly_functions import plot_sipm_array
from sipmarray_interactive.utils.interactive_aux_functions import *


# Initial SiPMarray
initial_model = 'tile'
initial_diameter = 160
initial_margin = 10
array = build_updated_array(initial_model, initial_diameter, initial_margin)

# Initial text
n_sipms = array.n_sipms
active_area = array.total_sipm_active_area
coverage = array.sipm_coverage
text_result_string = f'Number of sensors: {n_sipms}\nActive area: {active_area:.2f} mm2\nCoverage: {coverage:.2f} %'

text_active_corners = ''


def get_callbacks(app):
    # Define callback to update the plot based on dropdown selection
    @app.callback(
        Output('sipm-array-plot', 'figure'),
        Output('text-result', 'value'),
        Output('export-text', 'value',allow_duplicate=True),
        [Input('dropdown-selection', 'value'),
        Input('diameter-input', 'value'),
        Input('margin-input', 'value')]
    )
    def update_plot(new_model, new_diameter, new_margin):

        # Update SiPMarray based on the selected option
        updated_array = SiPMarray(array_diameter= new_diameter, 
                                border_margin=-1*new_margin, 
                                sipm_model=new_model)
        properties_text = get_properties_to_print(updated_array)
        too_many = ''
        if updated_array.n_sipms > 10000:
            updated_array = SiPMarray(array_diameter= initial_diameter,
                    border_margin= -1*initial_margin, 
                    sipm_model=initial_model)
            too_many = '\nToo many SiPMs! Display not updated.'
        elif updated_array.n_sipms > 100000:
            too_many = '\nToo many SiPMs! Display not updated.'
            raise('Waaay too many SiPMs!')
        # Plot the updated SiPMarray
        fig = go.Figure()
        fig = plot_sipm_array(updated_array, fig)

        return fig, properties_text + too_many, ''

    @app.callback(
        Output('export-text', 'value',allow_duplicate=True),

        [Input("download-btn-active-corners", "n_clicks"),
        Input("download-btn-packaging-corners", "n_clicks"),
        Input("download-btn-centers", "n_clicks"),
        Input('dropdown-selection', 'value'),
        Input('diameter-input', 'value'),
        Input('margin-input', 'value')]
    )
    def export_text(n_clicks_active, n_clicks_package, n_clicks_centers, 
                    new_model, new_diameter, new_margin):
        if n_clicks_active is None and n_clicks_package is None and n_clicks_centers is None:
            raise PreventUpdate
        
        else:
            ctx = dash.callback_context
            triggered_button_id = ctx.triggered_id
            
            if triggered_button_id == 'download-btn-active-corners':
                return get_active_corners_csv(new_model, new_diameter, new_margin)
            
            elif triggered_button_id == 'download-btn-packaging-corners':
                return get_package_corners_csv(new_model, new_diameter, new_margin)
            
            elif triggered_button_id == 'download-btn-centers':
                return get_centers_csv(new_model, new_diameter, new_margin)
            
            else:
                raise PreventUpdate
        
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
