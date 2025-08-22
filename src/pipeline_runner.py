import os
import yaml
import signal_process
from flask import jsonify

def execute_pipeline_config_test(node_id:int|str, signal:list=[]):

    # Get path relative to the script location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, 'pipelines', f'pipeline_{node_id}.yaml')

    with open(yaml_path, 'r') as file:
        result = None
        config = yaml.safe_load(file)
        for step_dict in config['pipeline']:
            print("Step ", step_dict['step'], " is being executed\n")
            function = signal_process.PROCESSING_FUNCTIONS.get(step_dict['step'])
            if function:
                if 'params' in step_dict:
                    kwargs = step_dict['params']
                else:
                    kwargs = dict()

                kwargs['signal'] = signal if result is None else result
                
                try:
                    result = function(**kwargs)
                except TypeError as e:
                    result = result
                    print("fail: Bad call to", function.__name__, ":", e)
                    
                print(result)

            else:
                raise Exception(f"fail: Function {step_dict['step']} was not found in *signal_process.py*")
                    
                    
def execute_pipeline_config(pipeline_json:dict):
    # Get path relative to the script location
    config = pipeline_json['config']
    for step_dict in config['pipeline']:
        print(step_dict['step'])
        function = signal_process.PROCESSING_FUNCTIONS.get(step_dict['step'])
        if function:
            if 'params' in step_dict:
                param_dict = step_dict['params']
                print(function(param_dict))
                        
                        
def load_pipeline_config(node_id:int|str):
    # Get path relative to the script location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yaml_path = os.path.join(base_dir, 'pipelines', f'pipeline_{node_id}.yaml')
    if os.path.exists(yaml_path):
        with open(yaml_path, 'r') as file:
            config_data = yaml.safe_load(file)
        return (config_data)
    else:
        return None
            

# Example usage inside src/pipeline_runner.py
if __name__ == '__main__':
    config = execute_pipeline_config_test(1, [1, 3, 5, 7, 9, 6, 4, 2])
