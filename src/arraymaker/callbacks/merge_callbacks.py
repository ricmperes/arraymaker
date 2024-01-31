from arraymaker.callbacks.sipm_callbacks import get_sipmcallbacks
from arraymaker.callbacks.pmt_callbacks import get_pmtcallbacks
from arraymaker.callbacks.models_callbacks import get_models_callbacks


def get_all_callbacks(app):
    """Function to merge all callbacks from the different pages.
    """

    get_sipmcallbacks(app)
    get_pmtcallbacks(app)
    get_models_callbacks(app)
