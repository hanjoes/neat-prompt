import logging

from action import CollectUserInfoAction, CollectGitInfoAction
from effect.effect import SetUserInfoEffect, SetGitInfoEffect
from flow.flow import Flow
from prompt.prompt import Prompt


logging.basicConfig(filename="/tmp/neat_prompt.log", level=logging.DEBUG)

flow = Flow(Prompt())
flow.add_action(CollectUserInfoAction(SetUserInfoEffect()))
flow.add_action(CollectGitInfoAction(SetGitInfoEffect()))
flow.run()
print flow.material
