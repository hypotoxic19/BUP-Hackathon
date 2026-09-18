def solve(data, directives):

    # ==================================
    # 1. Load input data
    # ==================================

    demand = data.get(
        "demand",
        []
    )

    solar = data.get(
        "solar",
        []
    )


    # If empty input

    if not demand:
        demand = [100] * 24


    if not solar:
        solar = [50] * 24



    # ==================================
    # 2. Convert input into 24 hour data
    # ==================================

    if len(demand) < 24:

        demand = demand + [
            demand[-1]
        ] * (24 - len(demand))


    if len(solar) < 24:

        solar = solar + [
            solar[-1]
        ] * (24 - len(solar))


    demand = demand[:24]

    solar = solar[:24]



    # ==================================
    # 3. Battery configuration
    # ==================================

    battery = 300

    battery_capacity = 500

    minimum_reserve = 100


    max_charge_rate = 100

    max_discharge_rate = 50



    # ==================================
    # 4. Extract AI constraints
    # ==================================

    no_charge_hours = []

    no_discharge_hours = []


    for directive in directives:


        dtype = directive.get(
            "directive_type"
        )


        adjustment = directive.get(
            "structured_adjustment",
            {}
        )


        # Solar reduction

        if dtype == "solar_reduction":


            hours = adjustment.get(
                "hours",
                []
            )


            factor = adjustment.get(
                "factor",
                0
            )


            for h in hours:

                if 0 <= h < 24:

                    solar[h] = solar[h] * (
                        1-factor
                    )



        # Battery reserve

        elif dtype == "minimum_battery_reserve":


            minimum_reserve = adjustment.get(
                "energy_kwh",
                minimum_reserve
            )



        # No charging

        elif dtype == "no_charge_window":


            no_charge_hours.extend(
                adjustment.get(
                    "hours",
                    []
                )
            )



        # No discharge

        elif dtype == "no_discharge_window":


            no_discharge_hours.extend(
                adjustment.get(
                    "hours",
                    []
                )
            )



    # ==================================
    # 5. Optimization
    # ==================================

    plan = []


    for hour in range(24):


        load = demand[hour]

        pv = solar[hour]


        grid = 0

        solar_used = 0

        action = "idle"



        # ------------------------------
        # Solar priority
        # ------------------------------

        if pv >= load:


            solar_used = load


            excess = pv - load



            if hour not in no_charge_hours:


                charge = min(

                    excess,

                    max_charge_rate,

                    battery_capacity - battery

                )


                if charge > 0:

                    battery += charge

                    action = "charge"



        # ------------------------------
        # Solar shortage
        # ------------------------------

        else:


            solar_used = pv


            shortage = load - pv



            if (

                hour not in no_discharge_hours

                and battery > minimum_reserve

            ):


                discharge = min(

                    shortage,

                    max_discharge_rate,

                    battery - minimum_reserve

                )


                battery -= discharge


                shortage -= discharge


                action = "discharge"



            grid = shortage



        plan.append({

            "hour": hour,

            "grid_kwh": round(
                grid,
                2
            ),

            "solar_used_kwh": round(
                solar_used,
                2
            ),

            "battery_action": action,

            "battery_kwh": round(
                battery,
                2
            )

        })


    return plan