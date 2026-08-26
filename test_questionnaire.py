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
                {"title": "Software Development", "percentage": 30, "color": "#8B5CF6"},
                {"title": "UI/UX Design", "percentage": 30, "color": "#F97316"},
                {"title": "AI/ML & Intelligent Systems", "percentage": 10, "color": "#C084FC"},
                {"title": "Cyber Security & Networking", "percentage": 30, "color": "#EAB308"},
            ],
        )
        self.assertEqual(result["primary_field"], "Software Development")

    def test_invalid_answers_raise_value_error(self):
        with self.assertRaises(ValueError):
            calculate_results({question_id: "A" for question_id in list(ANSWER_MAPPING)[:-1]})

        answers = {question_id: "A" for question_id in ANSWER_MAPPING}
        answers["Q1"] = "Z"
        with self.assertRaises(ValueError):
            calculate_results(answers)


if __name__ == "__main__":
    unittest.main()
