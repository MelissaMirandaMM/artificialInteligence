import heapq
import math
from typing import List, Tuple, Dict, Set
from itertools import permutations
import matplotlib.pyplot as plt
import numpy as np

# =============================================
# Definições de Tipos e Constantes
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

# Custo de movimento para cada terreno
COST_MAP = {
    GRAMA: 10,
    AREIA: 20,
    FLORESTA: 100,
    MONTANHA: 150,
    AGUA: 180
}

# Posições importantes no mapa (verificar coordenadas reais)
LINK_START = (25, 28)
LOST_WOODS = (7, 6)
DUNGEONS = {
    1: (6, 33),
    2: (40, 18),
    3: (25, 2)
}

# =============================================
# Implementação do Algoritmo A*
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
    """Implementação do algoritmo A*"""
    
    def get_move_cost(pos: Position) -> int:
        if dungeon:
            return 10  # Custo fixo nas masmorras
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
            
            if (next_pos[0] < 0 or next_pos[0] >= len(terrain_map) or
                next_pos[1] < 0 or next_pos[1] >= len(terrain_map[0])):
                continue
            
            if dungeon and terrain_map[next_pos[0]][next_pos[1]] != 0:
                continue
            
            move_cost = get_move_cost(next_pos)
            if move_cost == float('inf'):
                continue  # Terreno intransitável
            
            new_cost = cost_so_far[current] + move_cost
            
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic(next_pos, goal)
                heapq.heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current
                
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
# Estratégia para Coletar Pingentes
# =============================================

def collect_pendants(
    start: Position,
    dungeons: Dict[int, Position],
    pendant_positions: Dict[int, Position],
    dungeon_maps: Dict[int, TerrainMap],
    hyrule_map: TerrainMap,
    cost_map: Dict[int, int],
    lost_woods: Position
) -> Tuple[Path, int]:
    """Função para coletar os pingentes da virtude e ir para Lost Woods"""
    
    best_order = None
    best_cost = float('inf')
    best_path = []
    
    dungeon_entrances = {
        1: (14, 14),
        2: (14, 14),
        3: (14, 14)
    }
    
    for order in permutations(dungeons.keys()):
        temp_path = []
        temp_cost = 0
        temp_pos = start
        valid_path = True
        
        for dungeon_id in order:
            path, cost = a_star_search(temp_pos, dungeons[dungeon_id], hyrule_map, cost_map)
            if not path:
                valid_path = False
                break
            temp_path.extend(path)
            temp_cost += cost
            temp_pos = dungeons[dungeon_id]
            
            entrance = dungeon_entrances[dungeon_id]
            pendant_pos = pendant_positions[dungeon_id]
            
            path, cost = a_star_search(entrance, pendant_pos, dungeon_maps[dungeon_id], cost_map, True)
            if not path:
                valid_path = False
                break
            temp_path.extend(path)
            temp_cost += cost
            temp_pos = pendant_pos
            
            path, cost = a_star_search(temp_pos, entrance, dungeon_maps[dungeon_id], cost_map, True)
            if not path:
                valid_path = False
                break
            temp_path.extend(path)
            temp_cost += cost
            temp_pos = entrance
        
        if not valid_path:
            continue
        
        path, cost = a_star_search(temp_pos, lost_woods, hyrule_map, cost_map)
        if not path:
            continue
            
        temp_cost += cost
        temp_path.extend(path)
        
        if temp_cost < best_cost:
            best_cost = temp_cost
            best_order = order
            best_path = temp_path
    
    if best_order is None:
        print("Erro: Não foi possível encontrar um caminho válido!")
        return [], float('inf')
    
    return best_path, best_cost
def create_connected_dungeon_map() -> TerrainMap:
    """Cria um mapa de masmorra conectado"""
    dungeon_map = [[0 for _ in range(28)] for _ in range(28)]
    
    # Adicionar paredes nas bordas
    for i in range(28):
        dungeon_map[i][0] = 1
        dungeon_map[i][27] = 1
    for j in range(28):
        dungeon_map[0][j] = 1
        dungeon_map[27][j] = 1
    
    # Adicionar alguns obstáculos, mas mantendo caminhos
    for i in range(10, 18):
        dungeon_map[i][10] = 1
    for j in range(5, 20):
        dungeon_map[15][j] = 1
    
    # Garantir que o pingente está acessível
    dungeon_map[10][15] = 0
    dungeon_map[20][5] = 0
    dungeon_map[5][20] = 0
    
    return dungeon_map

