VALID_DIRECTIVES = [

    "solar_reduction",
    "minimum_battery_reserve",
    "no_charge_window",
    "no_discharge_window",
    "max_grid_window",
    "no_op"

]


def validate_directive(directive):


    # Check type exists

    if "type" not in directive:
        return False, "Missing directive type"



    # Check supported type

    if directive["type"] not in VALID_DIRECTIVES:
        return False, "Unsupported directive"



    directive_type = directive["type"]



    # Solar reduction validation

    if directive_type == "solar_reduction":

        factor = directive.get("factor")


        if factor is None:
            return False, "Missing solar factor"


        if factor < 0 or factor > 1:
            return False, "Factor must be between 0 and 1"



    # Battery reserve validation

    if directive_type == "minimum_battery_reserve":

        energy = directive.get("energy_kwh")


        if energy is None:
            return False, "Missing battery reserve"



        if energy < 0:
            return False, "Invalid battery value"



    return True, "Valid"