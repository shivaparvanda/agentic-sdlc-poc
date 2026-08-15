from agents.requirement import analyze,approve
from agents.design import design
from agents.build_test import build
from agents.evaluator import evaluate
from tools.search import search_enterprise_context
from tools.architecture_validator import validate_architecture
def start(requirement):
    ctx=search_enterprise_context(requirement)
    req=analyze(requirement,"\n".join(x["content"] for x in ctx))
    return req,ctx
def after_clarification(requirement,answers):
    req=approve(answers); des=design(req); val=validate_architecture(des["architecture_decision"]); return req,des,val
def finish(req,des):
    b=build(req,des); e=evaluate(req,des,b); return b,e
