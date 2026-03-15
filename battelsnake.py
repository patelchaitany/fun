# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import heapq
import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "ynatiahc",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


DIRECTIONS = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}


def _heuristic(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _astar(start: tuple, goal: tuple, obstacles: set, width: int, height: int):
    """Return the first move direction toward goal using A*, or None if unreachable."""
    open_set = [(0 + _heuristic(start, goal), 0, start)]
    came_from: dict = {}
    g_score = {start: 0}

    while open_set:
        _, g, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path back to the step right after start
            while came_from.get(current) != start:
                current = came_from[current]
            dx, dy = current[0] - start[0], current[1] - start[1]
            for name, (mx, my) in DIRECTIONS.items():
                if (mx, my) == (dx, dy):
                    return name
            return None

        if g > g_score.get(current, float("inf")):
            continue

        for dx, dy in DIRECTIONS.values():
            nx, ny = current[0] + dx, current[1] + dy
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if (nx, ny) in obstacles and (nx, ny) != goal:
                continue
            ng = g + 1
            if ng < g_score.get((nx, ny), float("inf")):
                g_score[(nx, ny)] = ng
                heapq.heappush(open_set, (ng + _heuristic((nx, ny), goal), ng, (nx, ny)))
                came_from[(nx, ny)] = current

    return None


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    print(game_state)
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    return {"move": "down","shout": "Hello, world!"}
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    print(is_move_safe)


    # Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    print(is_move_safe)

    # Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']

    for segment in my_body:
        if my_head["x"] - 1 == segment["x"] and my_head["y"] == segment["y"]:
            is_move_safe["left"] = False
        if my_head["x"] + 1 == segment["x"] and my_head["y"] == segment["y"]:
            is_move_safe["right"] = False
        if my_head["y"] - 1 == segment["y"] and my_head["x"] == segment["x"]:
            is_move_safe["down"] = False
        if my_head["y"] + 1 == segment["y"] and my_head["x"] == segment["x"]:
            is_move_safe["up"] = False

    print(is_move_safe)
    # Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for snake in opponents:
        for segment in snake["body"]:
            if my_head["x"] - 1 == segment["x"] and my_head["y"] == segment["y"]:
                is_move_safe["left"] = False
            if my_head["x"] + 1 == segment["x"] and my_head["y"] == segment["y"]:
                is_move_safe["right"] = False
            if my_head["y"] - 1 == segment["y"] and my_head["x"] == segment["x"]:
                is_move_safe["down"] = False
            if my_head["y"] + 1 == segment["y"] and my_head["x"] == segment["x"]:
                is_move_safe["up"] = False

    print(is_move_safe)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down","shout": "Hello, world!"}

    # Step 4 - Move towards food using A* pathfinding
    food = game_state['board']['food']

    obstacles = set()
    for segment in my_body:
        obstacles.add((segment["x"], segment["y"]))
    for snake in opponents:
        for segment in snake["body"]:
            obstacles.add((segment["x"], segment["y"]))

    head_pos = (my_head["x"], my_head["y"])
    best_move = None
    best_dist = float("inf")

    for morsel in food:
        goal = (morsel["x"], morsel["y"])
        dist = _heuristic(head_pos, goal)
        if dist < best_dist:
            direction = _astar(head_pos, goal, obstacles, board_width, board_height)
            if direction and direction in safe_moves:
                best_move = direction
                best_dist = dist

    print(best_move)
    next_move = best_move if best_move else random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move,"shout": "Hello, world!"}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})