from quart import Quart, request, jsonify
from quart.utils import run_sync

from service import Service

app = Quart(__name__)
service = Service()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/pass-through-async", methods=['POST'])
async def pass_through_async():
    data = await request.get_json()
    data = await service.pass_through_async(data)
    return jsonify(data)


@app.route("/pass-through-sync", methods=['POST'])
async def pass_through_sync():
    data = await request.get_json()
    data = await run_sync(service.pass_through_sync)(data)
    return jsonify(data)


@app.route("/calc-distance-async", methods=['POST'])
async def calc_distance_async():
    data = await request.get_json()
    data = await service.calc_distance_async()
    return jsonify(data)


@app.route("/calc-distance-sync", methods=['POST'])
async def calc_distance_sync():
    data = await request.get_json()
    data = await run_sync(service.calc_distance_sync)()
    return jsonify(data)
