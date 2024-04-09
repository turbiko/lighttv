
def get_date_from_cell_0(cell_data:str)->dict:
    if type(cell_data) == str:
        day_name, date_str = cell_data.split(',')

    return {'day_name':day_name, 'date_str':date_str }