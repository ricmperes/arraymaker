from arraymaker.callbacks.sipm_callbacks import get_sipmcallbacks
from arraymaker.callbacks.pmt_callbacks import get_pmtcallbacks
from arraymaker.callbacks.models_callbacks import get_models_callbacks
from arraymaker.callbacks.custom_callbacks import get_customcallbacks
from arraymaker.callbacks.xemass_callbacks import get_xemasscallbacks

def get_all_callbacks(app):
    """Function to merge all callbacks from the different pages.
    """

    get_sipmcallbacks(app)
    get_pmtcallbacks(app)
    get_models_callbacks(app)
    get_customcallbacks(app)
    get_xemasscallbacks(app)
    

