"""Benchmark Model 2 for relevance, schema compliance, and hallucinations."""

import re
import unittest

from career_advisor.questionnaire import calculate_results
from career_advisor.resource_analyzer import analyze_resources


mock_resources = [
    {
        "id": "ux-foundations-101",
        "title": "UI/UX Design Foundations",
        "category": "UI/UX Design",
        "difficulty": "beginner",
        "route": "/courses/ui-ux-foundations",
    },
    {
        "id": "figma-core-tools",
        "title": "Figma Core Tools",
        "category": "UI/UX Design",
        "difficulty": "beginner",
        "route": "/courses/figma-core-tools",
    },
    {
        "id": "ux-capstone",
        "title": "Design a Mobile App Prototype",
        "category": "UI/UX Design",
        "difficulty": "beginner",
        "route": "/projects/mobile-app-prototype",
    },
    {
        "id": "ux-research-advanced",
        "title": "Advanced UX Research Strategy",
        "category": "UI/UX Design",
        "difficulty": "advanced",
        "route": "/courses/advanced-ux-research",
    },
    {
        "id": "python-foundations",
        "title": "Python Programming Foundations",
        "category": "Software Development",
        "difficulty": "beginner",
        "route": "/courses/python-foundations",
    },
    {
        "id": "distributed-systems",
        "title": "Distributed Systems Architecture",
        "category": "Software Development",
        "difficulty": "advanced",
        "route": "/courses/distributed-systems",
    },
    {
        "id": "ml-intro",
        "title": "Introduction to Machine Learning",
        "category": "AI/ML & Intelligent Systems",
        "difficulty": "beginner",
        "route": "/courses/ml-intro",
    },
    {
        "id": "ai-capstone",
        "title": "Intelligent Systems Capstone",
        "category": "AI/ML & Intelligent Systems",
        "difficulty": "advanced",
        "route": "/projects/ai-capstone",
    },
]


def _selected_resources(roadmap: str) -> dict[str, list[dict[str, str]]]:
    """Extract resource records from Model 2's markdown output by phase."""
    selected = {"phase_1": [], "phase_2": [], "phase_3": []}
    phase = None
    for line in roadmap.splitlines():
        if line.startswith("### Phase 1:"):
            phase = "phase_1"
        elif line.startswith("### Phase 2:"):
            phase = "phase_2"
        elif line.startswith("### Phase 3:"):
            phase = "phase_3"
        elif phase and line.startswith("- ") and " | ID: " in line:
            match = re.fullmatch(r"- (.+) \| ID: ([^|]+) \| Route: (.+)", line)
            if not match:
                raise AssertionError(f"Resource line does not match the output schema: {line}")
            selected[phase].append(
                {"title": match.group(1), "id": match.group(2).strip(), "route": match.group(3)}
            )
    return selected


class Model2AccuracyTests(unittest.TestCase):
    def setUp(self):
        self.answers = {f"Q{number}": "B" for number in range(1, 11)}
        self.model_1_result = calculate_results(self.answers)
        self.roadmap = analyze_resources(self.model_1_result, mock_resources)
        self.selected = _selected_resources(self.roadmap)
        self.resources_by_id = {resource["id"]: resource for resource in mock_resources}

    def test_primary_field_relevance_and_output_schema(self):
        primary_field = self.model_1_result["primary_field"]
        phase_items = self.selected["phase_1"] + self.selected["phase_2"]
        self.assertTrue(phase_items, "Model 2 returned no Phase 1 or Phase 2 resources")

        for item in phase_items:
            self.assertIn(item["id"], self.resources_by_id)
            self.assertEqual(self.resources_by_id[item["id"]]["category"], primary_field)

    def test_zero_hallucination_policy(self):
        known_titles = {resource["title"] for resource in mock_resources}
        known_ids = set(self.resources_by_id)
        returned_items = self.selected["phase_1"] + self.selected["phase_2"]
        returned_items.extend(self.selected["phase_3"])
        for item in returned_items:
            self.assertIn(item["id"], known_ids)
            self.assertIn(item["title"], known_titles)

    def test_beginner_profile_excludes_advanced_resources(self):
        returned_ids = {
            item["id"]
            for phase_items in self.selected.values()
            for item in phase_items
        }
        advanced_ids = {
            resource["id"]
            for resource in mock_resources
            if resource["difficulty"] in {"advanced", "expert"}
        }
        self.assertTrue(advanced_ids.isdisjoint(returned_ids))


def main():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Model2AccuracyTests)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    model_1_result = calculate_results({f"Q{number}": "B" for number in range(1, 11)})
    roadmap = analyze_resources(model_1_result, mock_resources)
    selected = _selected_resources(roadmap)
    phase_items = selected["phase_1"] + selected["phase_2"]
    known = {resource["id"]: resource for resource in mock_resources}
    hallucinations = [item for item in phase_items if item["id"] not in known]
    matching = [item for item in phase_items if item["id"] in known and known[item["id"]]["category"] == model_1_result["primary_field"]]
    field_rate = 100 * len(matching) / len(phase_items) if phase_items else 0

    print("Model 1 primary field: " + model_1_result["primary_field"])
    print("Model 2 selected items: " + ", ".join(item["title"] for item in phase_items))
    print(f"Hallucination Rate (Target: 0%): {'PASS' if not hallucinations else 'FAIL'}")
    print(f"Field Match Rate (Target: 100%): {field_rate:.0f}% {'PASS' if field_rate == 100 else 'FAIL'}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())