import yaml
from dsp.processors import PROCESSING_FUNCTIONS

# TODO: Add error handling, just like in node-side processing
# standardize processing function output format for a smooth proc. chain

def run_server_pipelines(node_data, pipeline_yaml_path):
    """
    Runs all pipelines defined in YAML, returns dict of outputs.
    'type' is inferred dynamically.
    """
    with open(pipeline_yaml_path) as f:
        config = yaml.safe_load(f)

    results = {}
    for name, pipe in config["pipelines"].items():
        data = node_data
        for step_def in pipe.get("pipeline", []):
            step_name = step_def["step"]
            params = step_def.get("params", {})
            processor = PROCESSING_FUNCTIONS[step_name]
            data = processor(data, **params)
        results[name] = {
            "display_name": pipe.get("display_name", name),
            "output_file": pipe.get("output_file", f"{name}.json"),
            "node_data": data,
            "type": type(data['value']).__name__  # inferred dynamically
        }
    return results


import os

res = run_server_pipelines({'node_id': '2', 'value': [1, 23, 4]}, os.path.join(os.path.abspath('.'), 'pipelines', 'pipeline_server.yaml'))
print(res)
