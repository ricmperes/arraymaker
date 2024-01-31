import os

from sipmarray.array import SiPMarray

def build_updated_sipm_array(new_model, new_diameter, new_margin):
    array = SiPMarray(array_diameter= new_diameter, 
                      border_margin=-1*new_margin, 
                      sipm_model=new_model)
    return array

def get_active_sipm_corners_csv(new_model, new_diameter, new_margin):
    array = build_updated_sipm_array(new_model, new_diameter, new_margin)
    array.export_corners_active(file_name='corners_active.csv')
    with open('corners_active.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_active.csv')
    return download_content

def get_package_sipm_corners_csv(new_model, new_diameter, new_margin):
    array = build_updated_sipm_array(new_model, new_diameter, new_margin)
    array.export_corners_package(file_name='corners_package.csv')
    with open('corners_package.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_package.csv')
    return download_content

def get_sipm_centers_csv(new_model, new_diameter, new_margin):
    array = build_updated_sipm_array(new_model, new_diameter, new_margin)
    array.export_centres(file_name='centres.csv')
    with open('centres.csv', 'r') as f:
        download_content= f.read()
    os.remove('centres.csv')
    return download_content

def get_sipm_properties_to_print(array):
    n_sipms = array.n_sipms
    active_area = array.total_sipm_active_area
    coverage = array.sipm_coverage
    string = f"""Number of sensors modules: {n_sipms}
Active area: {active_area:.2f} mm2
Active area total coverage: {coverage*100:.2f} %
PDE of sensor: {array.sipmunit.pde*100:.0f} %"""
    return string