

def get_first_value(q_set):
    try:
        return q_set[0]
    except IndexError:
        return None