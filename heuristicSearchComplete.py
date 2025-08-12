import heapq
from typing import List, Tuple, Dict, Set
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np

Position = Tuple[int, int]
Path = List[Position]
TerrainMap = List[List[int]]

# Tamanho do mapa
MAIN_MAP_SIZE = (42, 42)
DUNGEON_MAP_SIZE = (28, 28)

# Tipos de terreno nos mapas
GRASS = 0
SAND = 1
FOREST = 2
MOUNTAIN = 3
WATER = 4
WAY = 5
WALL = 6

# Pontos importantes nos mapas
DANGEON = 7
PENDANT = 8
LINK = 9
LOSTWOOD = 11
SWORD = 12

# Custo de movimento para cada terreno
COST_MAP = {
    GRASS: 10,
    SAND: 20,
    FOREST: 100,
    MOUNTAIN: 150,
    WATER: 180,

    WAY: 10,
    WALL: float('inf'),

    DANGEON: 0,
    PENDANT: 0,
    LINK: 0,
    LOSTWOOD: 0,
    SWORD: 0
}

# Funcao heuristica (distância de Manhattan)
def heuristic(a: Position, b: Position) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(
    start: Position,
    goal: Position,
    terrain_map: TerrainMap,
    cost_map: Dict[int, int]
) -> Tuple[Path, dict[Position, int]]:
    
    # Função para obter custo de movimento
    def get_move_cost(pos: Position) -> int:
        terrain_type = terrain_map[pos[0]][pos[1]]
        return cost_map.get(terrain_type, float('inf'))  # Retorna infinito para terrenos inválidos
    
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    
    while frontier:
        _, current = heapq.heappop(frontier)
        
        if current == goal:
            break
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)
            
            # Verificar limites do mapa
            if (next_pos[0] < 0 or next_pos[0] >= len(terrain_map) or
                next_pos[1] < 0 or next_pos[1] >= len(terrain_map[0])):
                continue
                
            # Calcular novo custo
            move_cost = get_move_cost(next_pos)
            if move_cost == float('inf'):
                continue  # Terreno intransitável
                
            new_cost = cost_so_far[current] + move_cost
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current
                
    # Reconstruir caminho
    if goal not in came_from:
        return [], float('inf')  # Caminho não encontrado
        
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, cost_so_far

