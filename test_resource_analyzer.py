import unittest

from career_advisor import analyze_resources


class ResourceAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.profile = {"primary_field": "Software Development"}
        self.resources = [
            {"id": "foundation-1", "title": "Python Foundations", "route": "/courses/python", "field": "Software Development", "level": "beginner", "phase": "foundation"},
            {"id": "core-1", "title": "Web Framework Basics", "route": "/frameworks/web", "field": "Software Development", "level": "beginner", "phase": "core"},
            {"id": "project-1", "title": "Build an App", "route": "/projects/app", "field": "Software Development", "level": "beginner", "type": "capstone project"},
            {"id": "advanced-1", "title": "Advanced Systems", "route": "/advanced", "field": "Software Development", "level": "advanced", "phase": "core"},
            {"id": "design-1", "title": "Design Basics", "route": "/design", "field": "UI/UX Design", "level": "beginner"},
        ]

    def test_filters_and_formats_internal_resources(self):
        output = analyze_resources(self.profile, self.resources)

        self.assertIn("Python Foundations | ID: foundation-1 | Route: /courses/python", output)
        self.assertIn("Web Framework Basics | ID: core-1 | Route: /frameworks/web", output)
        self.assertIn("Build an App | ID: project-1 | Route: /projects/app", output)
        self.assertNotIn("Advanced Systems", output)
        self.assertNotIn("Design Basics", output)
        self.assertLess(output.index("Python Foundations"), output.index("Phase 2"))
        self.assertGreater(output.index("Web Framework Basics"), output.index("Phase 2"))
        self.assertGreater(output.index("Build an App"), output.index("Phase 3"))

    def test_missing_primary_field_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_resources({}, self.resources)

    def test_empty_match_still_returns_all_phases(self):
        output = analyze_resources({"primary_field": "Unknown Field"}, self.resources)
        self.assertEqual(output.count("Phase "), 3)
        self.assertIn("No matching internal capstone project available.", output)


if __name__ == "__main__":
    unittest.main()
