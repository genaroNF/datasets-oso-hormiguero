from generators.mix_datasets import mix_datasets as mix_all
from generators.mix_datasets_reduced_slope import mix_datasets_reduced_slope
from generators.mix_datasets_custom import mix_datasets_selected


def mix_datasets():
    print('Please select one of the following options:')
    print('1. Mix all the datasets.')
    print('2. Mix the datasets with less slope.')
    print('3. Custom mix.')
    print('4. Exit.')
    option = input('Input the number of the selected option: ')

    # Mix of all the datasets
    if option == '1':
        print('-' * 70)
        mix_all()
        print('-' * 70)
    # Mix all the datasets with less slope
    elif option == '2':
        print('-' * 70)
        mix_datasets_reduced_slope()
        print('-' * 70)
    # Custom mix
    elif option == '3':
        print('-' * 70)
        mix_datasets_selected()
        print('-' * 70)
    # Exit
    else:
        return False

    return True
