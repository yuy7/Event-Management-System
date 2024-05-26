
def count_days_distance(current_date, now):
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return (current_date-now).days