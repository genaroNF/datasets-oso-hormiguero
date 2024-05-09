import shutil

from generators.augment_datasets import augment_datasets as augment_sets
from generators.mix_datasets import mix_datasets as mix_all
from generators.mix_datasets_reduced_slope import mix_datasets_reduced_slope
from generators.mix_datasets_custom import mix_datasets_selected
from consts import MIX_PATH


def augment_datasets():
    print('Please select one of the following options:')
    print('1. Augment mixed datasets.')
    print('2. Augment all datasets.')
    print('3. Augment the datasets with less slope.')
    print('4. Custom augmentation.')
    print('5. Exit.')
    option = input('Input the number of the selected option: ')

    # Augment mixed the datasets
    if option == '1':
        print('-' * 70)
        augment_sets()
        print('-' * 70)
    # Augment all the datasets
    if option == '2':
        print('-' * 70)
        shutil.rmtree(MIX_PATH)
        mix_all()
        augment_sets()
        print('-' * 70)
    # Augment the datasets with less slope
    elif option == '3':
        print('-' * 70)
        shutil.rmtree(MIX_PATH)
        mix_datasets_reduced_slope()
        augment_sets()
        print('-' * 70)
    # Custom augmentation
    elif option == '4':
        print('-' * 70)
        shutil.rmtree(MIX_PATH)
        mix_datasets_selected()
        augment_sets()
        print('-' * 70)
    # Exit
    else:
        return False

    print('Data augmented successfully.')
    print('-' * 70)
    print('-' * 70)

    return True
