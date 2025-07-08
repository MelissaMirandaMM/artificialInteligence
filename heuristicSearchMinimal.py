import heapq
import math
import time
import os
from typing import List, Tuple, Dict, Set
from itertools import permutations

# =============================================
# Definições de Tipos e Constantes (ATUALIZADO)
# =============================================

Position = Tuple[int, int]
Path = List[Position]
TerrainMap = List[List[int]]

# Tamanho do mapa
MAP_SIZE = (10, 10)

# Tipos de terreno no mapa principal
GRAMA = 0
AREIA = 1
FLORESTA = 2
MONTANHA = 3
AGUA = 4
WALL = 5

DANGEON = 7
PENDANT = 8
LINK = 9

# Custo de movimento para cada terreno
COST_MAP = {
    GRAMA: 10,
    AREIA: 20,
    FLORESTA: 100,
    MONTANHA: 150,
    AGUA: 180,
    WALL: float('inf'),

    DANGEON: 0,
    PENDANT: 0,
    LINK: 0,
}

# =============================================
# Implementação do Algoritmo A* (CORRIGIDO)
# =============================================

def heuristic(a: Position, b: Position) -> float:
    """Função heurística (distância de Manhattan)"""
    """a posição atual e b é o objetivo"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(
    start: Position,
    goal: Position,
    terrain_map: TerrainMap,
    cost_map: Dict[int, int],
    dungeon: bool = False
) -> Tuple[Path, int]:
    """Implementação corrigida do algoritmo A*"""
    
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

def visualize_step_by_step(path: Path, cost, map_size: Tuple[int, int]):
    grid = [['.' for _ in range(map_size[1])] for _ in range(map_size[0])]
    
    # Marcar pontos importantes
    x, y = path[0]
    grid[x][y] = 'S'
    x, y = path[-1]
    grid[x][y] = 'X'

    # Marcar caminho
    print("\nVisualizacao do caminho:")
    for pos in path:
        os.system('cls')
        x, y = pos
        if grid[x][y] == '.':
            grid[x][y] = "#"
        for row in grid:
            print(' '.join(row))
        print("Custo atual:", cost.get(pos, float('inf')))
        time.sleep(0.1)
        
    
def loading_map(filename):
    map_data = []
    link_position = Position
    pendants_position = Position
    dungeon_position = Position

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
                        elif element_int == 7: # Pingente
                            dungeon_position = (row_index, col_index)

                    except ValueError:
                        print(f"Aviso: Não foi possível converter '{element_str}' para inteiro na linha {row_index}, coluna {col_index}")
                        process_lines.append(11)

                map_data.append(process_lines)

        return map_data, link_position, dungeon_position, pendants_position

    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

def main():
    print("Iniciando busca pelos Pingentes da Virtude...\n")
    # =====================TESTES=================
    hyrule_map, link_start, dungeon_position, _ = loading_map("mapMinimal.txt")
    test_path, test_cost = a_star_search(link_start, dungeon_position, hyrule_map, COST_MAP)
    visualize_step_by_step(test_path, test_cost, MAP_SIZE)
    print(f"Caminho teste encontrado! Custo total: {test_cost.get(dungeon_position, float('inf'))}")
    # ============================================

if __name__ == "__main__":
    main()