def plot_map(map_data: TerrainMap, map_size: Tuple[int, int], path: Path = None, cost: dict[Position, int] = {}, total_cost: int = 0):

    color_map = {
        GRASS: [0.55, 0.8, 0.3],
        SAND: [0.77, 0.75, 0.6],
        FOREST: [0.1, 0.55, 0.1],
        MOUNTAIN: [0.4, 0.35, 0.15],
        WATER: [0.33, 0.55, 0.83],
        DANGEON: [0.12, 0.12, 0.12], 
        LINK: [0.85, 0.5, 0.3],

        WAY: [1.0, 0.9, 0.9],
        WALL: [0.7, 0.7, 0.7],
        PENDANT: [1, 1, 0],
        LOSTWOOD: [0.8, 0.8, 0],
        SWORD: [0.8, 0.2, 0.2]
    }
    
    rows, cols = map_size
    grid = np.zeros((rows, cols, 3))

    for r in range(rows):
        for c in range(cols):
            terrain_type = map_data[r][c]
            grid[r, c] = color_map.get(terrain_type, [0.5, 0.5, 0.5])

            if(terrain_type == 9):
                grid[r, c] = [0.5, 0.5, 0.8]
            
    plt.ion()

    # --------- CONFIGURACOES DO PLOT --------
    fig, ax = plt.subplots(figsize=(10, 10))
    mng = plt.get_current_fig_manager()
    if mng is not None:
        mng.full_screen_toggle() 
    fig.subplots_adjust(top=1, bottom=0, left=0, right=1, wspace=0, hspace=0)
    im = ax.imshow(grid)
    # ----------------------------------------
    # --------- LINHAS PARA AS BORDAS --------
    ax.set_xticks(np.arange(-.5, cols, 1))
    ax.set_yticks(np.arange(-.5, rows, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    ax.grid(which='major', color='black', linestyle='-', linewidth=1)
    # ----------------------------------------
    # --------------- Custo ------------------
    curent_cost_text = ax.text(-0.015, 0.98, 'Custo: 0', ha='right', va='top', color='white', fontsize=16, weight='bold', 
        bbox=dict(facecolor='black', alpha=0.7, edgecolor='none'),
        transform=ax.transAxes)
    total_cost_text = ax.text(-0.015, 0.94, 'Custo: 0', ha='right', va='top', color='white', fontsize=16, weight='bold', 
        bbox=dict(facecolor='black', alpha=0.7, edgecolor='none'),
        transform=ax.transAxes)
    # ----------------------------------------

    plt.draw()
    # plt.waitforbuttonpress() 

    if path:
        grid[path[0]] = [1, 1, 1]
        for r, c in path: # Move o link

            curent_cost_text.set_text(f'Custo do caminho: {cost.get((r, c))}')
            total_cost_text.set_text(f'Custo total: {total_cost + cost.get((r, c))}')

            current_grid = np.copy(grid)
            current_grid[r, c] = color_map.get(LINK)

            im.set_data(current_grid)
            fig.canvas.draw_idle()
            # plt.pause(0.5)

        for r, c in path: # Pinta o caminho percorrido
            grid[r, c] = color_map.get(LINK)

        im.set_data(grid)
        fig.canvas.draw_idle()
        plt.pause(2)
        # plt.waitforbuttonpress()
        
    plt.ioff()
    plt.close(fig)

def loading_map(filename):
    map_data = []
    link_position = Position
    pendants_position = Position
    lostWoods_position = Position
    dungeons_position = []

    try:
        with open(filename, 'r') as f:
            for row_index, line in enumerate(f):
                lines = line.strip().split(' ')
                process_lines = []

                for col_index, element_str in enumerate(lines):
                    try:
                        element_int = int(element_str)
                        process_lines.append(element_int)

                        if element_int == 9: # Link
                            link_position = (row_index, col_index)
                        elif element_int == 8: # Pingente
                            pendants_position = (row_index, col_index)
                        elif element_int == 7: # Masmorra
                            dungeons_position.append((row_index, col_index))
                        elif element_int == 11: #Lost Wood
                            lostWoods_position = (row_index, col_index)

                    except ValueError:
                        print(f"Não foi possível converter '{element_str}' para inteiro na linha {row_index}, coluna {col_index}")
                        process_lines.append(22)

                map_data.append(process_lines)
        
        dungeons_position.reverse()
        dungeons_position.append(lostWoods_position)        
        return map_data, link_position, dungeons_position, pendants_position

    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

def main():
    total_cost = 0
    main_map_data, link_position, dungeons_position, _ = loading_map("mainMap.txt")

    for i, dungeon in enumerate(dungeons_position, start=1):
        # Encontra o caminho do Link até a masmorra atual no mapa principal usando A*
        test_path, test_cost = a_star_search(link_position, dungeon, main_map_data, COST_MAP)
        
        if test_path:
            # Plota o mapa principal com o caminho encontrado até a masmorra
            plot_map(main_map_data, MAIN_MAP_SIZE, test_path, test_cost, total_cost)
            # Adiciona o custo de alcançar a masmorra ao custo total
            total_cost += test_cost.get(dungeon)
        else:
            print(f"Não foi possível encontrar um caminho para a masmorra {i}.")
            break

        if i < 4:
            # Pergunta ao usuário se deseja prosseguir para dentro da masmorra (S/N)
            proceed = input(f"Caminho para a Masmorra {i} encontrado. Deseja prosseguir para a masmorra? (S/N): ").strip().upper()
            if proceed == 'S': # Altera a condição para 'S'
                # Se o usuário confirmar, carrega os dados do mapa da masmorra correspondente
                dungeon_map_data, link_position_dungeon, _, pendants_position = loading_map(f"dungeonMap{i}.txt")
                if dungeon_map_data:
                    # Encontra o caminho dentro da masmorra até o pingente
                    test_path_dungeon, test_cost_dungeon = a_star_search(link_position_dungeon, pendants_position, dungeon_map_data, COST_MAP)
                    if test_path_dungeon:
                        # Plota o mapa da masmorra com o caminho até o pingente
                        plot_map(dungeon_map_data, DUNGEON_MAP_SIZE, test_path_dungeon, test_cost_dungeon, total_cost)
                        # Adiciona o custo de alcançar o pingente ao custo total
                        total_cost += test_cost_dungeon.get(pendants_position)
                    else:
                        print(f"Não foi possível encontrar um caminho para o pingente na masmorra {i}.")
                        break
                else:
                    print(f"Não foi possível carregar o arquivo dungeonMap{i}.txt.")
                    break
            else:
                print("Jornada abortada.")
                break
        
        # Atualiza a posição do Link para a masmorra atual para a próxima etapa da jornada
        link_position = dungeon 

    print(f"Caminho encontrado! Custo total: {total_cost}")
    return

if __name__ == "__main__":
    main()