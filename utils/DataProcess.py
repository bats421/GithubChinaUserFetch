def get_data(data, *params):
    if isinstance(data, dict):
        result = data
        for p in params:
            try:
                result = result[p]
            except:
                return None
        return result
    return None