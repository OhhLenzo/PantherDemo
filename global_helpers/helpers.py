from functools import reduce
from collections.abc import Mapping


def batcave_slack_alert():
    # TODO: add more robust routing logic based on severity, type, etc
    return ["BatCAVE Slack Alerts"]


def deep_get(dictionary: dict, *keys, default=None):
    """Safely return the value of an arbitrarily nested map
    Inspired by https://bit.ly/3a0hq9E
    """
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, Mapping) else default,
        keys,
        dictionary,
    )
