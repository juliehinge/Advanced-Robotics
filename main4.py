from collections import deque
import copy

# Sokoban game board representation
class Sokoban:
    def __init__(self, board):
        self.board = board
        self.player_pos = self.find_player()
        self.targets = self.find_targets()
        self.crates = self.find_crates()
        self.width = len(board[0])
        self.height = len(board)

    def find_player(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == '@':
                    return (y, x)

    def find_targets(self):
        targets = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == '.' or cell == '*':
                    targets.append((y, x))
        return targets

    def find_crates(self):
        crates = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell == '$' or cell == '*':
                    crates.append((y, x))
        return crates

    def is_solved(self):
        for crate in self.crates:
            if crate not in self.targets:
                return False
        return True

    def is_valid_move(self, y, x):
        if 0 <= y < self.height and 0 <= x < self.width and self.board[y][x] != '#':
            return True
        return False

    def move(self, direction):
        dy, dx = direction
        new_y, new_x = self.player_pos[0] + dy, self.player_pos[1] + dx
        if not self.is_valid_move(new_y, new_x):
            return False

        # Handle pushing crate
        if (new_y, new_x) in self.crates:
            crate_new_y, crate_new_x = new_y + dy, new_x + dx
            if not self.is_valid_move(crate_new_y, crate_new_x) or (crate_new_y, crate_new_x) in self.crates:
                return False
            self.crates.remove((new_y, new_x))
            self.crates.append((crate_new_y, crate_new_x))
        #self.board[self.player_pos[0]][self.player_pos[1]] = ' '
        self.player_pos = (new_y, new_x)
        #self.board[new_y][new_x] = '@'
        return True
    
    def print_current_state(self):
        # Create a copy of the board to avoid modifying the original
        board_copy = [list(row) for row in self.board]

        # Place crates and player on the board copy
        for crate in self.crates:
            if crate in self.targets:
                board_copy[crate[0]][crate[1]] = '*'
            else:
                board_copy[crate[0]][crate[1]] = '$'

        for target in self.targets:
            # Make sure targets are displayed correctly if a crate isn't on them
            if board_copy[target[0]][target[1]] == ' ':
                board_copy[target[0]][target[1]] = '.'

        # Place the player on the board
        y, x = self.player_pos
        board_copy[y][x] = '@'

        # Print the board row by row
        for row in board_copy:
            print(''.join(row))
        print()
    

# Utility function to convert directions to human-readable format
def direction_to_string(direction):
    if direction == (-1, 0):
        return "Up"
    elif direction == (1, 0):
        return "Down"
    elif direction == (0, -1):
        return "Left"
    elif direction == (0, 1):
        return "Right"
        

def print_state(state):
    for i in state:
        print(i)

# Sokoban solver using BFS
def sokoban_solver_bfs(initial_board):
    initial_state = Sokoban(initial_board)
    queue = deque([(initial_state, [])])  # Queue holds (state, path) tuples
    explored = set()

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while queue:
        current_state, path = queue.popleft()
        print("Current state is:")
        current_state.print_current_state()
        print()
        # Check if we've already visited this state
        current_key = (tuple(current_state.crates), current_state.player_pos)
        if current_key in explored:
            continue
        explored.add(current_key)

        # Check if the game is solved
        if current_state.is_solved():
            return path

        # Explore possible moves
        print("Exploring the following states:")
        for direction in directions:
            new_state = copy.deepcopy(current_state)
            if new_state.move(direction):
                new_state.print_current_state()
                new_path = path + [direction]
                queue.append((new_state, new_path))
        print("----------------------------------")

    return None



# Sample game board
game_board = [
    ['#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '@', ' ', '#', ' ', '#'],
    ['#', '$', '*', ' ', '$', ' ', '#'],
    ['#', ' ', ' ', ' ', '$', ' ', '#'],
    ['#', ' ', '.', '.', ' ', ' ', '#'],
    ['#', ' ', ' ', '*', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#']
]

game_board1 = [
    ['#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', ' ', '.', ' ', '#'],
    ['#', ' ', '$', '@', ' ', '#'],
    ['#', ' ', ' ', ' ', ' ', '#'],
    ['#', '#', '#', '#', '#', '#']
]

# Solve the game
solution = sokoban_solver_bfs(game_board1)

if solution:
    print("Solved! Moves:", [direction_to_string(move) for move in solution])
else:
    print("Unsolvable")