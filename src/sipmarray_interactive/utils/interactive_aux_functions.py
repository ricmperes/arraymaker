import os

from sipmarray.array import SiPMarray

def build_updated_array(new_model, new_diameter, new_margin):
    array = SiPMarray(array_diameter= new_diameter, 
                      border_margin=-1*new_margin, 
                      sipm_model=new_model)
    return array

def get_active_corners_csv(new_model, new_diameter, new_margin):
    array = build_updated_array(new_model, new_diameter, new_margin)
    array.export_corners_active(file_name='corners_active.csv')
    with open('corners_active.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_active.csv')
    return download_content

def get_package_corners_csv(new_model, new_diameter, new_margin):
    array = build_updated_array(new_model, new_diameter, new_margin)
    array.export_corners_package(file_name='corners_package.csv')
    with open('corners_package.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_package.csv')
    return download_content

def get_centers_csv(new_model, new_diameter, new_margin):
    array = build_updated_array(new_model, new_diameter, new_margin)
    array.export_centres(file_name='centres.csv')
    with open('centres.csv', 'r') as f:
        download_content= f.read()
    os.remove('centres.csv')
    return download_content

def get_properties_to_print(array):
    n_sipms = array.n_sipms
    active_area = array.total_sipm_active_area
    coverage = array.sipm_coverage
    string = f'Number of sensors: {n_sipms}\nActive area: {active_area:.2f} mm2\nCoverage: {coverage:.2f} %'
    return string