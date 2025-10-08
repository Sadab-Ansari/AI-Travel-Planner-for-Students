# utils/prompt_builder.py
"""
This module builds a structured prompt for the AI Travel Planner.
It takes user inputs and formats them into a detailed prompt
suitable for OpenAI API to generate a personalized itinerary.
"""

def build_travel_prompt(
    destination: str,
    duration_days: int,
    budget: int,
    group_type: str = "solo",
    travel_mode: str = "train",
    stay_preference: str = "budget hotel",
    food_preference: str = "mix",
    interests: str = "sightseeing",
    starting_location: str = "",
    travel_goal: str = "",
    weather_preference: str = "",
    special_conditions: str = ""
) -> str:
    """
    Build a travel itinerary prompt for OpenAI API.

    Args:
        destination (str): Travel destination
        duration_days (int): Number of days
        budget (int): Total budget in INR
        group_type (str): Solo / friends / couple / family
        travel_mode (str): Preferred mode of travel
        stay_preference (str): Hostel / Budget Hotel / Airbnb
        food_preference (str): Veg / Non-Veg / Mix
        interests (str): Adventure / Beaches / Historical / Foodie etc.
        starting_location (str): Where the trip starts
        travel_goal (str): Purpose of travel
        weather_preference (str): Desired weather
        special_conditions (str): Any restrictions or preferences

    Returns:
        str: Formatted prompt for AI
    """

    prompt = f"""
You are an expert travel planner. Create a detailed, student-friendly travel itinerary.

- Destination: {destination}
- Duration: {duration_days} days
- Total budget: ₹{budget}
- Group type: {group_type}
- Travel mode: {travel_mode}
- Stay preference: {stay_preference}
- Food preference: {food_preference}
- Interests: {interests}
- Starting location: {starting_location}
- Travel goal: {travel_goal}
- Weather preference: {weather_preference}
- Special conditions: {special_conditions}

Please provide:

1. Day-wise itinerary with activities
2. Estimated travel, stay, and food costs
3. One hidden gem or local experience per day
4. Tips for saving money and staying safe

Format it clearly with headings for each day.
"""

    return prompt
