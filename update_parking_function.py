from typing import Dict, List, Tuple


def check_limits(centerx: int, centery: int, parking_dict: Dict[str,List[int]]):
    """
    params:
        centerx: x of the car's center
        centery: y of the car's center
    This method checks wether a car is in a parking spot or not
    return:
        The key of the parking spot or None
    """
    for key, value in parking_dict.items():
        x1, y1, x2, y2 = value[0], value[1], value[2], value[3]
        if x1 < centerx < x2 and y1 < centery < y2:
            return key
    return None


def update_parking(results: List[Tuple[int, int]], parking_dict: Dict[str, List[int]]):
    """ 
    params:
        results: List of tuples that contains the centers of cars.
        parking_dict: Dictionary containing parking spot main values
    This method updates the parking_dict
    return:
        A list of occupied parking spots
    """
    centers= []
    for result in results:
        centerx,centery = result 
        centers.append((centerx, centery)) # dibujar el rectángulo del objeto

    for key in parking_dict:
        parking_dict[key][4] = 1 

    spots = []
    for center in centers:
        occupied_spot = check_limits(center[0], center[1], parking_dict)
        spots.append(occupied_spot)
        if occupied_spot:
            parking_dict[occupied_spot][4] = 0

    occupied_spots = list(filter(lambda x: x is not None, spots))
    return occupied_spots, parking_dict



