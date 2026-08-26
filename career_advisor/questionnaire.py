"""Questionnaire data and career-trait scoring for the career advisor app."""

TRAITS = ("VIS", "SYS", "DAT", "INT", "SEC")
OPTION_LETTERS = ("A", "B", "C", "D", "E")

QUESTIONS = (
    {
        "id": "Q1",
        "text": "You buy a complicated piece of furniture with lots of parts. How do you assemble it?",
        "options": {
            "A": "Lay out every single screw and panel in precise, organized rows before starting.",
            "B": "Look at the cover photo to see how it should look, then start putting main pieces together visually.",
            "C": "Start building, but constantly test if joints wobble or parts feel weak along the way.",
            "D": "Skim the steps to understand the overall mechanism, then try to build it as fast as possible.",
            "E": "Group similar parts together and look for patterns in how the diagrams repeat.",
        },
    },
    {
        "id": "Q2",
        "text": "You are planning a week-long road trip with friends. What part do you naturally take charge of?",
        "options": {
            "A": "Creating a shared document with backup plans, emergency contacts, and vehicle checks.",
            "B": "Designing a fun playlist and creating a clean, easy-to-read itinerary poster for the group.",
            "C": "Mapping out the exact fuel stops, drive times, and reservation timelines.",
            "D": "Looking at past weather trends, gas prices, and crowd data to pick the absolute best departure times.",
            "E": "Finding fun roadside attractions, stopover games, and unique activities for the drive.",
        },
    },
    {
        "id": "Q3",
        "text": "When exploring a brand-new city for the first time, what catches your attention?",
        "options": {
            "A": "The unique architecture, signs, street layout, and overall visual mood of the neighborhood.",
            "B": "How the subway or public transit system connects all the distant parts of the city together.",
            "C": "Noticing where safety cameras are placed, where lighting is poor, or where rules aren't being followed.",
            "D": "How crowded different places get at different hours and how people move through the streets.",
            "E": "Discovering hidden spots, interactive exhibits, arcades, or lively street performances.",
        },
    },
    {
        "id": "Q4",
        "text": "You are playing a new escape room or puzzle game. What is your natural approach?",
        "options": {
            "A": "Examine physical objects to see how moving one part triggers another part to open.",
            "B": "Look at all the clues collected so far to find hidden connections or repeating numbers.",
            "C": "Systematically test every lock and door to see what is secured and what is left open.",
            "D": "Trace the logical steps backwards from the final goal to figure out what key is missing.",
            "E": "Notice colors, symbols, and artistic patterns hidden on the walls or furniture.",
        },
    },
    {
        "id": "Q5",
        "text": "An app you use every day suddenly changes its design overnight. How do you react?",
        "options": {
            "A": "I immediately notice if buttons moved, fonts changed, or if the layout looks better or worse.",
            "B": "I test everything I click to make sure my saved data and settings weren't lost or messed up.",
            "C": "I look for new smart features, like better search suggestions or automated shortcuts.",
            "D": "I poke around trying to find glitchy screens or missing features to see if they rushed the update.",
            "E": "I try out the new animations, swipe gestures, and micro-interactions to see how responsive it feels.",
        },
    },
    {
        "id": "Q6",
        "text": "When working on a group project, what kind of task feels least stressful for you?",
        "options": {
            "A": "Double-checking the final draft for inconsistent facts, bad formatting, or missing requirements.",
            "B": "Building a dynamic prototype or interactive presentation that the audience can engage with.",
            "C": "Structuring the folder drive, assigning file naming rules, and organizing shared files.",
            "D": "Polishing the final visual slides so the typography, alignment, and colors look professional.",
            "E": "Gathering research numbers, organizing survey feedback, and summarizing key takeaways.",
        },
    },
    {
        "id": "Q7",
        "text": "How do you react when a household device (like a TV remote or lamp) stops working?",
        "options": {
            "A": "I observe the symptoms (blinking light, delay) and compare them to times it failed before.",
            "B": "I open the battery hatch, inspect wires, and press buttons firmly to test the physical response.",
            "C": "I follow a strict process: power source first, connections second, settings third.",
            "D": "I check if there's a loose connection, safety switch, or damaged cord causing a risk.",
            "E": "I check if the indicator display or status light changed color or alignment.",
        },
    },
    {
        "id": "Q8",
        "text": "What kind of books, videos, or content do you consume when relaxing?",
        "options": {
            "A": "Documentaries about how massive structures, airports, or logistics networks operate behind the scenes.",
            "B": "True crime, mystery, or investigative stories about solving cases and uncovering secrets.",
            "C": "Video essays analyzing game mechanics, worldbuilding, or interactive storytelling.",
            "D": "Content about art history, interior design, photography, or typography.",
            "E": "Deep dives into interesting statistics, mysteries explained by data, or sports analytics.",
        },
    },
    {
        "id": "Q9",
        "text": "Imagine you are organizing a community festival. Which role would you take?",
        "options": {
            "A": "Setting up the entry gates, ticket checks, security perimeter, and safety rules.",
            "B": "Designing the event map, promotional flyers, badges, and stage decorations.",
            "C": "Tracking ticket sales data over time to estimate how much food and drink to order.",
            "D": "Managing the schedule, vendor logistics, and ensuring power and water supply runs continuously.",
            "E": "Running the festival games, activity booths, and stage entertainment to keep energy high.",
        },
    },
    {
        "id": "Q10",
        "text": "What feeling gives you the biggest sense of accomplishment?",
        "options": {
            "A": "Looking at a clean, beautiful finished product that people enjoy seeing and touching.",
            "B": "Watching a complex, multi-step process execute automatically from start to finish without errors.",
            "C": "Finding a hidden truth or accurately predicting an outcome using facts and evidence.",
            "D": "Creating something fun where people can play, experiment, and react in real-time.",
            "E": "Successfully finding a critical flaw or risk before it could cause real trouble.",
        },
    },
)

