from extensions import supabase

def fetch_data(table_name, query_params=None):
    """
    Lấy dữ liệu từ Supabase
    
    Args:
        table_name (str): Tên bảng
        query_params (dict, optional): Các tham số truy vấn. Defaults to None.
        
    Returns:
        dict: Dữ liệu từ Supabase
    """
    query = supabase.table(table_name).select("*")
    
    if query_params:
        if 'filter' in query_params:
            for filter_item in query_params['filter']:
                column, operator, value = filter_item
                query = query.filter(column, operator, value)
                
        if 'order' in query_params:
            column, direction = query_params['order']
            query = query.order(column, desc=(direction.lower() == 'desc'))
            
        if 'limit' in query_params:
            query = query.limit(query_params['limit'])
            
        if 'offset' in query_params:
            query = query.offset(query_params['offset'])
    
    response = query.execute()
    return response.data

def insert_data(table_name, data):
    """
    Thêm dữ liệu vào Supabase
    
    Args:
        table_name (str): Tên bảng
        data (dict): Dữ liệu cần thêm
        
    Returns:
        dict: Dữ liệu đã thêm
    """
    response = supabase.table(table_name).insert(data).execute()
    return response.data

def update_data(table_name, id_column, id_value, data):
    """
    Cập nhật dữ liệu trong Supabase
    
    Args:
        table_name (str): Tên bảng
        id_column (str): Tên cột ID
        id_value: Giá trị ID
        data (dict): Dữ liệu cần cập nhật
        
    Returns:
        dict: Dữ liệu đã cập nhật
    """
    response = supabase.table(table_name).update(data).eq(id_column, id_value).execute()
    return response.data

def delete_data(table_name, id_column, id_value):
    """
    Xóa dữ liệu từ Supabase
    
    Args:
        table_name (str): Tên bảng
        id_column (str): Tên cột ID
        id_value: Giá trị ID
        
    Returns:
        dict: Kết quả xóa
    """
    response = supabase.table(table_name).delete().eq(id_column, id_value).execute()
    return response.data