# =============================================
# Funções de Visualização
# =============================================

def plot_map(map_data: TerrainMap, map_size: Tuple[int, int], path: Path = None, highlight: Position = None):
    """Visualiza o mapa com diferentes cores para terrenos e o caminho percorrido"""
    color_map = {
        GRAMA: [0.1, 0.8, 0.1],  # Verde claro
        AREIA: [0.9, 0.8, 0.5],  # Amarelo claro
        FLORESTA: [0.1, 0.5, 0.1],  # Verde escuro
        MONTANHA: [0.6, 0.3, 0.1],  # Marrom
        AGUA: [0.1, 0.2, 0.8]  # Azul
    }
    
    grid = np.zeros((map_size[0], map_size[1], 3))  # Mapa colorido
    for i in range(map_size[0]):
        for j in range(map_size[1]):
            terrain_type = map_data[i][j]
            grid[i, j] = color_map.get(terrain_type, [1, 1, 1])  # Usar branco para terrenos inválidos
    
    if path:
        for idx, (x, y) in enumerate(path):
            grid[x, y] = [1, 0, 0]  # Vermelho para o caminho
        
    if highlight:
        x, y = highlight
        grid[x, y] = [1, 1, 0]  # Amarelo para destacar Lost Woods
    
    plt.imshow(grid)
    plt.title("Mapa de Hyrule com o Caminho Percorrido")
    plt.axis('off')
    plt.show()
def create_connected_hyrule_map() -> TerrainMap:
    """Cria um mapa principal de Hyrule conectado"""
    hyrule_map = [[GRAMA for _ in range(42)] for _ in range(42)]
    
    # Adicionar alguns terrenos diferentes, mas garantindo caminhos
    for i in range(42):
        for j in range(42):
            # Criar alguns obstáculos, mas mantendo caminhos conectados
            if 10 <= i < 20 and 10 <= j < 20:
                hyrule_map[i][j] = AREIA
            elif 30 <= i < 40 and 5 <= j < 15:
                hyrule_map[i][j] = FLORESTA
            elif i == 20 or j == 20:  # Criar corredores
                hyrule_map[i][j] = GRAMA
    
    # Garantir que as masmorras estão acessíveis
    for dungeon_pos in DUNGEONS.values():
        x, y = dungeon_pos
        hyrule_map[x][y] = GRAMA
        # Criar caminho até a masmorra
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 42 and 0 <= ny < 42:
                hyrule_map[nx][ny] = GRAMA
    
    return hyrule_map

# =============================================
# Função Principal
# =============================================

def main():
    print("Iniciando busca pelos Pingentes da Virtude...\n")
    
    hyrule_map = create_connected_hyrule_map()
    dungeon_maps = {
        1: create_connected_dungeon_map(),
        2: create_connected_dungeon_map(),
        3: create_connected_dungeon_map()
    }
    
    pendant_positions = {
        1: (10, 15),
        2: (20, 5),
        3: (5, 20)
    }
    
    test_path, test_cost = a_star_search(LINK_START, LOST_WOODS, hyrule_map, COST_MAP)
    if test_path:
        print(f"Caminho teste encontrado! Custo: {test_cost}")
        plot_map(hyrule_map, (42, 42), test_path, LOST_WOODS)
    else:
        print("Erro: Não foi possível encontrar caminho teste!")
        return
    
    path, total_cost = collect_pendants(
        LINK_START,
        DUNGEONS,
        pendant_positions,
        dungeon_maps,
        hyrule_map,
        COST_MAP,
        LOST_WOODS
    )
    
    if path:
        print(f"\nCaminho encontrado com custo total: {total_cost}")
        print(f"Total de passos: {len(path)}")
        visualize_input = input("\nDeseja visualizar o caminho completo? (S/N): ").strip().upper()
        if visualize_input == 'S':
            plot_map(hyrule_map, (42, 42), path, LOST_WOODS)
    else:
        print("\nErro: Não foi possível encontrar um caminho válido!")

if __name__ == "__main__":
    main()
