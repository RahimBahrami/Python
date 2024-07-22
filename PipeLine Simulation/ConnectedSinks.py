
def inside(i, j, n, m):
    if i >= 0 and i < n and j >= 0 and j < m:
        return True
    return False

def find_point(r, c, row, col):
    n = len(row)
    for i in range(n):
        if row[i] == r and col[i] == c:
            return i
    return -1

def find_type(p, types):
    n = len(types)
    for i in range(n):
        if types[i] == p:
            return i
    return -1

def check_flow(r, c, row, col, rows, cols, pipes, types, check, flow):
    if inside(r, c, rows, cols) and flow[r][c] == 0:
        next_ind = find_point(r, c, row, col)
        p_ind = find_type(pipes[next_ind], types)

        if next_ind != -1 and check[p_ind] == 1:
            return True

    return False
    
def connectedSinks(inputfile):
    types = ['*', u'\u2550', u'\u2551', u'\u2554', u'\u2557', u'\u255a', u'\u255d', u'\u2560', u'\u2563', u'\u2566', u'\u2569']
    left = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1]
    right = [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
    up = [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1]
    down = [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
    
    infile = open(inputfile, 'r', encoding = 'utf-8')
    pipes = []
    row = []
    col = []

    source_row = 0
    source_col = 0

    rows = 0
    cols = 0

    for p in infile:
        token = p.split()
        pipes.append(token[0])
        r = int(token[2])
        c = int(token[1])
        rows = max(rows, r)
        cols = max(cols, c)
        row.append(r)
        col.append(c)
        if token[0] == '*':
            source_row = r
            source_col = c    

    rows = rows + 1
    cols = cols + 1
    n = len(pipes)
    flow = []
    sinks = []
    
    
    for i in range(rows):
        empty_flow = []

        for j in range(cols):
            empty_flow.append(0)
        flow.append(empty_flow)

    for i in range(rows - 1, 0, -1):
        for j in range(cols):
            ind = find_point(i, j, row, col)
            if ind == -1:
                print('', end = ' ')
            else:
                print(pipes[ind], end = '')
        print('')
    
    queue_row = [source_row]
    queue_col = [source_col]

    flow[source_row][source_col] = 1
    
    while len(queue_row) != 0:
        cur_row = queue_row[0]
        cur_col = queue_col[0]

        ind = find_point(cur_row, cur_col, row, col)

        if ind != -1 and pipes[ind].isupper():
            sinks.append(pipes[ind])
            pipes[ind] = '*'
        
        #print('row = ' + str(cur_row) + ', col = ' + str(cur_col) + ', pipe = ' + pipes[ind])

        #left
        p_ind = types.index(pipes[ind])
        if ind != -1 and left[p_ind] == 1:
            next_row = cur_row
            next_col = cur_col - 1

            fsw = check_flow(next_row, next_col, row, col, rows, cols, pipes, types, right, flow)
            if fsw:
                flow[next_row][next_col] = 1
                queue_row.append(next_row)
                queue_col.append(next_col)

        #right
        p_ind = types.index(pipes[ind])
        if ind != -1 and right[p_ind] == 1:
            next_row = cur_row
            next_col = cur_col + 1

            fsw = check_flow(next_row, next_col, row, col, rows, cols, pipes, types, left, flow)
            if fsw:
                flow[next_row][next_col] = 1
                queue_row.append(next_row)
                queue_col.append(next_col)

        #up
        p_ind = types.index(pipes[ind])
        if ind != -1 and up[p_ind] == 1:
            next_row = cur_row + 1
            next_col = cur_col

            fsw = check_flow(next_row, next_col, row, col, rows, cols, pipes, types, down, flow)
            if fsw:
                flow[next_row][next_col] = 1
                queue_row.append(next_row)
                queue_col.append(next_col)
        
        #down
        p_ind = types.index(pipes[ind])
        if ind != -1 and down[p_ind] == 1:
            next_row = cur_row - 1
            next_col = cur_col

            fsw = check_flow(next_row, next_col, row, col, rows, cols, pipes, types, up, flow)
            if fsw:
                flow[next_row][next_col] = 1
                queue_row.append(next_row)
                queue_col.append(next_col)

        queue_row.pop(0)
        queue_col.pop(0)

    sinks.sort()
    result = ''
    for s in sinks:
        result = result + s

    #print(result)
    return result

#main
print(connectedSinks('connect.txt'))
