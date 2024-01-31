import os

from pmtarray.array import PMTarray

def build_updated_pmt_array(new_model, new_diameter, new_margin, 
                            new_intra_pmt_distance):
    array = PMTarray(array_diameter = new_diameter, 
                      border_margin = -1*new_margin, 
                      pmt_model = new_model,
                      intra_pmt_distance = new_intra_pmt_distance)
    return array

def get_active_pmt_corners_csv(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance):
    array = build_updated_pmt_array(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance)
    if array.pmtunit.type == 'circular':
        return ''
    
    array.export_corners_active(file_name='corners_active.csv')
    with open('corners_active.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_active.csv')
    return download_content

def get_package_pmt_corners_csv(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance):
    array = build_updated_pmt_array(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance)
    if array.pmtunit.type == 'circular':
        return ''
    array.export_corners_package(file_name='corners_package.csv')
    with open('corners_package.csv', 'r') as f:
        download_content= f.read()
    os.remove('corners_package.csv')
    return download_content

def get_pmt_centers_csv(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance):
    array = build_updated_pmt_array(new_model, new_diameter, new_margin,
                               new_intra_pmt_distance)
    array.export_centres(file_name='centres.csv')
    with open('centres.csv', 'r') as f:
        download_content= f.read()
    os.remove('centres.csv')
    return download_content

def get_pmt_properties_to_print(array):
    n_pmts = array.n_pmts
    active_area = array.total_pmt_active_area
    coverage = array.pmt_coverage
    string = f"""Number of sensors modules: {n_pmts}
Active area: {active_area:.2f} mm2
Active area total coverage: {coverage*100:.2f} %
QE of sensor: {array.pmtunit.qe*100:.0f} %"""
    return string