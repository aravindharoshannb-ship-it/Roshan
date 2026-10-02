# ============================================================
# PEOPLE / HUMAN IMPACT EXTRACTION
# ============================================================

import re


def extract_people_information(text):

    result = {
        "People Trapped": 0,
        "People Injured": 0,
        "People Missing": 0,
        "Deaths": 0
    }

    text_lower = text.lower()

    # --------------------------------------------------------
    # NUMBER WORDS
    # --------------------------------------------------------

    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20
    }


    # --------------------------------------------------------
    # FUNCTION TO CONVERT NUMBER
    # --------------------------------------------------------

    def convert_number(value):

        value = value.lower().strip()

        if value.isdigit():

            return int(value)

        return number_words.get(
            value,
            0
        )


    # --------------------------------------------------------
    # PEOPLE TRAPPED
    # --------------------------------------------------------

    trapped_patterns = [

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+people?\s+(?:are\s+)?trapped',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+persons?\s+(?:are\s+)?trapped',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+people?\s+trapped',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+persons?\s+trapped'
    ]


    for pattern in trapped_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            result["People Trapped"] = convert_number(
                match.group(1)
            )

            break


    # --------------------------------------------------------
    # PEOPLE INJURED
    # --------------------------------------------------------

    injured_patterns = [

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+people?\s+(?:are\s+)?injured',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+persons?\s+(?:are\s+)?injured',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+injured\s+people?'
    ]


    for pattern in injured_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            result["People Injured"] = convert_number(
                match.group(1)
            )

            break


    # --------------------------------------------------------
    # PEOPLE MISSING
    # --------------------------------------------------------

    missing_patterns = [

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+people?\s+(?:are\s+)?missing',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+persons?\s+(?:are\s+)?missing',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+missing\s+people?'
    ]


    for pattern in missing_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            result["People Missing"] = convert_number(
                match.group(1)
            )

            break


    # --------------------------------------------------------
    # DEATHS
    # --------------------------------------------------------

    death_patterns = [

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+(?:people?\s+)?(?:have\s+)?died',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+deaths?',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+people?\s+(?:are\s+)?dead',

        r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)'
        r'\s+fatalities?'
    ]


    for pattern in death_patterns:

        match = re.search(
            pattern,
            text_lower
        )

        if match:

            result["Deaths"] = convert_number(
                match.group(1)
            )

            break


    return result
