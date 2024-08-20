## CSCA20 - Final Project: Fantasy Hockey Live Draft Helper
## Pandas Code adapted primarily from Intro to Pandas for Data Analysis: https://app.datawars.io/skill-track/9bfbf033-d732-4273-8abb-431281dd1f25;
## freeCodecCamp.org Video Series: https://www.youtube.com/@freecodecamp
# Additional sources cited within.
## Functions detailed by docstrings - access with help().

## Import pandas library module for Worksheet/Data manipulation.
import pandas as pd # Import pandas into Python; renamed as "pd" (standard for pandas).
pd.set_option('display.max_columns', 14) # Set pandas to display all the columns (otherwise it will truncate with "...").
# Adapted from: How to Show All Columns of a Pandas DataFrame?
# https://www.geeksforgeeks.org/how-to-show-all-columns-of-a-pandas-dataframe/

## Specify File Path: points at the path for the Excel Workbook.
projection_file = "C:\\Users\\Mcowa\\OneDrive\\Documents\\UofT\\Current\\CSCA20 - Introduction to Programming\\Project\\Spreadsheets\\Sheet 1 - Dom's Projections.xlsx"
# Assigns the file path string (characters, numbers, symbols, or whitespace) to the projection_file variable.

## Pandas Data Frame code:
df = pd.DataFrame() # Creates a new Data Frame to store player data; like a customized Spreadsheet (DFs are how panda uses/messes with data - similar situation as in R).
drafted_players = [] # Variable holding empty list to store drafted players; pandas uses "[]" to denote lists.
## df.info: concise summary for testing (like summary/glimpse in R); double-checks that the DF is working.

## Setup Team & Opponents:
teams = { 'myteam': [], 'team2': [], 'team3': [], 'team4': [] } # Sets up a dictionary {} with key-value pairs ("myteam': [] ...) associated with an empty list "[]".
                                                                # Keys are 'myteam', 'team2', 'team3', 'team4'; value associated is the empty list '[]' for each.
                                                                ## Adapted from: Decoding Dictionaries in Python: A Comprehensive Guide to Key-Value Mastery - Rishu Gandhi
                                                                ## https://blog.stackademic.com/decoding-dictionaries-in-python-a-comprehensive-guide-to-key-value-mastery-56d67bf06030
                                                                    
def load_projection_file(): # Defines the function for loading the specified projection file (Sheet 1 - Dom's Projections).
    """
    Loads the fantasy hockey projection data from specified Excel Workbook into a pandas DataFrame (via read_excel). Only selected columns (i.e., Rank, Goals, Assists, Points, Shots, Powerplay Points, Wins, Saves) are considered/displayed.
    
    Note: Remember to check-mark the relevant scoring categories WITHIN Sheet 1 - Dom's Projections.xlsx!
    """   
    global df # Using the "global argument" here to get Python to refer to the original 'df' from Line 16 (defined outside of this function).
              # Otherwise, we'd have only a local variable (df) within the function (if this were the case, the original df would remain unchanged).
    
    try: ## Try-except block for testing and errors (ex. 'FileNotFoundError').
        # Create a new list that keeps only specific columns (names match column headers on 'The List'):
        scoring_category_columns_to_keep = ['RK', 'NAME', 'TEAM', 'G', 'A', 'PTS', 'SOG', 'PPP', 'W', 'SV']  # Add/remove scoring categories as needed (with the projections file).
        df = pd.read_excel(projection_file, sheet_name='The List', usecols=scoring_category_columns_to_keep) # usecols (from pd): specifies which columns (from list "scoring_category_columns_to_keep").
        df = df.round(1) # Rounds ALL numeric values in each column to one decimal place for simplicity (the categories generally have 6+ decimal points) Need to un-round Goalie categories later.
        print("Projections loaded successfully!")
        print(df.head(25))  # Take the df and show the first 25 rows in the DF (same as "head" in R).
    
    except FileNotFoundError:
        print("We couldn't find the Spreadsheet you're looking for: ", projection_file, ". Please try again!") # Print "File not found" (will notice if the file has been moved).
    except Exception as e:
        print("An has error occurred:", e) # "Broad Exception Handler"; prints any other errors not caught by the first except.
                                           ## Adapted from: Python Enhancement Proposals - Catching Exceptions - Collin Winter
                                           ## https://peps.python.org/pep-3110/
                                       
