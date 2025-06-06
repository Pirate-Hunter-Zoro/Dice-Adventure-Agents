class DiceAdventureHumanAgent:
    """
    Provides a uniform interface to connect human agents to Dice Adventure environment.
    Developers must implement the take_action() function.
    - init():         Initialize any needed variables.
    - take_action():  Determines which action to take given a state (dict) and list of actions. Note that your
                      agent does not need to use the list of actions, it is just provided for convenience.
    """
    def __init__(self, character_name, character_code):
        """
        Initialize any needed variables.
        :param character_name: (string) The character the agent will play as
        :param character_code: (string) The character code corresponding to the character

        Player code index:
        {
            "Dwarf" : "C1",
            "Giant" : "C2",
            "Human" : "C3"
        }
        """
        self.character = character_name
        self.character_code = character_code

    def take_action(self, state, actions):
        """
        Given a game state and list of actions, the agent should determine which action to take and return a
        string representation of the action.
        :param state:   (dict) A 'Dice Adventure' game state
        :param actions: (list) A list of string action names
        :return:        (string) An action from the 'actions' list
        """
        
        print(f"Character: {self.character}, Code: {self.character_code}")
        
        #first we see what phase we are in
        phase = state[0].get('currentPhase')
        print(f"Current phase: {phase}")
        # Display available actions
        print("Available actions:")
        for i, action in enumerate(actions):
            print(f"{i + 1}: {action}")
        # Prompt user for action
        action_index = int(input("Choose an action (number): ")) - 1
        if 0 <= action_index < len(actions):
            action = actions[action_index]
        else:
            print("Invalid action selected. Choosing a random action.")
            action = choice(actions)
        print(f"Chosen action: {action}")
        return action
 