from helpers import slack_alert, deep_get

# Variables

# Rule Definition
def rule(event):
    #Python. Use this section to define what should trigger an alert.
    # 
    return #Condition that is true

def title(event):
    # The output of this function must return a variable of type string, or a
    # string defined here.
    return f""

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
