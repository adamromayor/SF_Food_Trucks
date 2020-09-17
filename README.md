# SF_Food_Trucks
Run the following commands to install dependencies:
    pip install requests
    pip install pandas
    pip install sodapy


Once these are installed, run the program using the following command
in the terminal:
    python3 -m show_open_food_trucks

Description:
    This program will automatically print the first 10 open food trucks.
    
    > If there are more food trucks open, it will prompt the user to type
    "Y" or "N". 
    > If the user types "Y" or "y" the program will output 10 more
    open food trucks. 
    > If the user types "N" or "n" the program will end. 
    > If the user types any other character, the program will prompt the
    user to type "Y" or "N", until there is a valid input
    > Once all open food trucks are printed the program will print
    "You have viewed all open food trucks... goodbye!" and return