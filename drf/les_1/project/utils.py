def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = int((duration % 3600) % 60)
    return f'{hours} ч. {minutes} мин. {seconds} сек.'
