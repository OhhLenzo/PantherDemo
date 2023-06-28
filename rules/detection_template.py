from helpers import batcave_slack_alert, deep_get

# Variables
KNOWN_SYSTEM_USERNAME = {
    "system:apiserver",
    "system:kube-controller-manager"
    "system:serviceaccount:velero:velero-server",
}

# Rule Definition
def rule(event):
    # Python... Use this section to define what should trigger an alert.
    # What object are we triggering off of?
    token_object = deep_get(event, "objectRef", "subresource")
    # What action was taken on the object?
    object_action = event.get("verb")
    # Who is allowed to make these actions, and who should be allowed?
    username = deep_get(event, "user", "username")
    usergroups = deep_get(event, "user", "groups", default=[])
    return (
        token_object == "token"
        and object_action == "create"
        and username not in KNOWN_SYSTEM_USERNAME
        and "system:nodes" not in usergroups
        )

def title(event):
    # Extract relevant information from the event
    identity = event["user"]["username"]
    action = event["verb"]
    resource = event["objectRef"]["resource"]
    # Generate the detection message
    detection_message = f"UNAUTHORIZED IDENTITY - {identity} - HAS ATTEMPTED TO {action} {resource} FROM THE CLUSTER"
    # Return detection message
    return detection_message

def alert_context(event):
    # Additional context to be provided by the alert. You must create the keys
    # and values displayed in context.
    return {
        "useragent": deep_get(
            event,
            "userAgent",
        ),
        "response_code": deep_get(
            event,
            "responseStatus",
            "code"
        )
    }

def destinations(event):
    # Output alert to Slack, or any other destination.
    return slack_alert()
