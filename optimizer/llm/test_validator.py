from validator import validate_directive



test = {

"type":"solar_reduction",

"factor":0.5

}



result = validate_directive(test)


print(result)