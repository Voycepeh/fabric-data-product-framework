def launch_sequential_rule_approval_widget(candidate_rules):
    """Return candidate rules for notebook-driven sequential approval UX."""
    return {'mode':'approval','rules':candidate_rules}

def launch_sequential_rule_deactivation_widget(active_rules):
    """Return active rules for notebook-driven sequential deactivation UX."""
    return {'mode':'deactivation','rules':active_rules}
