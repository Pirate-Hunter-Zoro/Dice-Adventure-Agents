# PLEASE IMPORT ANY PACKAGES YOU NEED

class DiceAdventureAgent:
    """
    An interface to connect agents to the Dice Adventure environment.
    Developers must implement the take_action() function.
    - init():         Initialize any needed variables.
    - take_action():  Determines which action to take given a state (list<dict>) and list of actions. Note that your
                      agent does not need to use the list of actions, it is just provided for convenience.
    """
    def __init__(self, character_name: str, character_id: str) -> None:
        """
        Initialize any needed variables. The character_name and character_id arguments specify the name and ID
        of the character this agent will play as.
        :param character_name: The character the agent will play as
        :param character_id: The character ID corresponding to the character

        Player ID mappings:
            dwarf : C11
            giant : C21
            human : C31
        """
        self.character = character_name
        self.character_id = character_id
        self.has_key = False

        if self.is_dwarf():
            self.action_points = 6
            self.vision_range = 3
            self.key_shrine = 'K1'
            self.type = 'Dwarf'
            self.skills = {'rocks': 4, 'traps': 8, 'monsters': 6}
        elif self.is_human():
            self.action_points = 4
            self.vision_range = 5
            self.key_shrine = 'K3'
            self.type = 'Human'
            self.skills = {'rocks': 6, 'traps': 6, 'monsters': 8}
        elif self.is_giant():
            self.action_points = 3
            self.vision_range = 7
            self.key_shrine = 'K2'
            self.type = 'Giant'
            self.skills = {'rocks': 8, 'traps': 4, 'monsters': 6}
        else:
            assert False, "Invalid character ID. Must be C11, C21, or C31."

    def is_dwarf(self) -> bool:
        """
        Check if the agent is playing as a dwarf.
        :return: True if the agent is a dwarf, False otherwise.
        """
        return self.character_id == "C11"
    
    def is_giant(self) -> bool:
        """
        Check if the agent is playing as a giant.
        :return: True if the agent is a giant, False otherwise.
        """
        return self.character_id == "C21"
    
    def is_human(self) -> bool:
        """
        Check if the agent is playing as a human.
        :return: True if the agent is a human, False otherwise.
        """
        return self.character_id == "C31"

    def take_action(self, state: list[dict], actions: list[str]) -> str:
        """
        Given a game state and list of actions, the agent should determine which action to take and return a
        string representation of the action.
        :param state:   A 'Dice Adventure' game state
        :param actions: A list of string action names
        :return:        An action from the 'actions' list
        """
        my_position = None
        shrine_position = None
        tower_position = None
        visible_monsters = []
        visible_rocks = []
        visible_traps = []
        for entity in state:
            entityType = entity.get('entityType', None)
            if entityType == None:
                entityType = entity.get('type', None)
            objKey = entity.get('objKey', None)

            if entityType == self.type:
                my_position = (entity.get('x'), entity.get('y'))
            elif entityType == 'monster':
                visible_monsters.append(entity)
            elif entityType == 'Shrine' and entity.get('character') == self.type:
                shrine_position = (entity.get('x'), entity.get('y'))
            elif entityType == 'Goal':
                tower_position = (entity.get('x'), entity.get('y'))
            elif objKey == 'R1':
                visible_rocks.append(entity)
            elif objKey == 'T1':
                visible_traps.append(entity)
        
        if my_position and shrine_position:
            self.has_key = my_position == shrine_position

        ping_string = None
        if visible_monsters and not self.is_human():
            # If there are visible monsters, and I'm not the human, I should not attack but instead ping
            first_monster = visible_monsters[0]
            ping_string = f'ping ! {first_monster.get("x")} {first_monster.get("y")}'
        elif visible_rocks and self.is_dwarf():
            # Gotta ping the rocks if I'm a dwarf because I'm bad at them
            first_rock = visible_rocks[0]
            ping_string = f'ping V {first_rock.get("x")} {first_rock.get("y")}'
        elif visible_traps and self.is_giant():
            # Gotta ping the traps if I'm a giant because I'm bad at them
            first_trap = visible_traps[0]
            ping_string = f'ping V {first_trap.get("x")} {first_trap.get("y")}'

        if not ping_string:
            # If I didn't ping, then I need to do something else
            if visible_monsters:
                assert self.is_human(), "If a monster was visible and I was not human, I should have pinged."
                first_monster = visible_monsters[0]
                return f'move {first_monster.get("x")} {first_monster.get("y")}'
            elif visible_traps:
                assert not self.is_giant(), "If a trap was visible and I was a giant, I should have pinged."
                first_trap = visible_traps[0]
                return f'move {first_trap.get("x")} {first_trap.get("y")}'
            elif visible_rocks:
                assert not self.is_dwarf(), "If a rock was visible and I was a dwarf, I should have pinged."
                first_rock = visible_rocks[0]
                return f'move {first_rock.get("x")} {first_rock.get("y")}'
            else:
                # Goal seeking state
                assert my_position, "I should have a position."
                if self.has_key and tower_position:
                    # Goal is tower and tower is visible
                    return f'move {tower_position[0]} {tower_position[1]}'
                elif not self.has_key and shrine_position:
                    # Goal is shrine and shrine is visible
                    return f'move {shrine_position[0]} {shrine_position[1]}'
                elif self.has_key:
                    # Goal is tower but tower is not visible
                    # TODO - will need to implement a way to get the tower visible
                    return 'wait'
                else: 
                    # Goal is shrine but shrine is not visible
                    # TODO - will need to implement a way to get the shrine visible
                    return 'wait'
        else:
            # If I pinged, then I need to return the ping string
            return ping_string