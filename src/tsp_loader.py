def load_coordinates(file_path):
    coords = []
    with open(file_path, 'r') as f:
        start = False
        for line in f:
            if line.strip() == "NODE_COORD_SECTION":
                start = True
                continue
            if start:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                coords.append((float(parts[1]), float(parts[2])))
    return coords
