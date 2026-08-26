from career_advisor.questionnaire import calculate_results

# 1. Sample User Input (10 Questionnaire Choices)
sample_input_answers = {
    "Q1": "A",  # [VIS] Visual
    "Q2": "C",  # [VIS] Visual
    "Q3": "A",  # [VIS] Visual
    "Q4": "E",  # [VIS] Visual
    "Q5": "A",  # [VIS] Visual
    "Q6": "A",  # [VIS] Visual
    "Q7": "D",  # [VIS] Visual
    "Q8": "A",  # [VIS] Visual
    "Q9": "C",  # [VIS] Visual
    "Q10": "B"   # [VIS] Visual
}

# 2. Run Engine Calculation
output_result = calculate_results(sample_input_answers)

# 3. Display Output JSON
import json
print("--- MODEL INPUT ---")
print(json.dumps(sample_input_answers, indent=2))

print("\n--- MODEL OUTPUT (JSON for Frontend & Model 2) ---")
print(json.dumps(output_result, indent=2))