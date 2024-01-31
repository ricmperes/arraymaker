from arraymaker.callbacks.sipm_callbacks import get_sipmcallbacks
from arraymaker.callbacks.pmt_callbacks import get_pmtcallbacks

def get_all_callbacks(app):
    """Function to merge all callbacks from the different pages.
    """
    
    get_sipmcallbacks(app)
    get_pmtcallbacks(app)