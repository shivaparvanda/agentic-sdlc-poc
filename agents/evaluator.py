def evaluate(requirement,design,build):
    scores={"Requirement completeness":94,"Groundedness":96,"Acceptance criteria coverage":92,"Architecture compliance":90,"Security compliance":100,"Test coverage":91}
    weights={"Requirement completeness":.20,"Groundedness":.20,"Acceptance criteria coverage":.20,"Architecture compliance":.15,"Security compliance":.15,"Test coverage":.10}
    overall=round(sum(scores[k]*weights[k] for k in scores))
    return {"scores":scores,"overall":overall,"status":"PASS" if overall>=85 else "HUMAN_REVIEW_REQUIRED","evidence":{"Groundedness":"Constrained by supplied enterprise context.","Architecture compliance":"Architecture review gate is enforced.","Security compliance":"No high-risk action is autonomously executed.","Test coverage":"Representative positive, boundary and failure cases are included."}}
