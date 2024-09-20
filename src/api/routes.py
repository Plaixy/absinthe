from quart import Blueprint, jsonify
import etcd
import os
import replicate
import replicate.client

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
async def health_check():
    return jsonify({"status": "ok"}), 200

@api_bp.route('/characters', methods=['GET'])
async def characters():
    # TODO async etcd client
    client = etcd.Client()
    try:
        value = client.read('/character').value
        return jsonify({"characters": value}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api_bp.route('/imagegen', methods=['GET', 'POST'])
async def imagegen():
    prompt = "a sci-fi looking cat with the tomato and lightning, the cat should be in a picture frame, in Disney-style 3D cartoon"
    input = {
        "prompt": prompt,
        "output_quality": 90,
        "aspect_ratio": "1:1"
    }
    client = replicate.Client('')
    output = client.run(
        "black-forest-labs/flux-schnell",
        input=input
    )
    return jsonify({"image": str(output)}), 200