import unittest

from tools.evidence_router import route


class EvidenceRouterTests(unittest.TestCase):
    def test_groups_supported_cross_function_evidence(self):
        result = route([
            {"domain": "platform", "claim": "CNI status observed", "citation": "synthetic://network/1", "confidence": "high"},
            {"domain": "compliance", "claim": "Policy report mapped", "citation": "synthetic://policy/1", "confidence": "medium"},
        ])
        self.assertEqual(result["summary"]["accepted"], 2)
        self.assertTrue(result["summary"]["human_review_required"])
        self.assertEqual(result["domains"]["platform"][0]["status"], "supported")

    def test_rejects_secret_like_content(self):
        result = route([
            {"domain": "data", "claim": "token=abc123", "citation": "synthetic://data/1", "confidence": "high"}
        ])
        self.assertEqual(result["summary"]["rejected"], 1)

    def test_rejects_missing_citation(self):
        result = route([
            {"domain": "sre", "claim": "Incident explained", "confidence": "high"}
        ])
        self.assertEqual(result["summary"]["rejected"], 1)


if __name__ == "__main__":
    unittest.main()
