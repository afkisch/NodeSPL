import yaml
from dsp.processors import PROCESSING_FUNCTIONS

import temp_state

# TODO: Add error handling, just like in node-side processing
# standardize processing function output format for a smooth proc. chain

# TODO: Fix file handling

def run_server_pipelines(pipeline_yaml_path):
    """
    Runs all pipelines defined in YAML, returns dict of outputs.
    'type' is inferred dynamically.
    """
    with open(pipeline_yaml_path) as f:
        config = yaml.safe_load(f)
    
    node_id_list = config['nodes']

    result = {}
    for node_id in node_id_list:
        node_data = temp_state.latest_data.get(node_id, {'value': [0], 'last_seen': None})
        result_node = list()
        for name, pipe in config["pipelines"].items():
            print("Pipeline ", name, " is being executed\n")
            result_temp = None
            for step_def in pipe.get("pipeline", []):
                step_name = step_def["step"]
                function = PROCESSING_FUNCTIONS.get(step_name)                      # Can be done 
                if function:                                                        # using getattr()
                    kwargs = step_def.get("params", {})                             # w/o dict
                    kwargs['signal'] = node_data['value'] if result_temp is None else result_temp
                    try:
                        result_temp = function(**kwargs)
                        #print(result_node)
                    except TypeError as e:
                        result_temp = result_temp # Obviously...
                        print("fail: Bad call to", function.__name__, ":", e)
            
            result_node.append({'display_name': pipe.get('display_name', name),
                                'type': type(result_temp).__name__,
                                'value': result_temp})
            
        temp_state.results[node_id] = result[node_id] = {
            'last_seen': node_data['last_seen'],
            'outputs': result_node
        }

        # outfile_name = pipe.get('output_file', 'unknown')
        # if '.json' not in outfile_name:
        #     outfile_name = f"{outfile_name}.json"
        # outdir_path = os.path.join(os.path.abspath(''), 'src', 'results', node_data.get('node_id', 'unknown'))
        # if not os.path.exists(outdir_path):
        #     os.makedirs(outdir_path)

        # outfile_path = os.path.join(outdir_path, outfile_name)

        # with open(outfile_path, 'w', encoding='utf-8') as f:
        #     json.dump(result[name], f, ensure_ascii=False, indent=4)

    return result