def contains_required_params(params, form):
    for param in params:
        if param not in form:
            return False
    return True
