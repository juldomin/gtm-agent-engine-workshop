import unittest

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTests(unittest.TestCase):
    def test_update_persists_to_record_and_rebuilds_profile(self):
        prospect_id = "LEAD-71001"
        record = data_service.PROSPECTS[prospect_id]
        original_tech_stack = record["tech_stack"]
        data_service._PROFILES.pop(prospect_id, None)

        try:
            data_service.save_profile_to_db(prospect_id, {"tech_stack": list(original_tech_stack)})
            result = data_service.update_prospect_info(prospect_id, "Kafka")

            self.assertTrue(result["updated"])
            self.assertIn("Kafka", data_service.fetch_tech_stack(prospect_id))
            rebuilt = build_prospect_profile.invoke({"prospect_id": prospect_id})
            self.assertIn("Kafka", rebuilt["prospect_profile"]["tech_stack"])
            self.assertFalse(data_service.update_prospect_info(prospect_id, "Kafka")["updated"])
        finally:
            record["tech_stack"] = original_tech_stack
            data_service.PROSPECTS[prospect_id] = record
            data_service._PROFILES.pop(prospect_id, None)
