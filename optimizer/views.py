from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .serializers import EnergyRequestSerializer


from .llm.llm_client import ask_llm
from .llm.validator import validate_directive

from .solver.engine import solve

from django.shortcuts import render
def dashboard(request):

    return render(
        request,
        "dashboard.html"
    )

@api_view(['GET'])
def home(request):

    return Response({

        "project":
        "GridWise LLM",

        "status":
        "running",

        "apis":[
            "/health",
            "/optimize-energy"
        ]

    })



@api_view(['GET'])
def health(request):

    return Response({

        "status":"ok"

    })



@api_view(['POST'])
def optimize_energy(request):


    serializer = EnergyRequestSerializer(
        data=request.data
    )


    if not serializer.is_valid():

        return Response(

            {
                "error":
                serializer.errors
            },

            status=status.HTTP_400_BAD_REQUEST

        )



    data = serializer.validated_data



    directives=[]



    for note in data.get(
        "operator_notes",
        []
    ):


        result = ask_llm(note)


        valid,msg = validate_directive(
            result
        )


        directives.append({

            "directive_type":
            result["type"],


            "structured_adjustment":
            result,


            "valid":
            valid,


            "message":
            msg

        })



    plan = solve(
        data,
        directives
    )


    total_grid=sum(
        x["grid_kwh"]
        for x in plan
    )


    return Response({

        "scenario_id":
        data.get("scenario_id"),


        "directive_interpretation":
        directives,


        "hourly_plan":
        plan,


        "summary":{

            "total_grid_kwh":
            total_grid,


            "total_cost_bdt":
            total_grid*12

        }

    })