import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from arraymaker.utils.xemass_functions import *

def get_xemasscallbacks(app):
    @app.callback(
        Output('button-generate-plot', 'disabled'),
        [Input('upload-fm01', 'contents'), 
         Input('upload-fc01', 'contents')]
    )
    def check_files(fm01_content, fc01_content):
        if fm01_content is not None and fc01_content is not None:
            return False  # Show the button if both files are uploaded
        else:
            return True  # Hide the button if any file is missing
        

    # Change button to success once it has a file
    @app.callback(
        Output('button-fm01', 'color'),
        Output('button-fm01', 'children'),
        [Input('upload-fm01', 'contents'), 
         Input('upload-fm01', 'filename')],
    )
    def check_fm01_button(fm01_content, fm01_filename):
        if fm01_content is None:
            return "primary", "FM01"
            
        else:
            df_file = parse_data(fm01_content, fm01_filename)
            file_is_good = check_csv_file(df_file)
            if file_is_good: 
                return 'success', fm01_filename
            else: 
                return"primary", "FM01"
        
    @app.callback(
        Output('button-fc01', 'color'),
        Output('button-fc01', 'children'),
        [Input('upload-fc01', 'contents'), 
         Input('upload-fc01', 'filename')],
    )
    def check_fm01_button(fc01_content, fc01_filename):
        if fc01_content is None:
            return "primary", "FC01"
            
        else:
            df_file = parse_data(fc01_content, fc01_filename)
            file_is_good = check_csv_file(df_file)
            if file_is_good: 
                return 'success', fc01_filename
            else: 
                return"primary", "FM01"
        

    # Callback to generate plot on button click
    @app.callback(
        Output('plot-flow-mass', 'figure'),
        [Input('button-generate-plot', 'n_clicks'),
         Input('upload-fm01', 'contents'), 
         Input('upload-fm01', 'filename'),
         Input('upload-fc01', 'contents'), 
         Input('upload-fc01', 'filename'),
         Input('input-flow-offset', 'value'),
         Input('input-mass-offset','value')],
        suppress_callback_exceptions=True,
        )
    def update_plot(n_clicks, fm01_content, fm01_filename, 
                    fc01_content, fc01_filename, flow_offset,
                    mass_offset):
        if n_clicks is not None and n_clicks > 0:
            
            df_fm = parse_data(fm01_content, fm01_filename)
            df_fc = parse_data(fc01_content, fc01_filename)
            
            df = process_dfs_flow(df_fm, df_fc, 
                                  flow_offset, mass_offset)
            fig = make_mass_plot(df)
            return fig
        else:
            return make_initial_mass_plot()
        
    @app.callback(
        Output('gpm-text', 'children'),
        [Input('slpm-value', 'value')]
    )
    def update_gpm_value(slpm_value):
        gpm = mass_from_slpm(slpm_value)*1000
        ans = f' {gpm:.2f}  gpm'
        return ans
    
    @app.callback(
        Output('slpm-text', 'children'),
        [Input('gpm-value', 'value')]
    )
    def update_gpm_value(slpm_value):
        slpm = slpm_from_mass(slpm_value)
        ans = f' {slpm:.2f}  slpm'
        return ans
