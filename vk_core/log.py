import datetime


def log(module, event):
    time_label = f'[{datetime.datetime.today().replace(microsecond=0)}]'
    print(f'[{module}]{time_label}: {event}')