def get_available_players():
    """
    Returns a df of players who are still available to be drafted (as in they are NOT in drafted_players list). Used by view_available_players() and recommend_best_player().
    """
    return df[~df['NAME'].isin(drafted_players)]
    ## df[~df['NAME']: applies a condition that filters the original df to specifically access the 'NAME' column.
    # 1st df: point at original df; 2nd df (with the "[") is how we point at the column.
    # .isin(drafter_players): remember the "~" reversing the TRUE/FALSE...
    # This is a "boolean series": checking if the corresponding player's name is NOT (~) in the drafted_players list (meaning, they've already been selected by the user, so won't be placed in still_available_players).
    ## Note: ~ (not) and .isin adapted from: pandas - Indexing and selecting data
    ## https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html

def view_available_players():
    """
    Prints a list of players who are available to be drafted. Uses get_available_players().
    """
    available_players = get_available_players().head(25) # Calls the previous get_available_players function (which returns df of all players who haven NOT been drafted yet - who are NOT in drafted_players)...
                                                         # [...] to make a new DF (available_players) containing the first 25 rows with .head(25); works the same as "head" in default R.
    print(available_players)
    
def check_single_player():
    """
    Allows the user to input a player's name to displays that player's statistics; independent function.
    """
    player_name = input("Enter the name of the player you'd like to look up: ") # User inputs a player's name and stores it in the variable player_name.
    if player_name in df['NAME'].values: # Checks if the entered player_name is in the original df. 
        single_player_data = df[df['NAME'] == player_name] # If the player name was found, this creates a new "single_player_data" data frame (from the original df) containing the row for the selected player.
        
        ## Checking if player is a goalie or not by using the NaN (Not a Number) from the original Spreadsheet; Goalies have blank Skater stats (ex. Goals), Skaters have blank Goalie stats (ex. Wins).
        # Displaying the player's stats based on whether they are a skater or a goalie:
        if pd.isna(single_player_data['G'].iloc[0]):  # Check if the Goals (G) value is NaN; here, .iloc[0] is selecting the whole row to find the cell corresponding with Goals (G).
                                                      ## Adapted from: Pandas & Python for Data Analysis by Example – Full Course for Beginners
                                                      ## https://www.youtube.com/watch?v=gtjxAH8uaP0
            print(single_player_data[['RK', 'NAME', 'TEAM', 'W', 'SV']]) # Print Rank, Name, Team, Wins, and Saves (Wins and Saves are Goalie specific).
        else:
            # Otherwise we know it's a Skater, so display Skater categories.
            print(single_player_data[['RK', 'NAME', 'TEAM','G', 'A', 'PTS', 'SOG', 'PPP']])
    else:
        print("Player not found, please try again (check spelling).") # If the player's name is not found in the 'NAME' column prints this (likely a user spelling error, or they've been drafted).
    
