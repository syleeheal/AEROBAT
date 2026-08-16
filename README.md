# Automated Behavioral Scientific Research on AI Agents

[![Paper](https://img.shields.io/badge/arXiv-2608.10030-b31b1b.svg)](https://arxiv.org/abs/2608.10030)
![Analysis](https://img.shields.io/badge/analysis-notebooks%20reproducible-6a5acd.svg)
![Repository](https://img.shields.io/badge/repository-official-111.svg)

Official repository for the paper **Automating and Scaling Behavioral Scientific Research on
AI Agents**.

Paper: [arXiv:2608.10030](https://arxiv.org/abs/2608.10030)

AEROBAT is a multi-agent research pipeline for studying behavioral properties of
language-model agents. Given a target behavior and a subject agent, it generates
causal hypotheses, designs matched experimental configurations, runs controlled
multi-round simulations, blindly scores behavior, and fits the Bayesian
monotone-increment model used in the paper.

## At a Glance

| Goal | Entry Point |
| --- | --- |
| Run a new or cached behavioral study | [`run_notebook.ipynb`](run_notebook.ipynb) |
| Configure models, behaviors, and stages | [`seed.yaml`](seed.yaml) |
| Reproduce paper-facing analyses | [`run_analysis/`](run_analysis/) |
| Inspect released experiment outcomes | [`results/`](results/) |
| Use the implementation directly | [`src/aerobat/`](src/aerobat/) |

## Repository Layout

```text
seed.yaml           example experiment configuration
results/            public, transcript-free experiment outcomes
src/aerobat/        maintained AEROBAT implementation
run_notebook.ipynb  four-stage pipeline driver
run_analysis/       notebooks for regenerating analysis outputs
```

The repository is organized around two common workflows:

1. Run AEROBAT on a new or cached behavioral study with `run_notebook.ipynb`.
2. Recompute paper-facing analyses from the checked-in outcomes with
   `run_analysis/*.ipynb`.

If you are new to the repo, install the package, inspect [`seed.yaml`](seed.yaml),
and open [`run_notebook.ipynb`](run_notebook.ipynb). The notebook is intentionally
small: almost all experiment settings live in the YAML file.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[notebooks]"
```

Then:

1. Edit [`seed.yaml`](seed.yaml) for the behavior, models, and output directory.
2. Run [`run_notebook.ipynb`](run_notebook.ipynb) to execute the four-stage
   pipeline.
3. Run the notebooks in [`run_analysis/`](run_analysis/) to regenerate analysis
   tables and figures from `results/`.

## Installation

Python 3.10 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For notebook use:

```bash
pip install -e ".[notebooks]"
```

AEROBAT uses LiteLLM for model calls. Configure the relevant provider credentials
in your environment, then edit [`seed.yaml`](seed.yaml) for the models, target
behaviors, and stage settings you want to run.

No API credentials are stored in the repository.

## Using `seed.yaml`

[`seed.yaml`](seed.yaml) is the main experiment configuration file. For most uses,
you should copy or edit this file, then run the notebook or the Python API against
that configuration.

The fields people usually change first are:

```yaml
behavior:
  name: "literalism"
  description: "..."

simulation:
  subject_agent_model: "openai/gpt-5.1-mini"
  simulator_agent_model: "openai/gpt-5.1"

results_dir: "results/GPT-5-mini"
max_concurrent: 10
```

The major sections are:

| Section | What It Controls |
| --- | --- |
| `behavior` | The target behavior AEROBAT studies. `name` becomes the behavior directory name; `description` defines the behavior for hypothesis generation and review. |
| `research_manager` | Optional gatekeeping and report-writing model settings. The `stages` flags turn ranking, coherence, fidelity, and final-review gates on or off. |
| `hypothesis` | Stage 1 settings: hypothesis-generation model, number of hypotheses, number of suggested domains, and how many hypotheses advance to Stage 2. |
| `config_design` | Stage 2 settings: matched-configuration design model and `num_value_sets`, the number of matched groups per domain. |
| `simulation` | Stage 3 settings: subject-agent model, simulator model, temperatures, reasoning settings, token caps, and repetitions. |
| `review` | Stage 4 blind-review model settings. |
| `validity_analysis` | Settings for the optional environment-fidelity analysis notebook. |
| `results_dir` | Where outcomes for this run are read from or written to. Existing outcomes are reused unless the notebook requests a rerun. |
| `max_concurrent` | Global concurrency limit for model calls. Lower this if you hit provider rate limits. |

Two practical tips:

1. Use a fresh `results_dir` when running a new behavior or subject model, for
   example `results/my-new-run`.
2. Keep `behavior.description` explicit. AEROBAT uses it throughout the pipeline,
   so vague descriptions usually produce weaker hypotheses and noisier reviews.

## Running AEROBAT

The simplest entry point is [`run_notebook.ipynb`](run_notebook.ipynb). It wraps
`AerobatPipeline`, uses cached outcomes when available, and supports explicit
stage reruns through the notebook configuration.

Typical workflow:

1. Edit [`seed.yaml`](seed.yaml).
2. Open [`run_notebook.ipynb`](run_notebook.ipynb).
3. Set `STAGES = None` to run the complete cache-aware pipeline, or set a
   consecutive subset such as `[3, 4]` to rerun simulation and review using cached
   earlier stages.
4. Run the notebook. Outputs are written under the configured `results_dir`.

Programmatic use is minimal:

```python
from aerobat import AerobatPipeline, load_config

config = load_config("seed.yaml")
run = await AerobatPipeline(config).run()
```

The pipeline has four stages:

1. Generate behavior definitions, evaluation rubrics, and causal hypotheses.
2. Design matched configurations for selected hypotheses.
3. Run matched multi-round simulations.
4. Blindly review simulations and fit the statistical model.

Generated outcomes are written under the configured results directory. Existing
outcomes are reused unless a rerun is requested.

## Reproducing Analyses

Run the notebooks in [`run_analysis/`](run_analysis/) in numeric order:

```text
00_key_numbers.ipynb
01_behavioral_findings.ipynb
02_effect_by_configuration_component.ipynb
03_evidence_class_effects.ipynb
04_inter_subject_generalization.ipynb
05_environment_fidelity_and_gates.ipynb
06_model_and_rubric_sensitivity.ipynb
07_token_and_cost.ipynb
```

These notebooks read from `results/` and write generated figures, tables, CSVs,
JSON registries, and caches to ignored local directories such as
`run_analysis/outputs/` and `run_analysis/inputs/`. Those generated files are not
checked in; rerun the notebooks to recreate them.

## Released Results

The public `results/` directory contains canonical experiment outcomes grouped by
subject-agent model:

```text
model/
  target behavior/
    hypothesis_generation.json
    hypothesis id/
      matched_configurations.json
      matched_simulation_runs.json
      statistical_analysis.json
      sensitivity_analysis.json       # where available
      research_report.{json,md}       # where available
      domain/
        simulations/simulation_i*_j*_rep*.json
        reviews/review_i*_j*_rep*.json
```

## Citation

If you use AEROBAT or the released outcomes, please cite:

```bibtex
@article{lee2026automating,
  title={Automating and Scaling Behavioral Scientific Research on AI Agents},
  author={Lee, Soo Yong and Lee, Jongha and Chun, Jaewan and Hwang, Hyunjin and Bu, Fanchen and Ben-Zion, Ziv and Kim, Taekwan and Borsboom, Denny and Yoo, Jaemin and Shin, Kijung},
  journal={arXiv preprint arXiv:2608.10030},
  year={2026}
}
```

## License

Add the intended open-source license before publishing or redistributing this
repository.
