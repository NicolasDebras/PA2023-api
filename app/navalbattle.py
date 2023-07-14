import json
import random

PLAYER_ARG = {
    "name" : "players",
    "type" : "int",
    "min" : 2,
    "max" : 2,
    "description" : "number of players"
}

BOATS_ARG = {
    "name" : "boats",
    "type" : "int",
    "min" : 1,
    "description" : "number of boats"
}

class Grid:
    def __init__(self, case_size=100, size=10, boats=5):
        self.__case_size = case_size
        self.__size = size
        self.__grid = [[0]*size for _ in range(size)]
        self.__current_player = 1
        self.__boats = {1: boats, 2: boats}
        self.__shots = [[0]*size for _ in range(size)]
        self.current_instructions = []
        self.__generate_boats(boats)

    def __generate_boats(self, boats):
        for _ in range(boats):
            x, y = random.randint(0, self.__size - 1), random.randint(0, self.__size - 1)
            while self.__grid[x][y] == 1:
                x, y = random.randint(0, self.__size - 1), random.randint(0, self.__size - 1)
            self.__grid[x][y] = 1
    
    def get_grid_state(self):
        return [row.copy() for row in self.__grid]
    
    def fire(self, x, y):
        self.__shots[x][y] = 1
        if self.__grid[x][y] == 1:
            self.__grid[x][y] = 0
            self.__boats[self.__current_player] -= 1
            return 1
        else:
            return 0

    def get_svg(self, player):
        data = {
            "width": str(self.__size * self.__case_size),
            "height": str(self.__size * self.__case_size),
            "content": [],
            "player": player
        }

        data["content"] = [
			{"tag":"style", "content": "line{stroke:black;stroke-width:4;}"}
		]

        data["content"].append(self.__add_grid_lines())
        data["content"].append(self.__add_previous_shots())
        
        return data

    def __add_grid_lines(self):
        lines = []

        # Ajout des lignes verticales
        for i in range(self.__size + 1):
            lines.append({
                "tag": "line",
                "x1": str(i * self.__case_size),
                "y1": "0",
                "x2": str(i * self.__case_size),
                "y2": str(self.__size * self.__case_size),
            })

        # Ajout des lignes horizontales
        for i in range(self.__size + 1):
            lines.append({
                "tag": "line",
                "x1": "0",
                "y1": str(i * self.__case_size),
                "x2": str(self.__size * self.__case_size),
                "y2": str(i * self.__case_size)
            })

        return lines

    def __add_previous_shots(self):
        shots = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__shots[i][j] == 1:
                    shots.append({
                        "tag": "circle",
                        "cx": str(i * self.__case_size + self.__case_size // 2),
                        "cy": str(j * self.__case_size + self.__case_size // 2),
                        "r": str(self.__case_size // 4),
                        "fill": "red" if self.__grid[i][j] == 0 else "green"
                    })
        return shots


    def get_game_state(self):
        return {
             "game_state": {
                "scores": [self.__boats[1], self.__boats[2]],
                "game_over": self.__boats[1] == 0 or self.__boats[2] == 0
            }
        }


# Main part

def read_json():
    content = input()
    opening_curly_brackets = content.count("{")
    closing_curly_brackets = content.count("}")
    while opening_curly_brackets < 1 or closing_curly_brackets != opening_curly_brackets:
        content += input()
        opening_curly_brackets = content.count("{")
        closing_curly_brackets = content.count("}")
    content = content.strip()
    try:
        content = json.loads(content)
    except json.JSONDecodeError:
        print_error("BAD_JSON", message="Input is not valid JSON", fatal=True)
    return content

def print_error(type, **kwargs):
    quit = kwargs.pop("fatal", False)
    d = {"type":type}
    d.update(kwargs)
    print(json.dumps({"errors":[d]}, indent=2))
    if quit:
        exit()

def init(grid):
    content = read_json()
    if "init" not in content:
        print_error("BAD_FORMAT", 
            message="init key is missing", 
            fatal=True)
    init_content = content["init"]
    if "players" not in init_content : 
        print_error("MISSING_ARGUMENT", 
            arg=PLAYER_ARG, 
            fatal=True)
    if init_content["players"] != 2:
        print_error("INCORRECT_VALUE", 
            arg=PLAYER_ARG, 
            value=init_content["players"],
            fatal=True)
    if "boats" not in init_content : 
        print_error("MISSING_ARGUMENT", 
            arg=BOATS_ARG, 
            fatal=True)
    if len(init_content)>2:
        for k,v in init_content.items():
            if k not in {"players", "boats"}:
                print_error("UNEXPECTED_ARGUMENT", 
                    argname=k, 
                    value=v,
                    fatal=True)

    grid.current_instructions.append(grid.get_grid_state())
    print(json.dumps({
            "displays": [grid.get_svg(1), grid.get_svg(2)],
            **grid.get_game_state()
        }, indent=2))


def turn(grid):
    content = read_json()
    if "actions" not in content:
        print_error("BAD_FORMAT", 
            message="actions key is missing")
        return False
    actions = content["actions"]
    if not isinstance(actions, list):
        print_error("BAD_FORMAT", 
            message="actions value is not a list")
        return False
    if len(actions) != 1:
        print_error("BAD_FORMAT", 
            message="exactly one action is expected")
        return False
    action = actions[0]
    if not isinstance(action, dict):
        print_error("BAD_FORMAT", 
            message="action is not a dict containing player, x and y values")
    if not {"x", "y","player"}.issubset(action.keys()):
        print_error("BAD_FORMAT", 
            message="action is not a dict containing player, x and y values")
    if int(action["player"]) != grid.current_player:
        print_error("MISSING_ACTION", 
            player=grid.current_player,
            requested_action=grid.current_action)        
        return False
    try:
        score = grid.fire(int(action["x"]), int(action["y"]))
    except AttributeError:
        print_error("WRONG_ACTION", 
            subtype="OUT_OF_ZONE",
            player=grid.current_player,
            action=action,
            requested_action=grid.current_action)
        return False    
    print(json.dumps({
            "displays": [grid.get_svg(1), grid.get_svg(2)],
            **grid.get_game_state()
        }, indent=2))

    return score != 0


def str_all_values(content):
    if isinstance(content, dict):
        for k,v in content.items():
            content[k] = str_all_values(v)

    elif isinstance(content, list):
        for i,v in enumerate(content):
            content[i] = str_all_values(v)
    else:
        content = str(content)
    return content

if __name__ == "__main__":
    grid = Grid()
    init(grid)
    while not turn(grid):
        pass

        