from processors.ANTS.yolo import process_ANTS
from processors.roboflow.yolo import process_roboflow
from generators.mix_roboflow_ANTS import generate_roboflow_ANTS_mix
from generators.mix_roboflow_ANTS_reduced_slope import generate_roboflow_ANTS_mix_reduced_slope
if __name__ == "__main__":
    print("---Hello and welcome to oso-hormiguero's dataset processor and mix generator---")
    print("-------------------------------------------------------------------------------")
    while True:
        print("Please select one of the options:")
        option_1 = input("""1. Process a dataset for YOLO
2. Create one of the mixes
option: """     )
        if option_1 == "1":
            option_2 = input("""1. Process 'Cao, xiaoyan (2021), ANTS--ant detection and tracking'
2. Process 'Djay de Gier, Ant object detection Dataset'
option: """)
            print("------------------------------------------------")
            if option_2 == "1":
                process_ANTS("./results/datasets")
            else:
                process_roboflow("./results/datasets")
        else:
            option_2 = input("""1. Mix for train40
2. Mix for train40 with less slope
option: """)
            if option_2 == "1":
                print("------------------------------------------------")
                generate_roboflow_ANTS_mix()
                print("------------------------------------------------")
            else:
                print("------------------------------------------------")
                generate_roboflow_ANTS_mix_reduced_slope()
                print("------------------------------------------------")
                
    