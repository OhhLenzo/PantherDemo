# CONTRIBUTING GUIDELINES

* [Overview](#overview)
* [General Guidelines](#general-guidelines)
* [Detection PRs](#detection-prs)
    * [Minimum Criteria](#minimum-criteria)
    * [What makes a Good Detection](#what-makes-a-good-detection)
* [Create a Detection Workflow](#create-a-detection-workflow)
    * [Copy Templates](#copy-templates)
    * [Generate an Event](#generate-an-event)
    * [Draft Detection (YAML)](#draft-a-detection-yaml)
    * [Draft Detection (JSON)](#draft-a-detection-python)
    * [Create A Runbook](#create-a-runbook)

## Overview

This file serves as a guide to contribute detections to the batCAVE Detections-as-Code repo. The maintainers of the 
repository recommend following a trunk based commit model. To do so, copy the
repository to your local machine, configure your *GitLab* git profile, and
create a new branch off of main.

```sh
git checkout -b <yourname>/<feature-name>
```

## General guidelines:

- We prefer [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) naming schemes, but won't block merges on it.
- Keep pull requests focused on a single feature or fix change - this makes them more likely to be reviewed closely. Eg - separate refactors into different PRs from individual new detections.
- Utilize [Black](https://github.com/psf/black) for style formatting.
- We won't merge with non-passing test cases, see below for more specific guidance.

## Detection PRs

### Minimum Criteria

For new detections, the following is a MINIMUM requirement for a detection to be merged and enabled:

* a detection must have AT LEAST one true positive and true negative test case. Maintainers reserve the right to ask for additional test coverage based on the complexity of the detection.
* a detection must link to a runbook, expressed as markdown in this repository. The runbook must be detailed enough an untrained person could follow the instructions and determine if an escalation is needed.
* a detection must be peer reviewed (required to merge anyway).

If a detection doesn't have a runbook - it can be merged, but must NOT be enabled or alerting to a human until that is satisfied.

PRs for modifications of environment specific metadata such as `batcave_environment.py` or other PRs that are not specifically adding new detections should still be reviewed, but the above rules may not be applicable in that instance.

### What Makes a Good Detection

Borrowed with rewording from [*How to Write an Actionable Alert*](https://catscrdl.io/blog/howtowriteanactionablealert/) (which we recommend reading anyway if you are participating in the detection engineering process for BatCAVE):

1. **Immediately human actionable**. If you as a detection engineer are going to present an alert, the responder who’s responding to it should have the tools and information they need to immediately make a decision and take action.

2. **Automatically enriched**. If the first step a responder needs to take when triaging an alert is to collect additional data or information, the detection should be reworked to provide this information automatically.

3. **Well prioritized**. If presented with multiple alerts to work, the responder should be able to easily identify which are the highest priority to work first.

4. **Grouped and correlated**. Panther Rules support a `dedup()` function, and we should make appropriate usage of it to ensure that related/similar alerts are grouped together, and don't produce unneeded noise.


Other best practice considerations:

- Detections shouldn't make use of external API calls. Consider using Panther's [lookup tables](https://docs.panther.com/enrichment/lookup-tables), or [caching](https://docs.panther.com/writing-detections/caching) functionality to achieve your desired outcome instead.
- Avoid directly indexing into event payloads and make use of `get` or `deep_get` instead. Due to the nature of json based detections, some fields might not always be present. Our detection logic should handle those cases.

## Create a detection workflow

Usually, a detection will be identified by the batCAVE Purple team and be
prioritized as part of a regular Agile cadence. Please reach out to
#batcave-watchtower for identifying detections that have been groomed and
scoped. The following process assumes that a detection has been created in this
manner.

### Copy Templates

* Navigate to the `/templates` directory.
* Copy the `detection_template.py` and `detection_template.yml` files from
`/templates` into a subfolder under the `/rules` directory, based on the data
source type.
* Rename the YAML and PY files to similar names, while keeping their respective
prefixes.
* Copy `runbook_template.md` to the runbooks directory.
* Rename the file to something like  `<datasource>-<name of detection>-runbook.md`

### Generate an Event

* Identify a potential indicator of compromise and the corresponding data source
* Trigger an indicator of compromise within an environment that outputs to
    Panther.
    * Using tools like 
    [stratus-red-team](https://stratus-red-team.cloud/attack-techniques/AWS/) and 
    [Dorthy](https://github.com/elastic/dorothy) can be helpful to replicate
    triggering events consistently.
* In Panther, use the "Investigate">"Query Builder" functionality via the 
    Panther UI to explore data sources, and their matching events.
    * You may need to search across multiple data sources to correctly identify
    the event.
    * Check the detections-as-code repo under the `/rules` directory for
        existing data sources.
        * If a new data source type is added, create a new folder under
        `/rules`.
* Once the event has been located within Panther, copy the event JSON.

### Draft a Detection (YAML)

* Rename the files based on the detection you are creating.
    * Refer to existing detections if you get lost.
* Start with the YAML file.
    * Remove all comments as you fill out the file
    * Under the `Tests` stanza, search for `Log:`.
    * Copy the JSON event from the previous section into `Log:` stanza.
        * Fix any JSON {}
    * If the detection does not use deduplication logic, remove
    `DedupPeriodMinutes` and `Threshold`.
    * Repeat this process for any additional related logs for other tests.
    * _*YOU MUST CREATE AT LEAST ONE TRUE AND ONE FALSE CASE*_
    * Adjust the `ExpectedResult:` under each Test heading.

### Draft a Detection (Python)

* Open the template detection python file.
* Include any additional helpers that may be needed to write the detection.
    * If none are needed, remove L#3.
* For a detection within batCAVE, we require 4 functions to be completed within
    the `.py` file. Each of these are locally scoped.
* `def rule(event):` - Refer to your detection YAML log file. For every
    key/value relevant to your detection, you can export the value from the
    event. These values are used in the logic of the `return` of the function.
    * The logic must evaluate as true.
* `def title(event):` - The output of this function must be a string, or a 
    variable of type string.
* `def alert_context(event):` - In the area above the return, use `deep_get()`
    to retrieve contextual keys that are useful to humans responding to the
    alert.
    * As part of the `return{}`, create the text and variable evaluations that
    will accompany the alert.
* `def destinations(event):` - Currently we return the `batcave_slack_alert`
function which sends alerts to #batcave-security-alerts room in slack.

### Create a Runbook

* Once you have drafted your alert and created at least one true and one false
test case, create a runbook.
* The runbooks support standard Markdown (.md) rather than extended Markdown (.mdx)
* Style Guide:
    * Use general lists `*` where possible.
    * If using numbered lists, use the number `1.` for all values. Markdown will
    create a numbered list with appropriate descent.
    * H1/`#` is only used for titles.
    * H2/`##` is used for all headings; Investigation, Remediation,
    Communication, Helpful Reading
* In the event that the `runbook_template.md` is updated, please update 
existing runbooks to match.
