import random
import copy 
with open("02-swarming-ant.txt") as f: # 00-example.txt, 01-chilling-cat.txt, 02-swarming-ant.txt, 03-input-anti-greedy.txt
    lines = f.read().splitlines()

C, R, S = map(int,lines[0].split())
sneake_len = list(map(int,lines[1].split()))

matrix = [[0 for _ in range(C)] for _ in range(R)]
wormholes_coord = []

for i in range(R):
    l = []
    for j,schifo in enumerate(list(lines[i+2].split())):
        if schifo == "*":
            wormholes_coord.append((i,j))
        l.append(schifo)
    matrix[i] = l


def movimenti_possibili(i,j,move,R,C):
    if move=="R":
        j = (j + 1) % C
    elif move=="L":
        j = (j - 1) % C
    elif move == "D":
        i = (i + 1) % R
    else:
        i = (i - 1) % R


    return i,j



def dfs_path(i,j,len_snake, current_score, current_visited, current_path, best_score, best_visited, best_path):
    if len_snake == 0:
        return (current_path, current_score, current_visited)
    else:

        max_score_next_move = 0
        max_n_i, max_n_j = 0, 0

        wormhole_in_i, wormhole_in_j = 0, 0
        go_through_wormhole = False
        
        best_move = ""
        # Find "best" move 
        for move in ["U", "R", "L", "D"]:
            n_i, n_j = movimenti_possibili(i,j,move,R,C)

            if (n_i, n_j) not in current_visited:

                # Find the "best" exit wormhole to use
                if (n_i, n_j) in wormholes_coord:
                    for move_wormhole in ["U", "R", "L", "D"]:
                        # Don't need and (w_i, w_j) not in visited because multiple snakes can go though the same wormhole
                        for (w_i,w_j) in wormholes_coord:
                            if (w_i, w_j) != (n_i,n_j): 
                                w_n_i, w_n_j = movimenti_possibili(w_i,w_j,move_wormhole,R,C)
                                if (w_n_i, w_n_j) not in current_visited and (w_n_i, w_n_j) not in wormholes_coord:
                                    if int(matrix[w_n_i][w_n_j]) > max_score_next_move:
                                        max_score_next_move = int(matrix[w_n_i][w_n_j])
                                        # Here put the coordinates of the exiting wormhole so we don't miss steps
                                        max_n_i = w_i
                                        max_n_j = w_j
                                        go_through_wormhole = True
                                        best_move = move
                else:    
                    if int(matrix[n_i][n_j]) > max_score_next_move:
                        max_score_next_move = int(matrix[n_i][n_j])
                        max_n_i = n_i
                        max_n_j = n_j
                        best_move = move
                        go_through_wormhole = False
        
        new_current_path = current_path.copy()
        new_current_path.append(best_move)

        n_i, n_j = max_n_i, max_n_j
        
        if go_through_wormhole:
            new_current_path.append(str(n_i))
            new_current_path.append(str(n_j))
            current_visited.add((wormhole_in_i, wormhole_in_j))
    
        current_visited.add((n_i, n_j))      

        tmp_score = 0
        tmp_path = []
        tmp_visited = set()

        if (n_i, n_j) in wormholes_coord:
            # Make sure we don't finish on a wormhole
            if len_snake > 2:                
                tmp_path, tmp_score, tmp_visited = dfs_path(n_i, n_j, len_snake - 1, current_score + 0, current_visited.copy(), new_current_path, best_score, best_visited, best_path)
        else:
            tmp_path, tmp_score, tmp_visited = dfs_path(n_i, n_j, len_snake - 1, current_score + int(matrix[n_i][n_j]) , current_visited.copy(), new_current_path, best_score, best_visited, best_path)
            
        current_visited.remove((n_i, n_j))
        if go_through_wormhole:
            current_visited.remove((wormhole_in_i, wormhole_in_j))
        if tmp_score > best_score:                        
            best_path = tmp_path
            best_visited = tmp_visited
            best_score = tmp_score

        return (best_path, best_score, best_visited)


def best_path(len_snake, visited):
    # heuristic: find the "best" coordinates to start with, by sorting the grid by score
    start_i = random.randint(0,R-1)
    start_j = random.randint(0,C-1)
    while (start_i,start_j) in wormholes_coord or (start_i, start_j) in visited:
        start_i = random.randint(0,R-1)
        start_j = random.randint(0,C-1)
    score = int(matrix[start_i][start_j])
    visited.add((start_i,start_j))    
    path, score, visited = dfs_path(start_i,start_j,len_snake-1,score,current_visited = visited,current_path = [], best_score = 0, best_visited = set(), best_path = [])
    return start_i, start_j, path, score, visited

tot_score = 0
visited = set()
results = []

for i,sneake in enumerate(sneake_len):
    print(i, "/", len(sneake_len))
    start_i, start_j, sneake_path, sneake_score, visited = best_path(sneake, visited)
    if sneake_path != []:
        results.append(str(start_i) + " " + str(start_j) + " " + " ".join(sneake_path))
    else:
        results.append("")
    tot_score += sneake_score
    

print(tot_score)

with open("output.txt","w") as f:
    f.write("\n".join(results))
    