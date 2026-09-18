def check_battery(
        battery,
        capacity,
        reserve
):

    if battery > capacity:

        return False


    if battery < reserve:

        return False


    return True



def check_grid_limit(
        grid,
        maximum
):

    if grid > maximum:

        return False


    return True