def recommend_best_player():
    '''
    Recommending the best player available based on rank (from Sheet 1 - Dom's Projections). Uses get_available_players().
    '''
    still_available_players = get_available_players() # Calls get_available_players function (which returns a list of players NOT in drafted_players) and saves as still_available_players df.
    
    best_player = still_available_players.sort_values(by='RK').iloc[0] # New variable to store best available player that is STILL AVAILABLE, based on Rank (RK column in Spreadsheet).
                                                                       ## Using Integer-location based Indexing (.iloc[0]) on the still_available_players df:
                                                                       # .sort_values(by='RK'): Sort the RK column (which puts player with the best rank on top).
                                                                       # .iloc[0]: Then, return the the values of the first row of our new df (still_available_players) as a panda Series (best_player).
                                                                       # panda Series: a single column of data with an associated index (then index here is the categories, and their associated values is the column.
                                                                       # Each element in this series corresponds with a column value for that player (Name, Team, Goals, etc.)
                                                                       # This corresponds with the Spreadsheet (where RK is cell A1, and Connor McDavid is the #1 player).
                                                                       ## Adapted from: Pandas DataFrame iloc Property - W3 Schools
                                                                       ## https://www.w3schools.com/python/pandas/ref_df_iloc.asp
    
    best_player_df = pd.DataFrame([best_player])  # pd.DataFrame(best_player): turns the best_player panda series into a DataFrame, by using the best_player series as a row (in the new best_player_df).
                                                  ## Adapted from: How to Create Pandas DataFrame from Series (Example 2: Creating Pandas DataFrame Using Series as Row) - Zach
                                                  ## https://www.statology.org/pandas-create-dataframe-from-series/
    
    ## Again, checking if player is a goalie or not by using the NaN (Not a Number) from the original Spreadsheet; Goalies have blank Skater stats (ex. Goals), Skaters have blank Goalie stats (ex. Wins).
    # Displaying the player's stats based on whether they are a skater or a goalie:
    if pd.isna(best_player['G']):  # Check if the Goals (G) value is NaN.
                                   ## Adapted from: Pandas & Python for Data Analysis by Example – Full Course for Beginners
                                   ## https://www.youtube.com/watch?v=gtjxAH8uaP0
        
        goalie_columns = ['RK', 'NAME', 'TEAM', 'W', 'SV'] # Create a list that has ONLY Goalie stats in it.
        return best_player_df[goalie_columns] # Returns the recommendation (from best_player_df), but ONLY showing goalie-specific columns from goalie_columns list (otherwise the NaN Skater Columns show up).
    
    else: # else case: if the player is not a Goalie (specifically, Skaters won't have NaN in Goals):
        skater_columns = ['RK', 'NAME', 'G', 'A', 'PTS', 'SOG', 'PPP'] # Create a list that shows ONLY Skater stats in it.
        return best_player_df[skater_columns] # Returns the recommendation (from best_player_df), but ONLY showing skater-specific columns from skater_columns list.
        
def draft_player():
    """
    Drafts a player to a team specified by the user, considering only the relevant categories (from the projections) based on position (Goalie/Skater). Modifies drafted_players, and uses display_player_stats().
    """
    global drafted_players  # Need to specify "global" here so we can modify the global drafted_players (that empty list at the beginning). Again, without global this would be local only within this function.
    
    player_name = input("Enter player name to draft: ") # Variable storing player name.
    team_name = input("Enter team name (myteam, team2, team3, team4): ").strip().lower() # Variable storing Team (these are pre-set corresponding to dictionary from before).
                                                                                         # .strip().lower()
                                                                                         # Adapted from: pandas.Series.str.strip
                                                                                         # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.strip.html
                                                                                         # [...] and from: pandas.Series.str.lower
                                                                                         # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.lower.html

    if player_name in df['NAME'].values and player_name not in drafted_players: # Checks if the player is in the original df under the 'NAME' column, and not already drafted (not in drafted_players list).
        try:
            teams[team_name].append(player_name) # Then, add to the key-value pairs in the teams dictionary (specified before)...
                                                 ## (Mentioned previously) adapted from Decoding Dictionaries in Python: A Comprehensive Guide to Key-Value Mastery - Rishu Gandhi
                                                 ## https://blog.stackademic.com/decoding-dictionaries-in-python-a-comprehensive-guide-to-key-value-mastery-56d67bf06030
            drafted_players.append(player_name) # And, append the list in drafted_players.
        
            print(f"{player_name} has been added to {team_name}.") # f-string to print the contents of {player_name} and {team_name}.
        
            drafted_player_data = df[df['NAME'] == player_name] # Creates another subset df containing only the row where the player's name matches what was specified in "player_name".
                                                                ## Note: this df gets passed to display_player_stats.
            display_player_stats(drafted_player_data) # Calls the function "display_player_stats" - which displays the stats for players - passing the drafted_player_data df.
        except KeyError:
                print(f"Team '{team_name}' not found. Please check the team name and try again.") # Try-except block just in case user types in the team_name incorrectly.   
    else:
        print("Player not found (please check the spelling) or has already been drafted.")
        
