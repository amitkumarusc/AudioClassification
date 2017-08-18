# Audio Songs Genre Classification
[![N|Solid](https://secure.gravatar.com/avatar/7273c58dc017eec83667b50742ff6368?s=80)](https://nodesource.com/products/nsolid)

This is a python program which groups similar songs by performing a statistical similarity between the audio forms of the mp3 songs. It uses R to generate a Voronoi diagram displaying the position of different songs. 

### Dependencies:
1. Install following dependencies via pip: `pip install <module_name>`
	```
	1. numpy
	2. wave
	3. csv
	```
2. Install `mpg123` to convert `.mp3` files to `.wav` files
    ```
    >> brew install mpg123
    ```
3. Install `R`. Follow instructions from `https://cran.r-project.org/bin/macosx/`. Also install `deldir` package by running following command in R prmompt
    ```
    >> install.packages("deldir")
    ```

### Steps to execute program
1. Clone the current project to your local machine:
    ```sh
    $ git clone https://github.com/amitasviper/AudioClassification
    ```
2. Place your `.mp3` songs in the `audio_files` directory.
3. Run the following command to convert `.mp3` songs to `.wav`.
    ```
    >> python mp3ToWav.py
    ```
3. To extract audio feature from the above proceesed songs run the followwing command
    ```
    >> python readAndProcess.py
    ```
4. Step 2 will generate a file named `featureOutput.csv`. This constains all the songs with their features.
5. Now we can use these features to perform a statistical analysis.
6. Finally the `output.png` will look somewhat like the below given image.
![alt text](output.png?raw=true)