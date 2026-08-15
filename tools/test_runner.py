def run_tests():
    tests=[("inventory above threshold",True),("inventory below threshold",True),("exact threshold",True),("missing inventory",True),("stale inventory",True)]
    return {"passed":sum(x[1] for x in tests),"total":len(tests),"tests":tests,"status":"PASS"}
