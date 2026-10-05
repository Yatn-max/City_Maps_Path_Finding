import pygame
import subprocess
import os
import math


# ============================================================
# SETTINGS
# ============================================================

WIDTH = 1200
HEIGHT = 800

FPS = 60

MARGIN = 50

NODE_RADIUS = 2

START_RADIUS = 8
END_RADIUS = 8  

ROAD_WIDTH = 1
PATH_WIDTH = 5



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GRAPH_FILE = os.path.join(BASE_DIR, "graph_data.txt")
NODES_FILE = os.path.join(BASE_DIR, "nodes_data.txt")
PATH_FILE = os.path.join(BASE_DIR, "path.txt")

CPP_PROGRAM = os.path.join(BASE_DIR, "A_yatn.exe")


# ============================================================
# LOAD NODE COORDINATES
# ============================================================

def load_node_coordinates(filename):

    nodes = {}

    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            node_id = int(parts[0])

            latitude = float(parts[1])

            longitude = float(parts[2])

            nodes[node_id] = (
                latitude,
                longitude
            )

    print("Coordinates loaded:", len(nodes))

    return nodes


# ============================================================
# LOAD GRAPH
# ============================================================

def load_graph(filename):

    graph = []

    with open(filename, "r") as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            u = int(parts[0])

            v = int(parts[1])

            weight = float(parts[2])

            graph.append((u, v, weight))

    print("Graph edges loaded:", len(graph))

    return graph


# ============================================================
# LOAD PATH.TXT
# ============================================================

def load_path(filename):

    start_node = None

    end_node = None
    

    distance = None

#### adding new 
    
    block_node = None

    path = []

    if not os.path.exists(filename):

        return start_node, end_node, distance, path

    with open(filename, "r") as file:

        lines = file.readlines()

    reading_path = False

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("NO_PATH"):

            return None, None, None, []

        if line.startswith("START "):

            start_node = int(line.split()[1])

        elif line.startswith("END "):

            end_node = int(line.split()[1])

        elif line.startswith("DISTANCE "):

            value = line.split()[1]

            value = value.replace("m", "")

            distance = float(value)

        elif line == "PATH":

            reading_path = True

        elif reading_path:

            path.append(int(line))

    return start_node, end_node, distance, path


# ============================================================
# CONVERT LAT/LON TO SCREEN COORDINATES
# ============================================================

def create_screen_coordinates(nodes):

    latitudes = [
        value[0]
        for value in nodes.values()
    ]

    longitudes = [
        value[1]
        for value in nodes.values()
    ]

    min_lat = min(latitudes)
    max_lat = max(latitudes)

    min_lon = min(longitudes)
    max_lon = max(longitudes)

    if max_lat == min_lat:
        max_lat += 0.000001

    if max_lon == min_lon:
        max_lon += 0.000001

    screen_nodes = {}

    for node_id, (lat, lon) in nodes.items():

        x = (
            (lon - min_lon)
            /
            (max_lon - min_lon)
        )

        y = (
            (max_lat - lat)
            /
            (max_lat - min_lat)
        )

        x = MARGIN + x * (
            WIDTH - 2 * MARGIN
        )

        y = MARGIN + y * (
            HEIGHT - 2 * MARGIN
        )

        screen_nodes[node_id] = (
            int(x),
            int(y)
        )

    return screen_nodes


# ============================================================
# FIND NEAREST NODE
# ============================================================

def find_nearest_node(
    mouse_position,
    screen_nodes
):

    mouse_x, mouse_y = mouse_position

    nearest_node = None

    minimum_distance = float("inf")

    for node_id, (x, y) in screen_nodes.items():

        distance = math.sqrt(
            (mouse_x - x) ** 2
            +
            (mouse_y - y) ** 2
        )

        if distance < minimum_distance:

            minimum_distance = distance

            nearest_node = node_id

    return nearest_node


# ============================================================
# RUN C++ DIJKSTRA
# ============================================================

