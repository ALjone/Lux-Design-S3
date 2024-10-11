import json
from typing import Dict
import sys
from argparse import Namespace

import numpy as np

from agent import Agent
# from lux.config import EnvConfig
from lux.kit import from_json
### DO NOT REMOVE THE FOLLOWING CODE ###
agent_dict = dict() # store potentially multiple dictionaries as kaggle imports code directly
agent_prev_obs = dict()
def agent_fn(observation, configurations):
    """
    agent definition for kaggle submission.
    """
    global agent_dict
    step = observation.step
    player = observation.player
    remainingOverageTime = observation.remainingOverageTime
    if step == 1:
        with open(f"inputs_{step}.txt", "w") as f:
            f.write(str(observation.__dict__))
        agent_dict[player] = Agent(player, configurations["env_cfg"])
    agent = agent_dict[player]
    actions = agent.act(step - 1, from_json(observation.obs), remainingOverageTime)
    return dict(action=actions.tolist())
    
    
    
    # if step == 0:
    #     env_cfg = EnvConfig.from_dict(configurations["env_cfg"])
    #     agent_dict[player] = Agent(player, env_cfg)
    #     agent_prev_obs[player] = dict()
    #     agent = agent_dict[player]
    # agent = agent_dict[player]
    # obs = process_obs(player, agent_prev_obs[player], step, json.loads(observation.obs))
    # agent_prev_obs[player] = obs
    # agent.step = step
    # if obs["real_env_steps"] < 0:
    #     actions = agent.early_setup(step, obs, remainingOverageTime)
    # else:
    #     actions = agent.act(step, obs, remainingOverageTime)

    # return process_action(actions)

if __name__ == "__main__":
    
    def read_input():
        """
        Reads input from stdin
        """
        try:
            return input()
        except EOFError as eof:
            raise SystemExit(eof)
    step = 0
    player_id = 0
    env_cfg = None
    i = 0
    while True:
        inputs = read_input()
        raw_input = json.loads(inputs)
        observation = Namespace(**dict(step=raw_input["step"], obs=raw_input["obs"], remainingOverageTime=raw_input["remainingOverageTime"], player=raw_input["player"], info=raw_input["info"]))
        if i == 0:
            env_cfg = raw_input["info"]["env_cfg"]
            player_id = raw_input["player"]
        if i == 35 and player_id == "player_0":
            with open(f"inputs_{i}.txt", "w") as f:
                f.write(inputs)
        i += 1
        actions = agent_fn(observation, dict(env_cfg=env_cfg))
        # send actions to engine
        print(json.dumps(actions))