def format_name(name: str):
    if ' ' not in name:
        return name
    split = name.index(' ')
    return f'{name[split+1:]}, {name[:split]}'