def run_dijkstra(start_node, end_node,blocked_node1,blocked_node2):

    print()
    print("Running Dijkstra...")
    print("Start:", start_node)
    print("End:", end_node)
    print("Blocked:", blocked_node1)
    print("Blocked:", blocked_node2)

    try:

        result = subprocess.run(
            [
                CPP_PROGRAM,
                str(start_node),
                str(end_node),
                str(blocked_node1),
                str(blocked_node2)
            ],
            cwd = BASE_DIR,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.stderr:

            print("C++ ERROR:")
            print(result.stderr)

    except Exception as e:

        print("Could not run C++ program:")
        print(e)


# ============================================================
# DRAW GRAPH
# ============================================================

def draw_graph(
    screen,
    graph,
    screen_nodes
):

    for u, v, weight in graph:

        if u not in screen_nodes:
            continue

        if v not in screen_nodes:
            continue

        x1, y1 = screen_nodes[u]

        x2, y2 = screen_nodes[v]

        pygame.draw.line(
            screen,
            (100, 100, 100),
            (x1, y1),
            (x2, y2),
            ROAD_WIDTH
        )


# ============================================================
# DRAW PATH
# ============================================================

def draw_path(
    screen,
    path,
    screen_nodes
):

    if len(path) < 2:

        return

    points = []

    for node in path:

        if node in screen_nodes:

            points.append(
                screen_nodes[node]
            )

    if len(points) >= 2:

        pygame.draw.lines(
            screen,
            (255, 50, 50),
            False,
            points,
            PATH_WIDTH
        )


# ============================================================
# DRAW SELECTED START NODE
# ============================================================

def draw_start(
    screen,
    start_node,
    screen_nodes
):

    if start_node is None:
        return

    if start_node not in screen_nodes:
        return

    x, y = screen_nodes[start_node]

    pygame.draw.circle(
        screen,
        (0, 255, 0),
        (x, y),
        START_RADIUS
    )


# ============================================================
# DRAW SELECTED END NODE
# ============================================================

def draw_end(
    screen,
    end_node,
    screen_nodes
):

    if end_node is None:
        return

    if end_node not in screen_nodes:
        return

    x, y = screen_nodes[end_node]

    pygame.draw.circle(
        screen,
        (255, 0, 0),
        (x, y),
        END_RADIUS
    )

# ============================================================
# DRAW BLOCKED NODE
# ============================================================

def draw_blocked(
    screen,
    blocked_node,
    screen_nodes
):
    if not blocked_node:
        return

    for node in blocked_node:

        if node not in screen_nodes:
            continue

        x,y = screen_nodes[node]

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (x, y),
            10
        )



# ============================================================
# DRAW INFORMATION
# ============================================================