def display_player_stats(drafted_player_data): ## Passing drafted_player_data from the draft_player function.
    """
    Non-interactive function (works similarly to check_single_player) that displays category stats for drafted player(s), distinguishing between Goalies and Skaters. Used by draft_player() and display_team_stats().
    """
    goalie_columns = ['RK', 'NAME', 'TEAM', 'W', 'SV'] # List for Goalie categories.
    skater_columns = ['RK', 'NAME', 'TEAM', 'G', 'A', 'PTS', 'SOG', 'PPP'] # List for Skater categories.

    if pd.isna(drafted_player_data['G'].iloc[0]): # Check if 'Goals' column is NaN (pandas function pd.isna) for goalies by selecting the first row of the drafted_player_data df (from draft_player) using .iloc[0] again.
                                                  ## Adapted from: Pandas & Python for Data Analysis by Example – Full Course for Beginners
                                                  ## https://www.youtube.com/watch?v=gtjxAH8uaP0
        print(drafted_player_data[goalie_columns]) # If the player is a Goalie, print the stats in goalie_columns from drafter_player_data df.
    else:
        print(drafted_player_data[skater_columns]) # Otherwise, the player must be a Skater - so print the stats in the skater_columns from drafted_player_data df.
    
def view_teams():
    """
    Shows the roster of each team; uses 'teams' dictionary to print out each team's drafted players. Uses compare_team_rosters().
    """
    for team, players in teams.items(): # Iterate over each key-value pair in "teams" dictionary (loop dictionary items method); specifically, "team" is the team name, and "players" is the associated drafted list.
                                        ## Adapted from: Iterate Through a Dictionary in Python: A Coding Deep Dive - Claudio Sabato
                                        ## https://codefather.tech/blog/iterate-through-dictionary-python/
        
        print(f"\n{team} Roster:") # f-string to print the contents of {team}; "\n" starts a new line before printing {team} Roster. 
                                   ## Adapted from: Python New Line and How to Python Print Without a Newline - Estefania Cassingena Navone
                                   ## https://www.freecodecamp.org/news/python-new-line-and-how-to-python-print-without-a-newline/
                                   
        if players: # Checks if the list "players" is empty or not.
            for player in players: # Goes through the players list.
                print(f"- {player}") # f-string: Prints each player's name within the team.
        else:
            print("No players have been drafted yet!")

    compare_teams = input("\nWould you like to compare teams? (yes/no): ").lower() # .lower: converts the input to lower-case so nothing messes up.
    if compare_teams == 'yes': # If the user inputs yes, regardless of the case...
        compare_team_rosters() # Then call the compare_team_rosters function (user can view all teams stats, or compare specific teams.

def compare_team_rosters():
    """
    Options to compare team rosters (individual comparisons or by totals); user can choose between viewing all team rosters, comparing two specific teams, 
    viewing player stats from all relevant columns. Used by view_teams().
    """
    choice = input("Choose an option: \n1. View all team rosters\n2. Compare two teams\nEnter your choice: ") # User input stored as "choice"; 2 options (separated by spacing via \n1 and \n2).
                                                                                                              ## Adapted from: Python New Line and How to Python Print Without a Newline - Estefania Cassingena Navone
                                                                                                              ## https://www.freecodecamp.org/news/python-new-line-and-how-to-python-print-without-a-newline/
    if choice == '1': # Checks if the user's input is equivalent compared to (==) to string "1".
        for team, players in teams.items(): # Iterate over each key-value pair in "teams" dictionary (loop dictionary items method); specifically, "team" is the team name, and "players" is the associated drafted list.
                                            ## (Previously) Adapted from: Iterate Through a Dictionary in Python: A Coding Deep Dive - Claudio Sabato
                                            ## https://codefather.tech/blog/iterate-through-dictionary-python/
            print(f"\n{team} Roster:") # f-string to print the contents of {team}; "\n" starts a new line before printing {team} Roster. 
            display_team_stats(team) # Calls the display_team_stats function for each team, passing the current team's name as the argument.

    elif choice == '2':
        # team1 & team2 variables storing user input:
        team1 = input("Enter the first team to compare (myteam, team2, team3, team4):").strip().lower() # Removing whitespace and forcing lower-case to prevent user error.
        team2 = input("Enter the second team to compare (myteam, team2, team3, team4): ").strip().lower()

        if team1 in teams and team2 in teams: # Checks if both teams are in the 'teams' dictionary (from the beginning of the code).
            print(f"\n{team1} Roster:") # f-string to print the contents of {team1}; "\n" starts a new line before printing {team} Roster.
            display_team_stats(team1) # Calls the display_team_stats function for team1.

            print(f"\n{team2} Roster:") # f-string to print the contents of {team2}; "\n" starts a new line before printing {team} Roster.
            display_team_stats(team2) # Calls the display_team_stats function for team2.
        else:
            print("Something went wrong. Check to see both team names are correct and try again.")
        
