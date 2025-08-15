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
    cost_map: Dict[int, int],
    dungeon: bool = False  
) -> Tuple[Path, dict[Position, int]]:
    
    # Função para obter custo de movimento
    def get_move_cost(pos: Position) -> int:
        terrain_type = terrain_map[pos[0]][pos[1]]
        return cost_map.get(terrain_type, float('inf'))
    
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

def plot_map(map_data: TerrainMap, map_size: Tuple[int, int], path: Path = None, 
             cost: dict[Position, int] = {}, total_cost: int = 0):
    
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
            if terrain_type == SWORD:
                grid[r, c] = color_map[SWORD]
            elif terrain_type == LINK:
                grid[r, c] = color_map[LINK]
            else:
                grid[r, c] = color_map.get(terrain_type, [0.5, 0.5, 0.5])
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 12))
    mng = plt.get_current_fig_manager()
    if mng is not None:
        mng.full_screen_toggle() 
    
    # Configurações do plot
    plt.title('Jornada de Link', pad=20, fontsize=16, weight='bold')
    fig.subplots_adjust(top=0.9, bottom=0.15, left=0.1, right=0.75)
    
    # Adicionar legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Link (Início)', 
                  markerfacecolor=color_map[LINK], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Master Sword (Objetivo)', 
                  markerfacecolor=color_map[SWORD], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Pingente da Virtude', 
                  markerfacecolor=color_map[PENDANT], markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Lost Woods', 
                  markerfacecolor=color_map[LOSTWOOD], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Grama (Custo: 10)', 
                  markerfacecolor=color_map[GRASS], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Areia (Custo: 20)', 
                  markerfacecolor=color_map[SAND], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Floresta (Custo: 100)', 
                  markerfacecolor=color_map[FOREST], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Montanha (Custo: 150)', 
                  markerfacecolor=color_map[MOUNTAIN], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Água (Custo: 180)', 
                  markerfacecolor=color_map[WATER], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Masmorra', 
                  markerfacecolor=color_map[DANGEON], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Caminho (Masmorra)', 
                  markerfacecolor=color_map[WAY], markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Parede (Intransponível)', 
                  markerfacecolor=color_map[WALL], markersize=10)
    ]
    
    ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), 
              loc='upper left', borderaxespad=0., title="Legenda:")
    
    # Linhas para as bordas
    ax.set_xticks(np.arange(-.5, cols, 1))
    ax.set_yticks(np.arange(-.5, rows, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    ax.grid(which='major', color='black', linestyle='-', linewidth=1)
    
    # Textos de custo
    current_cost_text = ax.text(-0.015, 0.98, 'Custo Atual: 0', ha='right', va='top', 
                               color='white', fontsize=14, weight='bold', 
                               bbox=dict(facecolor='black', alpha=0.8, edgecolor='white', boxstyle='round,pad=0.5'))
    
    total_cost_text = ax.text(-0.015, 0.94, 'Custo Total: 0', ha='right', va='top', 
                             color='white', fontsize=14, weight='bold', 
                             bbox=dict(facecolor='black', alpha=0.8, edgecolor='white', boxstyle='round,pad=0.5'))
    
    # Barra de progresso
    progress_text = ax.text(0.5, -0.05, 'Preparando jornada...', ha='center', va='top', 
                           color='black', fontsize=12, weight='bold',
                           transform=ax.transAxes)
    
    # Mostrar mapa inicial
    im = ax.imshow(grid)
    fig.canvas.draw_idle()
    plt.pause(0.5)

    if path:
        # Mostrar caminho sendo percorrido
        for i, (r, c) in enumerate(path):
            current_grid = np.copy(grid)
            
            # Atualizar posição do Link
            current_grid[r, c] = color_map[LINK]
            
            # Desenhar caminho com gradiente
            for step, (pr, pc) in enumerate(path[:i]):
                intensity = 0.5 + 0.5*(step/i) if i > 0 else 1
                current_grid[pr, pc] = np.clip(np.array(color_map[LINK]) * intensity, 0, 1)
            
            # Atualizar custos
            current_cost = cost.get((r, c), 0)
            current_cost_text.set_text(f'Custo Atual: {current_cost}')
            total_cost_text.set_text(f'Custo Total: {total_cost + current_cost}')
            
            # Atualizar progresso
            progress = (i+1)/len(path)*100
            progress_text.set_text(f'Progresso: {progress:.1f}% - Etapa {i+1}/{len(path)}')
            
            # Atualizar visualização
            im.set_data(current_grid)
            fig.canvas.draw_idle()
            plt.pause(0.1)
        
        # Mostrar caminho completo no final
        for r, c in path:
            grid[r, c] = color_map[LINK]
        
        im.set_data(grid)
        fig.canvas.draw_idle()
        plt.pause(2)
    
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
    
    # Encontra a posição da Master Sword (12)
    sword_position = None
    for i in range(len(main_map_data)):
        for j in range(len(main_map_data[0])):
            if main_map_data[i][j] == SWORD:  # 12 representa a Master Sword
                sword_position = (i, j)
                break
        if sword_position:
            break

    if not sword_position:
        print("Posição da Master Sword não encontrada no mapa!")
        return

    # Coletar pingentes nas 3 masmorras (excluindo Lost Woods da lista)
    for i, dungeon in enumerate(dungeons_position[:3], start=1):  # Pega apenas as 3 primeiras posições
        # Encontra caminho até a masmorra
        test_path, test_cost = a_star_search(link_position, dungeon, main_map_data, COST_MAP)
        
        if test_path:
            plot_map(main_map_data, MAIN_MAP_SIZE, test_path, test_cost, total_cost)
            total_cost += test_cost.get(dungeon, 0)
        else:
            print(f"Não foi possível encontrar caminho para a Masmorra {i}.")
            return

        # Entrar na masmorra
        proceed = input(f"Caminho para Masmorra {i} encontrado. Entrar na masmorra? (S/N): ").strip().upper()
        if proceed != 'S':
            print("Jornada abortada pelo herói.")
            return

        dungeon_map_data, link_position_dungeon, _, pendant_pos = loading_map(f"dungeonMap{i}.txt")
        if not dungeon_map_data:
            print(f"Erro ao carregar mapa da Masmorra {i}.")
            return

        # Caminho até o pingente
        pendant_path, pendant_cost = a_star_search(link_position_dungeon, pendant_pos, dungeon_map_data, COST_MAP)
        if pendant_path:
            plot_map(dungeon_map_data, DUNGEON_MAP_SIZE, pendant_path, pendant_cost, total_cost)
            total_cost += pendant_cost.get(pendant_pos, 0)
        else:
            print(f"Não foi possível encontrar o pingente na Masmorra {i}.")
            return

        # Voltar para entrada da masmorra
        exit_path, exit_cost = a_star_search(pendant_pos, link_position_dungeon, dungeon_map_data, COST_MAP)
        if exit_path:
            plot_map(dungeon_map_data, DUNGEON_MAP_SIZE, exit_path, exit_cost, total_cost)
            total_cost += exit_cost.get(link_position_dungeon, 0)
        else:
            print(f"Não foi possível sair da Masmorra {i}.")
            return

        # Atualiza posição do Link para a entrada da masmorra
        link_position = dungeon

    # 1. Primeiro ir para Lost Woods (11)
    lost_woods_pos = None
    for i in range(len(main_map_data)):
        for j in range(len(main_map_data[0])):
            if main_map_data[i][j] == LOSTWOOD:
                lost_woods_pos = (i, j)
                break
        if lost_woods_pos:
            break

    if not lost_woods_pos:
        print("Posição de Lost Woods não encontrada no mapa!")
        return

    # Caminho até Lost Woods
    lw_path, lw_cost = a_star_search(link_position, lost_woods_pos, main_map_data, COST_MAP)
    if lw_path:
        plot_map(main_map_data, MAIN_MAP_SIZE, lw_path, lw_cost, total_cost)
        total_cost += lw_cost.get(lost_woods_pos, 0)
    else:
        print("Não foi possível encontrar caminho para Lost Woods.")
        return

    # 2. Depois ir da Lost Woods até a Master Sword (12)
    sword_path, sword_cost = a_star_search(lost_woods_pos, sword_position, main_map_data, COST_MAP)
    if sword_path:
        plot_map(main_map_data, MAIN_MAP_SIZE, sword_path, sword_cost, total_cost)
        total_cost += sword_cost.get(sword_position, 0)
        
        # Saída final
        print("\n=== MISSÃO CUMPRIDA ===")
        print(f"Todos os pingentes foram coletados!")
        print(f"Master Sword obtida em {sword_position}")
        print(f"Custo total da jornada: {total_cost}")
        print("O Reino de Hyrule está salvo!\n")
    else:
        print("Não foi possível encontrar caminho da Lost Woods para a Master Sword.")
        
if __name__ == "__main__":
    main()