ANSWER_MAPPING = {
    "Q1": {"A": "SYS", "B": "VIS", "C": "SEC", "D": "INT", "E": "DAT"},
    "Q2": {"A": "SEC", "B": "VIS", "C": "SYS", "D": "DAT", "E": "INT"},
    "Q3": {"A": "VIS", "B": "SYS", "C": "SEC", "D": "DAT", "E": "INT"},
    "Q4": {"A": "INT", "B": "DAT", "C": "SEC", "D": "SYS", "E": "VIS"},
    "Q5": {"A": "VIS", "B": "SYS", "C": "DAT", "D": "SEC", "E": "INT"},
    "Q6": {"A": "SEC", "B": "INT", "C": "SYS", "D": "VIS", "E": "DAT"},
    "Q7": {"A": "DAT", "B": "INT", "C": "SYS", "D": "SEC", "E": "VIS"},
    "Q8": {"A": "SYS", "B": "SEC", "C": "INT", "D": "VIS", "E": "DAT"},
    "Q9": {"A": "SEC", "B": "VIS", "C": "DAT", "D": "SYS", "E": "INT"},
    "Q10": {"A": "VIS", "B": "SYS", "C": "DAT", "D": "INT", "E": "SEC"},
}

_CATEGORY_DETAILS = (
    ("Software Development", ("SYS", "INT"), "#8B5CF6"),
    ("UI/UX Design", ("VIS",), "#F97316"),
    ("AI/ML & Intelligent Systems", ("DAT",), "#C084FC"),
    ("Cyber Security & Networking", ("SEC",), "#EAB308"),
)


def calculate_results(answers):
    """Calculate career category percentages from Q1-Q10 letter selections."""
    expected_questions = set(ANSWER_MAPPING)
    supplied_questions = set(answers)
    missing = expected_questions - supplied_questions
    unexpected = supplied_questions - expected_questions
    if missing or unexpected:
        problems = []
        if missing:
            problems.append("missing answers: " + ", ".join(sorted(missing)))
        if unexpected:
            problems.append("unexpected answers: " + ", ".join(sorted(unexpected)))
        raise ValueError("Invalid questionnaire answers (" + "; ".join(problems) + ")")

    trait_counts = {trait: 0 for trait in TRAITS}
    for question_id, selected_option in answers.items():
        if selected_option not in OPTION_LETTERS:
            raise ValueError(
                f"Invalid option for {question_id}: {selected_option!r}. "
                f"Expected one of {', '.join(OPTION_LETTERS)}."
            )
        trait_counts[ANSWER_MAPPING[question_id][selected_option]] += 1

    matches = []
    for title, traits, color in _CATEGORY_DETAILS:
        percentage = sum(trait_counts[trait] for trait in traits) * 10
        matches.append({"title": title, "percentage": percentage, "color": color})

    primary_field = max(matches, key=lambda match: match["percentage"])["title"]
    return {"top_career_matches": matches, "primary_field": primary_field}
