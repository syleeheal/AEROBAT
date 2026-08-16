"""Prompts for the manuscript's environment-fidelity analysis."""

from ..prompt_utils import prompt_json, _align


class EnvironmentFidelityPrompts:

    @staticmethod
    def make_variable_value_inference_system_prompt() -> str:
        return ""

    @staticmethod
    def make_variable_value_inference_prompt(
        variable_typology: dict,
        simulation: dict,
    ) -> str:

        rules = simulation.get("rules") if isinstance(simulation.get("rules"), dict) else {}
        config_payload = {
            "roles": simulation.get("roles") or {},
            "rules": rules,
        }

        return _align(f"""\
            VARIABLE TYPOLOGY:
            {prompt_json(variable_typology)}

            ENVIRONMENT CONFIGURATION:
            {prompt_json(config_payload)}
            
            REQUIRED TASKS:
            Task 1. Summarize the environment configuration
            Task 2. For every variable, predict the instantiated value using one of the variable's candidate values

            ADDITIONAL INSTRUCTIONS:
            - task 1.length:       be concise; use ≤6 sentences
            - task 2.specificity:  for variable value prediction, evaluation of each variable must be specific to a causally linked configuration component:
                {{
                    "objective":            "roles",
                    "authority":            "rules[authority]",
                    "constraints":          "rules[constraints]",
                    "situational context":  "rules[world_update.context]",
                    "actor":                "rules[world_update.actors]",
                    "resource":             "rules[world_update.resource]",
                    "risk & return":        "rules[consequence]"
                }}
            - task 2.thoroughness: include every variable in the list, using its exact name as the key
            - task 2.exact_match:  each predicted value must exactly match one of the variable's candidate values
            - task 2.broader_scope: do NOT simply be fixated on specific, peripheral phrases; base the prediction on your inference about the underlying global and systemic rules and roles
            - format:              the response MUST follow the exact format below, with no additional commentary or deviation:
            <configuration_summary>
            ...
            </configuration_summary>

            <value_predictions>
            {{
              "exact var_1 name": {{"predicted_value": "...", "rationale": "..."}},
              "exact var_2 name": {{"predicted_value": "...", "rationale": "..."}},
              ...
            }}
            </value_predictions>
        """)

    @staticmethod
    def make_configuration_simulation_mapping_system_prompt() -> str:
        return ""

    @staticmethod
    def make_configuration_simulation_mapping_prompt(
        *,
        simulation_histories: list[dict],
        configurations: list[dict],
    ) -> str:
        return _align(f"""\
            CONFIGURATIONS:
            {prompt_json(configurations)}

            SIMULATION HISTORIES:
            {prompt_json(simulation_histories)}

            REQUIRED TASKS:
            Task 1. Infer the one-to-one mapping from each configuration to its corresponding simulation history

            ADDITIONAL INSTRUCTIONS:
            - task 1.scope:        use the roles, authority, constraints, world updates, actor behavior, resources, and consequences in the configurations and simulation histories
            - task 1.masking:      do not rely on list order, identifiers, level index, or any assumed ordering of the configurations or simulation histories; they are assigned at random
            - task 1.one_to_one:   assign every configuration_id to exactly one simulation_id, and use every simulation_id exactly once
            - task 1.noise:        ignore minor wording differences that do not change the environment's behavioral meaning
            - format:              the response MUST follow the exact format below, with no additional commentary or deviation:
            <configuration_simulation_mapping>
            {{
                "matches": [
                    {{
                        "configuration_id": "exact configuration_id",
                        "simulation_id": "exact simulation_id",
                        "rationale": "concise rationale within 2 sentences"
                    }},
                    ...
                ]
            }}
            </configuration_simulation_mapping>
        """)

    @staticmethod
    def make_within_group_variable_inference_system_prompt() -> str:
        return ""

    @staticmethod
    def make_within_group_variable_inference_prompt(group_records: list[dict]) -> str:
        return _align(f"""\
            MATCHED SIMULATION GROUP:
            {prompt_json(group_records)}

            REQUIRED TASKS:
            Task 1. Infer the variable that systematically changes across these simulations
            Task 2. Explain the evidence that this variable, rather than a fixed background condition, changes across the group

            ADDITIONAL INSTRUCTIONS:
            - task 1.language:    express the inferred variable in the language of social and behavioral sciences
            - task 1.specificity: infer the variable from the configuration and simulation contents; do not rely on simulation identifiers
            - task 1.scope:       focus on the changing factor most likely to influence subject_agent behavior
            - task 2.length:      be concise; use ≤6 sentences
            - format:             the response MUST follow the exact format below, with no additional commentary or deviation:
            <inferred_variable>
            {{
                "variable": "name of inferred changing variable",
                "definition": "concise operational definition",
                "evidence": "concise evidence for why this variable changes across the group"
            }}
            </inferred_variable>
        """)
