# AutoSolenoid
Solenoid actuator design and analysis done quick. Built on pyFEMM.

![autosol](https://user-images.githubusercontent.com/80536083/227770201-95344fc2-cb73-4073-ad98-998b73f90d95.jpg)

## Requirements
 - The FEMM software (https://www.femm.info/wiki/HomePage)
 - pyfemm
 - matplotlib
 - moviepy (optional)
 
## How to Use

1. To start the graphical interface, **run start-gui.py**. If you don't want the graphical interface **run start-python.py**.
2. **Enter design inputs**.
3. If using the GUI, **click on PERFORM ANALYSIS**. Otherwise, run the python script.
4. **Wait** until FEMM analyses are complete. The console window will tell how many of the analyses are completed.
5. **Navigate to your export directory** (the filename you chose) to see the results and FEMM models.

## Results
![plunger](https://user-images.githubusercontent.com/80536083/227770453-a10d4441-9251-4afa-9a30-83e2690fbb82.gif)

AutoSoleonid auto-exports magnetic flux density plots and a stroke-force graph.

For other results, you can use the generated FEMM models in your export directory to get more data.
