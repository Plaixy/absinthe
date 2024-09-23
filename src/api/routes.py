from quart import Blueprint, jsonify, request

import etcd3
import json
import replicate
import replicate.client
import yaml

api_bp = Blueprint('api', __name__)

@api_bp.route('/llm-validate', methods=['POST'])
async def llmValidate():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.json.get('data')
    if data is None:
        return jsonify({"error": "Missing 'data' field in JSON"}), 400
    try:
        content = json.loads(data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON string in 'data' field"}), 400
    
    if not isinstance(content, dict):
        return jsonify({"error": "Decoded JSON must be an object"}), 400
    
    return jsonify({"resul": "ok"}), 200

@api_bp.route('/characters', methods=['GET'])
async def characters():
    etcd_client = etcd3.client(host='47.95.214.18', port=2379)
    base_path = '/character/'
    try:
        key_values = etcd_client.get_prefix(base_path)
        character_names = []
        for key_value in key_values:
            value_str = key_value[0].decode('utf-8')
            try:
                character_data = yaml.safe_load(value_str)
                if 'character_name' in character_data:
                    character_names.append(character_data['character_name'])
            except yaml.YAMLError as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"characters": character_names}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        etcd_client.close()

@api_bp.route('/llm-models', methods=['GET'])
async def llmmodels():
    etcd_client = etcd3.client(host='47.95.214.18', port=2379)
    models = []
    try:
        value_str, _ = etcd_client.get('/rosemary/config/rosemary-config')
        yaml_content = value_str.decode('utf-8')
        config_data = yaml.safe_load(yaml_content)   
        if 'llm-providers' in config_data:
            models = list(config_data['llm-providers'].keys())
        return jsonify({"models": models}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        etcd_client.close()
    
@api_bp.route('/imagegen', methods=['POST'])
async def imagegen():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({"error": "The 'prompt' parameter is required"}), 400
    input = {
        "prompt": prompt,
        "output_quality": 90,
        "aspect_ratio": "1:1"
    }
    client = replicate.Client('PROVIDE_YOUR_KEY')
    output = client.run(
        "black-forest-labs/flux-schnell",
        input=input
    )
    return jsonify({"image": str(output)}), 200