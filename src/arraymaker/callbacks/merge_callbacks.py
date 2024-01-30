from arraymaker.callbacks.sipm_callbacks import get_sipmcallbacks

def get_all_callbacks(app):
    """Function to merge all callbacks from the different pages.
    """
    
    get_sipmcallbacks(app)