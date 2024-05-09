from process_datasets import process_datasets
from mix_datasets import mix_datasets
from augment_datasets import augment_datasets


if __name__ == '__main__':
    print(
        '### Welcome to oso-hormiguero\'s dataset processor ###'
    )
    print('-' * 70)

    # TODO: select the model for which we want to process the datasetsg

    while True:
        print('Please select one of the following options:')
        print('1. Process datasets for YOLO.')
        print('2. Create a mix of datasets.')
        print('3. Augment datasets.')
        print('4. Exit.')
        option = input('Input the number of the selected option: ')
        print('-' * 70)

        # Option 1 - Process a dataset for YOLO.
        if option == '1':
            if (not process_datasets()):
                break

        # Option 2 - Create a mix of datasets.
        elif option == '2':
            if (not mix_datasets()):
                break

        # Option 3 - Augment datasets.
        elif option == '3':
            if (not augment_datasets()):
                break

        # Exit
        else:
            break
