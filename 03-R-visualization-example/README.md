# R IonVision data visualization
This R script provides an example on how to open and visualize json files created by the IonVision DMS in R. Different fields recorded in the result files are explored, and the data is visualized into spectra using the ggplot package. Seven measurement files are included in the IonVision-sample-data -folder, along with annotations for the measurements. The code is provided in a notebook format, with explanations for different sections in between the code chunks.

## Usage
This example is made to be run in RStudio. To run, you need to install packages "jsonlite", "ggplot2", "viridis", and "data.table". Additionally, you need to download the example data from folder "IonVision-sample-data", and change the path in the code to the location of the example data.