def display_team_stats(team_name):
    """
    Displays the roster and detailed stats of a specified team, including the totals of all stats. Used by compare_team_rosters().
    """
    team_stats = []  # Initialize as an empty list to store the df of individual player stats for the specified team.

    for player in teams[team_name]: # Loops over each player in the specified team.
        player_data = df[df['NAME'] == player] # Retrieves player stats from the original data frame (df) - where the player's name is in the "NAME" column - and creates a new player_data df.
        display_player_stats(player_data) # Calls display_player_stats function to print the stats from the new df (player_data).
        team_stats.append(player_data) # Appends the player's data frame to the team_stats list.

    ## Concatenate (pd.concat) all player data Data Frames and calculate the sum of each column:
    ## Adapted from: pandas - Merge, join, concatenate and compare
    ## https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    if team_stats: # If team_stats is not empty (i.e., the team has drafted players already)...
        total_stats_df = pd.concat(team_stats) # Concatenates all data frames in team_stats into a single data frame total_stats_df. This is done using pd.concat.
                                               ## Essentially, team_stats is a list of dfs (the stats of each individual player on the team); here we combine all the separate dfs into a single vertical df (total_stats_df).
        totals = total_stats_df.sum(numeric_only=True) # Calculates the sum (total_stats_df.sum) of each "numeric_only=True" (numeric).  
                                                       # sum() method is pandas way of adding up all values in each column (similar to count/summarize in R).
                                                       ## Adapted from: Pandas DataFrame sum() Method - W3 Schools
                                                       ## https://www.w3schools.com/python/pandas/ref_df_sum.asp
                                                       ## [...] and from: Remove name, dtype from pandas output of dataframe or series
                                                       ## https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output-of-dataframe-or-series
        
        # Exclude the 'RK' column from the totals (don't need to show the sum of the ranks - provides nothing).
        totals = totals.drop(labels=['RK']) # drop(labels: specifies to drop the 'RK' column (which has been summed prior).
                                            ## Adapted from: A Comprehensive Guide to Pandas drop() Method in Python
                                            ## https://machinelearningtutorials.org/a-comprehensive-guide-to-pandas-drop-method-in-python/

        # Display the total stats
        print("\nTotal Stats:")
        print(totals.to_string())  # Using to_string() removes to remove the "dtype" information (which is typically displayed at the bottom of a df). 
                                   ## Adapted from: pandas - pandas.DataFrame.to_string
                                   ## https://pandas.pydata.org/pandas-docs/version/2.1/reference/api/pandas.DataFrame.to_string.html
    else:
        print("No players have been drafted to this team.")

def main_menu():
    """
    Runs the main menu loop, allowing the user to choose from various options related to drafting/viewing/comparing players and their stats.
    """    
    while True:
        print("\nFantasy Hockey Live Draft Helper") # Using "\n" again for spacing.
        print("1. Load Projection File")
        print("2. View Available Players")
        print("3. Check a Single Player")
        print("4. Best Player Recommendation")
        print("5. Draft a Player")
        print("6. View & Compare Team Rosters")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            load_projection_file() # Calls the load_projection_file() function.
        elif choice == '2':
            print("Displaying the Top 25 players still available to draft.")
            view_available_players() # Calls the view_available_players() function.
        elif choice == '3':
            check_single_player() # Calls the check_single_player() function.           
        elif choice == '4':
            if not df.empty:
                best_player_stats = recommend_best_player() #
                print("Here's the best player available to draft:")
                print(best_player_stats.to_string(index=False)) # Excludes the index column from the output with "index=False" (cleaner).
                ## Adapted from: Remove name, dtype from pandas output of dataframe or series
                ## https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output-of-dataframe-or-series                                                                
        elif choice == '5':
            draft_player()            
        elif choice == '6':
            view_teams() # Calls the view_teams() function.
        elif choice == '7':
            print("Exiting the application. Good bye!")
            break
        else:
            print("Invalid choice. Please try again!")

if __name__ == "__main__":
    main_menu()
