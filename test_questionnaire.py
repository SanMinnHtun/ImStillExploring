import unittest

from career_advisor import ANSWER_MAPPING, QUESTIONS, calculate_results


class QuestionnaireTests(unittest.TestCase):
    def test_dataset_contains_exact_question_shape(self):
        self.assertEqual(len(QUESTIONS), 10)
        self.assertEqual([question["id"] for question in QUESTIONS], [f"Q{number}" for number in range(1, 11)])
        self.assertTrue(all(set(question["options"]) == set("ABCDE") for question in QUESTIONS))
        self.assertEqual(set(ANSWER_MAPPING), {f"Q{number}" for number in range(1, 11)})

    def test_each_answer_maps_to_one_trait(self):
        self.assertTrue(all(set(mapping) == set("ABCDE") for mapping in ANSWER_MAPPING.values()))
        self.assertTrue(all(trait in {"VIS", "SYS", "DAT", "INT", "SEC"} for mapping in ANSWER_MAPPING.values() for trait in mapping.values()))

    def test_results_have_expected_category_percentages(self):
        answers = {question_id: "A" for question_id in ANSWER_MAPPING}
        result = calculate_results(answers)

        self.assertEqual(
            result["top_career_matches"],
            [
                {"title": "UI/UX Design", "percentage": 16, "color": "#F97316"},
                {"title": "Cyber Security & Networking", "percentage": 16, "color": "#EAB308"},
                {"title": "DevOps & Cloud Architecture", "percentage": 14, "color": "#10B981"},
                {"title": "Game Development & Interactive Media", "percentage": 11, "color": "#EC4899"},
                {"title": "Frontend Engineering", "percentage": 11, "color": "#06B6D4"},
                {"title": "Security Operations & Threat Intelligence", "percentage": 11, "color": "#F59E0B"},
                {"title": "Software Development", "percentage": 8, "color": "#8B5CF6"},
                {"title": "Data Engineering & Analytics", "percentage": 8, "color": "#3B82F6"},
                {"title": "AI/ML & Intelligent Systems", "percentage": 5, "color": "#C084FC"},
            ],
        )
        self.assertEqual(result["primary_field"], "UI/UX Design")
        self.assertEqual(sum(match["percentage"] for match in result["top_career_matches"]), 100)

    def test_invalid_answers_raise_value_error(self):
        with self.assertRaises(ValueError):
            calculate_results({question_id: "A" for question_id in list(ANSWER_MAPPING)[:-1]})

        answers = {question_id: "A" for question_id in ANSWER_MAPPING}
        answers["Q1"] = "Z"
        with self.assertRaises(ValueError):
            calculate_results(answers)


if __name__ == "__main__":
    unittest.main()
