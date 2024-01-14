import plotly.graph_objects as go
import numpy as np
import numpy.ma as ma


def plot_model(mppc, xy=(0, 0)):
    """Make a plot of the SiPM unit model using Plotly

    Args:
        xy (tuple, optional): coordinates of the bottom left corner.
            Defaults to (0,0).
        figax (plotly.graph_objects.Figure or None, optional): 
            Plotly figure environment. Defaults to None.

    Returns:
        plotly.graph_objects.Figure or None: updated figure environment
    """

    fig = go.Figure()


    # Packaging area rectangle
    fig.add_shape(
        type='rect',
        x0=xy[0] + mppc.width_tolerance,
        y0=xy[1] + mppc.height_tolerance,
        x1=xy[0] + mppc.width_tolerance + mppc.width_package,
        y1=xy[1] + mppc.height_tolerance + mppc.height_package,
        fillcolor='grey',
        opacity=0.3,
        line=dict(color='black'),
        layer='below',
        name='Packaging area'
    )

    # Active area rectangle
    fig.add_shape(
        type='rect',
        x0=xy[0] + mppc.D_corner_x_active,
        y0=xy[1] + mppc.D_corner_y_active,
        x1=xy[0] + mppc.D_corner_x_active + mppc.width_active,
        y1=xy[1] + mppc.D_corner_y_active + mppc.height_active,
        fillcolor='black',
        opacity=0.8,
        line=dict(color='black'),
        layer='above',
        name='Active area'
    )

    geometric_centre = mppc.get_unit_centre()
    active_centre = mppc.get_unit_active_centre()

    # Geometric centre point
    fig.add_trace(
        go.Scatter(
            x=[geometric_centre[0]],
            y=[geometric_centre[1]],
            mode='markers',
            marker=dict(color='green'),
            name='Geometric centre'
        )
    )

    # Active centre point
    fig.add_trace(
        go.Scatter(
            x=[active_centre[0]],
            y=[active_centre[1]],
            mode='markers',
            marker=dict(color='red', symbol='x'),
            name='Active centre'
        )
    )

    # Layout settings
    fig.update_layout(
        width=500,
        height=500,
        autosize=False,
        xaxis_range=[xy[0] - 0.1 * mppc.width_unit, xy[0] + 1.1 * mppc.width_unit],
        yaxis_range=[xy[1] - 0.1 * mppc.height_unit, xy[1] + 1.1 * mppc.height_unit],
        xaxis=dict(title='x [mm]', scaleanchor="y", scaleratio=1),
        yaxis=dict(title='y [mm]'),
        legend=dict(x=1.02, y=1),
        showlegend=True,
        hovermode='closest',
        template='simple_white'
    )

    fig.show()
    return fig


def plot_sipm_array(array, fig = None):
    """Plot the array of SiPMs using Plotly.

    Args:
        figax (plotly.graph_objects.Figure or None, optional): 
            Plotly figure environment. Defaults to None.

    Returns:
        plotly.graph_objects.Figure or None: updated figure environment
    """

    if fig is None:
        fig = go.Figure()
    
    
    n_corner_x, n_corner_y = np.shape(array.D_corners_xx)

    xs_packaging = []
    ys_packaging = []
    xs_active = []
    ys_active = []

    for _x_i in range(n_corner_x):
        for _y_i in range(n_corner_y):
            _x0 = array.D_corners_xx[_x_i, _y_i]
            _y0 = array.D_corners_yy[_x_i, _y_i]
            
            space_has_not_sipm = (ma.is_masked(_x0) and ma.is_masked(_y0))

            if space_has_not_sipm:
                continue
            else:
                             
                x0=_x0 + array.sipmunit.width_tolerance
                y0=_y0 + array.sipmunit.height_tolerance
                x1=_x0 + array.sipmunit.width_tolerance + array.sipmunit.width_package
                y1=_y0 + array.sipmunit.height_tolerance + array.sipmunit.height_package
            
                xs_packaging += [x0, x0, x1, x1, None]
                ys_packaging += [y0, y1, y1, y0, None]

                x0=_x0 + array.sipmunit.D_corner_x_active
                y0=_y0 + array.sipmunit.D_corner_y_active
                x1=_x0 + array.sipmunit.D_corner_x_active + array.sipmunit.width_active
                y1=_y0 + array.sipmunit.D_corner_y_active + array.sipmunit.height_active
                
                xs_active += [x0, x0, x1, x1, None]
                ys_active += [y0, y1, y1, y0, None]

    fig.add_trace(go.Scatter(x=xs_packaging,
                             y=ys_packaging,
                             fill="toself",
                             fillcolor='gray',
                             opacity=0.3,
                             line=dict(color='black' ),
                             name='Packaging area'
                             )
                             )
    fig.add_trace(go.Scatter(x=xs_active,
                             y=ys_active,
                             fill="toself",
                             fillcolor='black',
                             opacity=0.7,
                             line=dict(color='black' ),
                             name='Active area'
                             )
                             )

    # Array diameter circle
    fig.add_shape(
        type='circle',
        x0=-array.array_diameter / 2,
        y0=-array.array_diameter / 2,
        x1=array.array_diameter / 2,
        y1=array.array_diameter / 2,
        fillcolor='rgba(0,0,0,0)',
        opacity=1.,
        line=dict(color='DarkRed',width=4,),
        name='Array diameter',
        layer='above'
    )

    # Layout settings
    fig.update_layout(
        
        xaxis_range=[-array.array_diameter * 1.2 / 2, array.array_diameter * 1.2 / 2],
        yaxis_range=[-array.array_diameter * 1.2 / 2, array.array_diameter * 1.2 / 2],
        xaxis=dict(title='x [mm]', scaleanchor="y", scaleratio=1),
        yaxis=dict(title='y [mm]'),
        showlegend=False,
        #legend=dict(x=0.05, y=0.95),
        hovermode='closest',
        width=600,
        height=500,
        template='simple_white',
        margin=dict(l=0, r=0, t=0, b=0)
    )

    if fig is None:
        fig.show()
    
    return fig


def add_widgets(fig):
    """Add widgets to the plotly figure.

    Returns:
        plotly.graph_objects.FigureWidget: updated figure environment
    """
    # Add dropdown
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        args=["model", "tile"],
                        label="UZH tile",
                        method="restyle"
                    ),
                    dict(
                        args=["model", "quad"],
                        label="Quad (12x12 mm2) ",
                        method="restyle"
                    ),
                    dict(
                        args=["model", "sbs"],
                        label="6x6 mm2",
                        method="restyle"
                    ),
                    dict(
                        args=["model", "tbt"],
                        label="3x3 mm2",
                        method="restyle"
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.25,
                xanchor="left",
                y=1,
                yanchor="middle"
            ),
        ]
    )
    # Add annotation
    fig.update_layout(
        annotations=[
            dict(text="SiPM model:", showarrow=False,
            x=0, y=1,yref = 'paper', align="left")
        ]
    )
    
    return fig