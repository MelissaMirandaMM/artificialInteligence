import heapq
import math
from typing import List, Tuple, Dict, Set
from itertools import permutations

# =============================================
# Definições de Tipos e Constantes (ATUALIZADO)
# =============================================

Position = Tuple[int, int]
Path = List[Position]
TerrainMap = List[List[int]]

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

# Posições importantes no mapa (verificar coordenadas reais)
LINK_START = (0, 0)
LOST_WOODS = (9, 9)
DUNGEONS = {
    1: (9, 0),
    2: (5, 5),
    3: (0, 9)
}

# =============================================
# Implementação do Algoritmo A* (CORRIGIDO)
# =============================================

def heuristic(a: Position, b: Position) -> float:
    """Função heurística (distância de Manhattan)"""
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
        if dungeon:
            return 10  # Custo fixo em masmorras
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
                
            # Verificar se é caminho válido (em masmorras)
            if dungeon and terrain_map[next_pos[0]][next_pos[1]] != 0:
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
    
    return path, cost_so_far.get(goal, float('inf'))

# =============================================
# Funções de Visualização (MELHORADO)
# =============================================

def visualize_path(path: Path, map_size: Tuple[int, int], highlight: Position = None):
 
    grid = [['.' for _ in range(map_size[1])] for _ in range(map_size[0])]
    
    # Marcar pontos importantes
    if highlight:
        x, y = highlight
        grid[x][y] = 'X'
    # Marcar caminho
    for step, pos in enumerate(path):
        x, y = pos
        if grid[x][y] == '.':
            grid[x][y] = "#"
    
    print("\nVisualizacao do caminho:")
    for row in grid:
        print(' '.join(row))

def loading_map(filename):
    map_data = []
    link_position = (0,0)
    pendants_position = (0,0)

    try:
        with open(filename, 'r') as f:
            for row_index, line in enumerate(f):
                lines = line.strip().split(' ')
                process_lines = []

                for col_index, element_str in enumerate(lines):
                    try:
                        element_int = int(element_str)
                        process_lines.append(element_int)

                        if element_int == 9:
                            link_position = (row_index, col_index)
                        elif element_int == 8:
                            pendants_position = (row_index, col_index)

                    except ValueError:
                        print(f"Aviso: Não foi possível converter '{element_str}' para inteiro na linha {row_index}, coluna {col_index}")
                        process_lines.append(11)

                map_data.append(process_lines)

        return map_data, link_position, pendants_position

    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

# =============================================
# Função Principal (ATUALIZADA)
# =============================================
def main():
    print("Iniciando busca pelos Pingentes da Virtude...\n")
    
    # =====================TESTES=================
    hyrule_map, link_start, _ = loading_map("mapMinimal.txt")
    test_path, test_cost = a_star_search(link_start, LOST_WOODS, hyrule_map, COST_MAP)
    visualize_path(test_path, (10, 10), LOST_WOODS)
    print(f"Caminho teste encontrado! Custo: {test_cost}")
    hyrule_map, link_start, pendants_position = loading_map("dungeonMinimal.txt")
    test_path, test_cost = a_star_search(link_start, pendants_position, hyrule_map, COST_MAP)
    visualize_path(test_path, (10, 10), pendants_position)
    print(f"Caminho teste encontrado! Custo: {test_cost}")
    # ============================================

    # dungeon_maps = {
    #     1: loading_map("dungeonMinimal.txt"),
    #     # 2: loading_map(),
    #     # 3: loading_map()
    # }
    
    # 2. Posições dos pingentes dentro das masmorras
    # pendant_positions = {
    #     1: (10, 15),
    #     2: (20, 5),
    #     3: (5, 20)
    # }
    
    # 4. Encontrar o melhor caminho completo
    # print("\nCalculando o melhor caminho completo...")
    # path, total_cost = collect_pendants(
    #     LINK_START,
    #     DUNGEONS,
    #     #pendant_positions,
    #     #dungeon_maps,
    #     hyrule_map,
    #     COST_MAP,
    #     LOST_WOODS
    # )

if __name__ == "__main__":
    main()