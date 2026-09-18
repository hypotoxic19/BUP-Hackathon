def calculate_cost(plan, price=12):

    total_cost = 0

    for item in plan:

        total_cost += (
            item["grid_kwh"] * price
        )

    return round(total_cost, 2)



def calculate_solar_utilization(plan):

    solar_used = 0
    total_solar = 0


    for item in plan:

        solar_used += item["solar_used_kwh"]


    if total_solar == 0:
        return 0


    return round(
        (solar_used / total_solar) * 100,
        2
    )