import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pmtarray import PMTunit
from sipmarray import SiPMunit
import dash_bootstrap_components as dbc
from arraymaker.utils.plotly_functions import (plot_circular_pmt_model,
                                               plot_square_model)
from arraymaker.utils.pmt_aux_functions import *


def get_models_callbacks(app):

    @app.callback(
        Output('table-properties-pmt', 'children'),
        Output('plot-pmt-unit', 'figure'),
        [Input('dropdown-selection-pmtsensor', 'value')]
    )
    def update_table_properties_pmt(new_model):
        pmtunit = PMTunit(model=new_model)
        pmt_properties_df = pmtunit.get_properties_df()

        # the table object with from_dataframe needs to be re-created 
        # instead of just updated
        table_properties_pmt = dbc.Table.from_dataframe(df = pmt_properties_df,
                                                 striped=True, bordered=True,
                                                 hover=True, size='md',
                                                 style={'margin-left': '2rem',
                                                        'margin-bottom': '2rem',
                                                        'margin-top': '1rem'})
        fig = go.Figure()
        if pmtunit.type == 'circular':
            fig = plot_circular_pmt_model(pmtunit)
        elif pmtunit.type == 'square':
            fig = plot_square_model(pmtunit)
        else:
            
            raise ('PMT type not recognized!')

        return table_properties_pmt, fig

    @app.callback(
        Output('table-properties-sipm', 'children'),
        Output('plot-sipm-unit', 'figure'),
        [Input('dropdown-selection-simpsensor', 'value')]
    )
    def update_table_properties_pmt(new_model):
        sipmunit = SiPMunit(model=new_model)
        sipm_properties_df = sipmunit.get_properties_df()

        table_properties_sipm = dbc.Table.from_dataframe(df = sipm_properties_df,
                                                 striped=True, bordered=True,
                                                 hover=True, size='md',
                                                 style={'margin-left': '2rem',
                                                        'margin-bottom': '2rem',
                                                        'margin-top': '1rem'})
        fig = go.Figure()
        fig = plot_square_model(sipmunit, fig)

        return table_properties_sipm, fig
