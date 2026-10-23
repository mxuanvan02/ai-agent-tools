# Risk tiers — how to write the rules

## The tier comes from the change, not the author

The same rule file must produce the same answer for a staff engineer and for an agent. If the
author can influence the tier, the tier is meaningless.

## Default is a floor, not a start

The default tier applies only to paths that match no rule. A common mistake is to start the
running maximum at the default: then no rule can ever lower the tier, every change becomes
high, and the gate is quietly useless while still printing a verdict.

## Always-human paths win over everything

A workflow file inside `docs/` must still be high, even when `docs/**` is low. The failure
mode of a wrong low is a silent merge; the failure mode of a wrong high is one extra read.
Always-human paths are the ones where the failure mode of a wrong low is irreversible.

## Unknown paths fail closed

A path that matches no rule lands on the default tier (high). Do not add a catch-all rule
that lowers the tier for "everything else" — that is the same mistake as starting the
maximum at the default.

## Size is its own risk signal

A change over the threshold (default 1000 lines) raises the tier floor to medium. This is
a floor, not a tier: an always-human path inside a big change still wins. The measured
finding rate on changes over 1k lines is high enough that the floor is raised rather than
trusting the path rules alone.

## The rules file is a policy, not a configuration

It must be reviewed by the same people who review the code it governs. A rule that demotes
a sensitive path to low is a policy decision, not a typo.
