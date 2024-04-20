
from generators.mix_datasets import mix_datasets
from generators.mix_datasets_custom import mix_datasets_selected

DEFAULT_SLOPE = '2'


def mix_datasets_reduced_slope():
    slope = int(input(
        'Specify the desired the amount of frames to be discated (default 2): '
    ) or DEFAULT_SLOPE)
    slope += 1
    print('-' * 70)

    print('Please select one of the following options:')
    print('1. Mix all datasets.')
    print('2. Select datasets.')
    print('3. Exit.')
    option = input('Input the number of the selected option: ')
    print('-' * 70)

    if option == '1':
        mix_datasets(slope=slope)
    if option == '2':
        mix_datasets_selected(slope=slope)

    return False
