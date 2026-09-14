class Planner:

    def create_plan(
        self,
        intent: str
    ):

        plans = {

            "SYSTEM_STATUS": [
                "read_world_state",
                "evaluate_health",
                "evaluate_security",
                "generate_report"
            ],

            "ENERGY_OPTIMIZATION": [
                "inspect_resources",
                "identify_noncritical_tasks",
                "simulate_power_reduction",
                "apply_safe_configuration"
            ],

            "SECURITY_CHECK": [
                "inspect_devices",
                "calculate_trust",
                "check_quarantine",
                "generate_security_report"
            ],

            "SIMULATION": [
                "create_scenario",
                "simulate_candidates",
                "compare_results",
                "recommend_best_action"
            ],

            "PREDICTION": [
                "collect_state",
                "detect_anomalies",
                "predict_future_risk",
                "generate_explanation"
            ],

            "GENERAL_QUERY": [
                "understand_request",
                "select_capability",
                "generate_response"
            ]
        }

        return plans.get(
            intent,
            plans["GENERAL_QUERY"]
        )


planner = Planner()
