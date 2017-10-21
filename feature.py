#!/usr/bin/env python2

from __future__ import print_function
import argparse
import os
import subprocess
import sys

ACTION_START = "start"
ACTION_SYNC = "sync"
ACTION_SWITCH = "switch"
ACTION_FINISH = "finish"
ACTION_ALTER = "alter"
ACTIONS = [
    ACTION_START,
    ACTION_SYNC,
    ACTION_SWITCH,
    ACTION_FINISH,
    ACTION_ALTER,
]

BRANCH_TYPE_USER = "user"
BRANCH_TYPE_INTEGRATION = "integration"
BRANCH_TYPES = [
    BRANCH_TYPE_USER,
    BRANCH_TYPE_INTEGRATION,
]

SYNC_STRATEGY_REBASE = "rebase"
SYNC_STRATEGY_MERGE_AND_PUSH = "merge_and_push"
SYNC_STRATEGY_MERGE_AND_PULL_REQUEST = "merge_and_pull_request"
SYNC_STRATEGIES = [
    SYNC_STRATEGY_REBASE,
    SYNC_STRATEGY_MERGE_AND_PUSH,
    SYNC_STRATEGY_MERGE_AND_PULL_REQUEST,
]

DEFAULT_BRANCH_TYPE = BRANCH_TYPE_USER
DEFAULT_SYNC_STRATEGY = {
    BRANCH_TYPE_USER: SYNC_STRATEGY_REBASE,
    BRANCH_TYPE_INTEGRATION: SYNC_STRATEGY_MERGE_AND_PUSH,
}
DEFAULT_TARGET_BRANCH = "master"
DEFAULT_REMOTE = "origin"

def get_config_value(key, split=None):
    value = subprocess.check_output(["git", "config", "--local", "--get-all", key])
    if split is None:
        return value
    else:
        return value.split(split)

def set_config_value(key, value):
    if type(value) != list:
        value = [value]
    for v in value:
        subprocess.call(["git", "config", "--local", "--replace-all", key, v])

def unset_config_value(key):
    subprocess.check_call(["git", "config", "--local", "--unset-all", key])

def remove_config_section(section):
    subprocess.check_call(["git", "config", "--local", "--remove-section", section])

# TODO: lookup in gitconfig
class Config(object):
    def __init__(self):
        pass

    def default_branch_type(self):
        return DEFAULT_BRANCH_TYPE

    def default_sync_strategy(self, branch_type):
        return DEFAULT_SYNC_STRATEGY[branch_type]

    def default_target_branch(self):
        return DEFAULT_TARGET_BRANCH

    def default_remote(self):
        return DEFAULT_REMOTE

class Feature(object):
    def __init__(self, name, branch_type, sync_strategy, target_branch, base_branch, remote, dependencies):
        self.name = name
        self.branch_type = branch_type
        self.sync_strategy = sync_strategy
        self.target_branch = target_branch
        self.base_branch = base_branch
        self.remote = remote
        self.dependencies = dependencies

    def _config_section(self):
        return "feature.{}".format(self.name)

    def _config_key(self, key):
        return "{}.{}".format(self.config_section(), key)

if __name__ == "__main__":
    config = Config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--dryrun", default=False, action="store_true")

    subparsers = parser.add_subparsers(help="Invoke one of the sub-commands")

    start_parser = subparsers.add_parser(ACTION_START)
    start_parser.add_argument("name")
    start_parser.add_argument("--type", choices=BRANCH_TYPES, default=config.default_branch_type())
    start_parser.add_argument("--strategy", choices=SYNC_STRATEGIES, default=None)
    start_parser.add_argument("--target", default=config.default_target_branch())
    start_parser.add_argument("--base")
    start_parser.add_argument("--depends", action="append")

    sync_parser = subparsers.add_parser(ACTION_SYNC)

    switch_parser = subparsers.add_parser(ACTION_SWITCH)

    finish_parser = subparsers.add_parser(ACTION_FINISH)

    alter_parser = subparsers.add_parser(ACTION_ALTER)

    args = parser.parse_args()
    print(args)
