import base64
import io
import plotly.graph_objects as go
import numpy as np
import numpy.ma as ma
import pandas as pd
from plotly.subplots import make_subplots

@np.vectorize
def mass_from_slpm(slpm):
    """Calculates the mass flow in from standard volumetric flow rate
    """
    dens_std = 5.8980 #g/L
    return slpm * dens_std /1000 #kg

@np.vectorize
def slpm_from_mass(mass):
    """Calculates the standard volumetric flow rate from mass flow in 
    (mass in grams, flow in slpm)
    """
    dens_std = 5.8980
    return mass / dens_std

def height_cylinder(mass): # in kg
    dens = 2.8609 #g/cm^3
    h = mass*1000/dens/np.pi/(25/2)**2 #cm
    return h

def mass_cylinder(height):
    dens = 2.8609 #g/cm^3
    m = height*dens*np.pi*(25/2)**2 /1000 #kg
    return m

def parse_data(contents, filename):
    """Based on https://stackoverflow.com/questions/60223161/using-dash-
    upload-component-to-upload-csv-file-and-generate-a-graph"""
    
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif "txt" or "tsv" in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+")
    
    except:
        raise AttributeError("Error reading file.")
        
    return df

def check_csv_file(df_csv):
    columns = df_csv.columns

    time_is_good = 'Time' in columns
    flow_is_good = ('FM01' in columns) or ('FC01' in columns)
    if time_is_good and flow_is_good:
        return True
    else:
        return False


def process_dfs_flow(df_fm, df_fc, flow_offset, mass_offset):

    df = pd.merge(df_fm, df_fc, on = 'Time')
    df.rename(columns = {'FM01':'flow_meter', 
                        'FC01':'flow_controler'}, 
            inplace = True)

    df['Time'] = np.int64(df['Time']/1000)
    df['datetime'] = pd.to_datetime(
        df['Time'], unit = 's')+np.timedelta64(2,'h')
    df['minutes_since_start'] = (df['Time']-df['Time'].iloc[0])/60

    df['flow_meter'] = np.where(df['flow_meter']<0.5, 0, df['flow_meter'])
    df['flow_controler'] = np.where(
        df['flow_controler']<0.5, 0, df['flow_controler'])

    # Times FC was ON and FM was OFF (without filling)
    _starts = [np.datetime64('2024-05-08T15:00:00')]
    _ends = [np.datetime64('2024-05-08T16:30:00')]
    for _start, _end in zip (_starts, _ends):
        
        df['flow_controler'] = np.where(
            (df['datetime'] > _start) &
            (df['datetime'] < _end), 0, df['flow_controler'])
        df['flow_meter'] = np.where(
            (df['datetime'] > _start) &
            (df['datetime'] < _end), 0, df['flow_meter'])

    df['flow'] = df['flow_meter'] - df['flow_controler'] - flow_offset
    df['corr_flow'] = np.where(df['flow']<0.5, 0, df['flow'])
    df['corr_flow'] = np.where(df['flow'] is np.nan, 0, df['flow'])
    df['cumsum_flow'] = np.nancumsum(
        df['corr_flow'])*(df['Time'].iloc[1]-df['Time'].iloc[0])/60


    df['recuperated_mass'] = mass_from_slpm(df['cumsum_flow']) + mass_offset

    return df



def make_initial_mass_plot():
    fig = go.Figure()
    word = ['X','e','n','o','s','c','o','p','e']
    for _x, letter in enumerate(word):
        # Add text annotations for each letter
        fig.add_annotation(
            x=_x*0.7,
            y=1,
            text=letter,
            showarrow=False,
            font=dict(size=30)
    )

    # Update layout
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        width=800,
        height=400,
        template='simple_white',
    )
    return fig

def make_mass_plot(df, fig = None):
    if fig is None:
        fig = go.Figure()

    # Create traces
    trace1 = go.Scatter(x=df['datetime'], y=df['recuperated_mass'], 
                        mode='lines', name='Xe mass filled [kg]', 
                        line=dict(color='blue'))
    trace2 = go.Scatter(x=df['datetime'], y=df['corr_flow'], 
                        mode='lines', name='Xe flow [slpm]', 
                        opacity = 0.2,
                        line=dict(color='red'))

    # Create figure with secondary y-axis
    #fig = go.Figure()
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True) 
                        #subplot_titles=("Xe Mass and Flow Over Time"))

    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=1)

    # Add y-axis labels
    fig.update_yaxes(title_text='Xe mass filled [kg]', 
                     secondary_y=False)
    fig.update_yaxes(title_text='Xe flow [slpm]', 
                     secondary_y=True, color='red')

    fig.update_xaxes(showgrid=True, zeroline=True)
    fig.update_yaxes(showgrid=True, zeroline=True)
    # Set x-axis date format
    #fig.update_layout(xaxis=dict(tickformat='%d/%m'))

    # Rotate x-axis labels
    fig.update_layout(xaxis_tickangle=0)

    # Set layout parameters
    fig.update_layout(
        width=800,
        height=400,
        template='simple_white',
    )


    # Show plot
    return fig