def draw_information(
    screen,
    font,
    start_node,
    end_node,
    blocked_node,
    distance,
    path
):

    title = font.render(
        "Jodhpur Shortest Path",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (20, 15)
    )


    if start_node is None:

        text = font.render(
            "Click a node to select START",
            True,
            (0, 255, 0)
        )

        screen.blit(
            text,
            (20, 50)
        )

        return


    text = font.render(
        f"Start: {start_node}",
        True,
        (0, 255, 0)
    )

    screen.blit(
        text,
        (20, 50)
    )


    if end_node is None:

        text = font.render(
            "Click another node to select END",
            True,
            (255, 100, 100)
        )

        screen.blit(
            text,
            (20, 80)
        )

        return


    text = font.render(
        f"End: {end_node}",
        True,
        (255, 100, 100)
    )

    screen.blit(
        text,
        (20, 80)
    )


    if blocked_node is None:

        text = font.render(
            "Click another node to BLOCK it",
            True,
            (255, 165, 0)
        )

        screen.blit(
            text,
            (20, 110)
        )

    else:

        text = font.render(
            f"Blocked: {blocked_node}",
            True,
            (255, 165, 0)
        )

        screen.blit(
            text,
            (20, 110)
        )


    if distance is not None:

        text = font.render(
            f"Distance: {distance:.2f} m",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (20, 110)
        )


    if path:

        text = font.render(
            f"Path nodes: {len(path)}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            (20, 140)
        )


    text = font.render(
        "Press R to choose a new route",
        True,
        (200, 200, 200)
    )

    screen.blit(
        text,
        (20, 170)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading data...")


    nodes = load_node_coordinates(
        NODES_FILE
    )


    graph = load_graph(
        GRAPH_FILE
    )


    if not nodes:

        print("No coordinates found.")

        return


    if not graph:

        print("No graph found.")

        return


    screen_nodes = create_screen_coordinates(
        nodes
    )


    # --------------------------------------------------------
    # INITIALIZE PYGAME
    # --------------------------------------------------------

    pygame.init()


    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )


    pygame.display.set_caption(
        "Jodhpur Dijkstra Route Finder"
    )


    clock = pygame.time.Clock()


    font = pygame.font.SysFont(
        "Arial",
        20
    )


    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    start_node = None

    end_node = None

    blocked_node = None

    distance = None

    path = []


    running = True


    # ========================================================
    # MAIN LOOP
    # ========================================================
    block_mode = False


    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            # ====================================================
            # MOUSE CLICK
            # ====================================================

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    clicked_node = find_nearest_node(
                        event.pos,
                        screen_nodes
                    )


                    # --------------------------------------------
                    # BLOCK NODE MODE
                    # --------------------------------------------

                    if block_mode:

                        # Don't allow start node
                        if clicked_node == start_node:

                            print("Start node cannot be blocked.")
                            continue


                        # Don't allow end node
                        if clicked_node == end_node:

                            print("End node cannot be blocked.")
                            continue


                        # Don't allow duplicate block
                        if clicked_node in blocked_node:

                            print("Node already blocked.")
                            continue


                        # Add blocked node
                        blocked_node.append(clicked_node)

                        print(
                            "Blocked node selected:",
                            clicked_node
                        )


                        # ----------------------------------------
                        # Two nodes selected
                        # ----------------------------------------

                        if len(blocked_node) == 2:

                            block_mode = False

                            print(
                                "Two blocked nodes:",
                                blocked_node
                            )


                            # Run Dijkstra if start/end exist
                            if start_node is not None and end_node is not None:

                                run_dijkstra(
                                    start_node,
                                    end_node,
                                    blocked_node[0],
                                    blocked_node[1]
                                )


                                (
                                    start_node,
                                    end_node,
                                    distance,
                                    path
                                ) = load_path(
                                    PATH_FILE
                                )

                            else:

                                print(
                                    "Select start and end nodes first."
                                )
                                continue


                        else:


                            print(
                                "Select the second blocked node."
                            )
                            continue


                    # --------------------------------------------
                    # FIRST CLICK = START
                    # --------------------------------------------

                    if start_node is None:

                        start_node = clicked_node

                        print(
                            "Start selected:",
                            start_node
                        )


                    # --------------------------------------------
                    # SECOND CLICK = END
                    # --------------------------------------------

                    elif end_node is None:

                        if clicked_node == start_node:

                            print(
                                "End cannot be same as start."
                            )

                            continue


                        end_node = clicked_node

                        print(
                            "End selected:",
                            end_node
                        )


                        # ----------------------------------------
                        # Run Dijkstra
                        # ----------------------------------------

                        if (blocked_node != None):

                            run_dijkstra(
                                start_node,
                                end_node,
                                blocked_node[0],
                                blocked_node[1]
                            )


                            (start_node,end_node,distance,path) = load_path(PATH_FILE)

                        elif(blocked_node == None):

                            run_dijkstra(
                                start_node,
                                end_node,
                                -1,-1
                            )

                            (start_node,end_node,distance,path) = load_path(PATH_FILE)

                            
                            
                            print(
                                "Two blocked nodes have not been selected."
                            )


            # ====================================================
            # KEYBOARD
            # ====================================================

            elif event.type == pygame.KEYDOWN:


                # -----------------------------------------------
                # R = RESET
                # -----------------------------------------------

                if event.key == pygame.K_r:

                    start_node = None

                    end_node = None

                    blocked_node = None

                    block_mode = False

                    distance = None

                    path = []

                    print(
                        "Route reset."
                    )


                # -----------------------------------------------
                # N = BLOCK NODE MODE
                # -----------------------------------------------

                elif event.key == pygame.K_n:

                    blocked_node = []

                    block_mode = True

                    print(
                        "Block mode ON."
                    )

                    print(
                        "Select blocked node 1."
                    )


            # ----------------------------------------------------
            # DRAW
            # ----------------------------------------------------

        screen.fill(
            (25, 25, 25)
        )


        # Complete graph
        draw_graph(
            screen,
            graph,
            screen_nodes
        )


        # Shortest path
        draw_path(
            screen,
            path,
            screen_nodes
        )


        # Start
        draw_start(
            screen,
            start_node,
            screen_nodes
        )


        # End
        draw_end(
            screen,
            end_node,
            screen_nodes
        )


        #blocked_node

        draw_blocked(
            screen,blocked_node,
            screen_nodes
        )




        # Information
        draw_information(
            screen,
            font,
            start_node,
            end_node,
            blocked_node,
            distance,
            path
        )


        pygame.display.flip()


        clock.tick(FPS)


    pygame.quit()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()