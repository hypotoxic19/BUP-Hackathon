from rest_framework.decorators import api_view
from rest_framework.response import Response

from .llm.llm_client import ask_llm
from .llm.validator import validate_directive

from .solver.engine import solve



@api_view(['GET'])
def health(request):

    return Response({
        "status": "ok"
    })



@api_view(['POST'])
def optimize_energy(request):

    data = request.data


    # -----------------------------
    # 1. Convert operator notes
    #    into structured directives
    # -----------------------------

    directives = []


    notes = data.get(
        "operator_notes",
        []
    )


    for index, note in enumerate(notes):

        result = ask_llm(note)


        valid, message = validate_directive(result)


        directives.append({

            "note_index": index,

            "original_note": note,

            "valid": valid,

            "validation_message": message,

            "directive_type": result.get(
                "type",
                "no_op"
            ),

            "structured_adjustment": result

        })



    # -----------------------------
    # 2. Optimization Engine
    # -----------------------------

    plan = solve(
        data,
        directives
    )



    # -----------------------------
    # 3. Summary calculation
    # -----------------------------

    total_grid = sum(
        item["grid_kwh"]
        for item in plan
    )


    peak_grid = max(
        item["grid_kwh"]
        for item in plan
    )



    electricity_price = 12


    total_cost = (
        total_grid *
        electricity_price
    )



    # -----------------------------
    # 4. Final Response
    # -----------------------------

    return Response({

        "scenario_id":
            data.get("scenario_id"),


        "directive_interpretation":
            directives,


        "hourly_plan":
            plan,


        "summary": {

            "total_grid_kwh":
                total_grid,


            "electricity_cost_bdt":
                total_cost,


            "peak_grid_kwh":
                peak_grid

        },


        "message":
            "Optimization completed successfully"

    })