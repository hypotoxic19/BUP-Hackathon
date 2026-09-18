import re


def extract_hours(text):
    """
    Extract hour information from text.
    Example:
    1 PM to 3 PM -> [13,14,15]
    """

    hours = []

    pattern = r'(\d+)\s*(am|pm).*?(\d+)\s*(am|pm)'

    match = re.search(pattern, text.lower())

    if match:

        start = int(match.group(1))
        end = int(match.group(3))

        start_period = match.group(2)
        end_period = match.group(4)

        if start_period == "pm" and start != 12:
            start += 12

        if end_period == "pm" and end != 12:
            end += 12

        hours = list(range(start, end + 1))


    return hours



def interpret_notes(notes):

    result=[]


    for i,note in enumerate(notes):

        text = note.lower()


        # Default
        directive = {
            "type":"no_op"
        }

        applies=False


        # 1. Solar Reduction

        if "solar" in text or "sun" in text:

            factor = 0.5


            percentage = re.search(
                r'(\d+)\s*%',
                text
            )

            if percentage:
                factor = int(
                    percentage.group(1)
                ) / 100


            directive={
                "type":"solar_reduction",
                "hours":extract_hours(text)
                         or [13,14,15],
                "factor":factor
            }

            applies=True



        # 2. No charging

        elif (
            "no charge" in text
            or "do not charge" in text
            or "charging prohibited" in text
        ):

            directive={
                "type":"no_charge_window",
                "hours":extract_hours(text)
                         or [14,15,16]
            }

            applies=True



        # 3. No discharge

        elif (
            "no discharge" in text
            or "do not discharge" in text
        ):

            directive={
                "type":"no_discharge_window",
                "hours":extract_hours(text)
                         or [18,19,20]
            }

            applies=True



        # 4. Battery reserve

        elif "reserve" in text:

            amount=100

            value=re.search(
                r'(\d+)\s*kwh',
                text
            )

            if value:
                amount=int(value.group(1))


            directive={
                "type":"minimum_battery_reserve",
                "energy_kwh":amount
            }

            applies=True



        # 5. Grid limit

        elif (
            "grid" in text
            and (
                "limit" in text
                or "maximum" in text
                or "not exceed" in text
            )
        ):

            limit=200

            value=re.search(
                r'(\d+)',
                text
            )

            if value:
                limit=int(value.group(1))


            directive={
                "type":"max_grid_window",
                "hours":extract_hours(text)
                         or [20,21,22],
                "limit":limit
            }

            applies=True



        result.append({

            "note_index":i,

            "original_note":note,

            "applies":applies,

            "directive_type":directive["type"],

            "structured_adjustment":directive

        })


    return result