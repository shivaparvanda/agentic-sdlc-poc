from tools.test_runner import run_tests
def build(requirement,design):
    code='''def should_notify(current_inventory, predicted_demand, threshold):\n    if current_inventory is None or predicted_demand is None:\n        raise ValueError("inventory and predicted demand are required")\n    return (current_inventory - predicted_demand) < threshold\n'''
    return {"code":code,"tests":["above threshold","below threshold","exact threshold","missing inventory","stale inventory"],"execution":run_tests(),"traceability":["AC1 -> threshold test","AC2 -> notification test","AC3 -> no automatic ordering test"]}
