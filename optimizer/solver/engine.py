def solve(data, directives):


    # =====================================
    # 1. Input Data
    # =====================================

    demand = data.get(
        "demand",
        []
    )

    solar = data.get(
        "solar",
        []
    )


    if not demand:

        demand = [100] * 24


    if not solar:

        solar = [50] * 24



    # Convert into 24 hours

    if len(demand) < 24:

        demand += [demand[-1]] * (
            24 - len(demand)
        )


    if len(solar) < 24:

        solar += [solar[-1]] * (
            24 - len(solar)
        )


    demand = demand[:24]

    solar = solar[:24]



    # =====================================
    # 2. Time Of Use Electricity Price
    # =====================================

    electricity_price = [

        8, 8, 8, 8,       # 00-03 cheap

        10,10,12,15,      # 04-07

        15,15,12,10,      # 08-11

        10,10,15,15,      # 12-15

        18,18,15,10,      # 16-19 peak

        8,8,8,8           # 20-23 cheap

    ]



    # =====================================
    # 3. Battery Configuration
    # =====================================

    battery = 300

    battery_capacity = 500

    minimum_reserve = 100


    max_charge_rate = 100

    max_discharge_rate = 30



    # =====================================
    # 4. Read AI Directives
    # =====================================

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


        # -------------------------------
        # Solar Reduction
        # -------------------------------

        if dtype == "solar_reduction":


            hours = adjustment.get(
                "hours",
                []
            )


            factor = adjustment.get(
                "factor",
                0
            )


            for hour in hours:


                if 0 <= hour < 24:


                    solar[hour] = (
                        solar[hour]
                        *
                        (1-factor)
                    )



        # -------------------------------
        # Minimum Battery Reserve
        # -------------------------------

        elif dtype == "minimum_battery_reserve":


            minimum_reserve = adjustment.get(
                "energy_kwh",
                minimum_reserve
            )



        # -------------------------------
        # No Charge Window
        # -------------------------------

        elif dtype == "no_charge_window":


            no_charge_hours.extend(

                adjustment.get(
                    "hours",
                    []
                )

            )



        # -------------------------------
        # No Discharge Window
        # -------------------------------

        elif dtype == "no_discharge_window":


            no_discharge_hours.extend(

                adjustment.get(
                    "hours",
                    []
                )

            )



    # =====================================
    # 5. Optimization
    # =====================================

    plan = []



    for hour in range(24):


        load = demand[hour]

        pv = solar[hour]


        grid = 0

        solar_used = 0

        action = "idle"



        current_price = electricity_price[hour]



        # =================================
        # Case 1: Solar is enough
        # =================================

        if pv >= load:


            solar_used = load


            excess = pv - load



            # Charge only in cheap hours

            if (

                hour not in no_charge_hours

                and current_price <= 12

            ):


                charge = min(

                    excess,

                    max_charge_rate,

                    battery_capacity - battery

                )


                if charge > 0:


                    battery += charge

                    action = "charge"



        # =================================
        # Case 2: Solar shortage
        # =================================

        else:


            solar_used = pv


            shortage = load - pv



            # Discharge during expensive hours

            if (

                hour not in no_discharge_hours

                and current_price >= 15

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



        # =================================
        # Store Result
        # =================================

        plan.append({

            "hour":
                hour,


            "electricity_price":
                current_price,


            "grid_kwh":
                round(
                    grid,
                    2
                ),


            "solar_used_kwh":
                round(
                    solar_used,
                    2
                ),


            "battery_action":
                action,


            "battery_kwh":
                round(
                    battery,
                    2
                )

        })



    return plan