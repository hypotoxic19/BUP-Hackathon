import requests
import json


API_URL = "http://127.0.0.1:8000/optimize-energy"


# Load official sample cases
with open("sample_cases/cases.json") as file:
    data = json.load(file)


cases = data["cases"]


for case in cases:

    print("\n====================")

    scenario_id = case["input"]["scenario_id"]

    print("Running:", scenario_id)


    input_data = case["input"]


    # Convert official GridWise format
    # into your current Django API format

    hours = input_data.get("hours", [])


    payload = {

        "scenario_id": scenario_id,


        "demand": [
            hour["demand_kwh"]
            for hour in hours
        ],


        "solar": [
            hour["solar_kwh"]
            for hour in hours
        ],


        "operator_notes": input_data.get(
            "operator_notes",
            []
        )

    }


    try:

        response = requests.post(

            API_URL,

            json=payload,

            timeout=30

        )


        if response.status_code == 200:


            result = response.json()


            print("SUCCESS")


            # Your current API response format

            if "summary" in result:

                print(
                    "Total Grid:",
                    result["summary"].get(
                        "total_grid_kwh"
                    )
                )


                print(
                    "Total Cost:",
                    result["summary"].get(
                        "total_cost_bdt"
                    )
                )


            else:

                print(
                    "Total Grid:",
                    result.get(
                        "total_grid_kwh"
                    )
                )


                print(
                    "Total Cost:",
                    result.get(
                        "total_cost_bdt"
                    )
                )



        else:

            print(
                "FAILED",
                response.text
            )


    except Exception as e:


        print(
            "ERROR:",
            str(e)
        )