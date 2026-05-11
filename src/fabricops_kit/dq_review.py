import json
import ipywidgets as widgets
from IPython.display import display as ipy_display

APPROVED_RULES_FROM_WIDGET = []
REJECTED_RULES_FROM_WIDGET = []


def review_dq_rules(candidate_rules, table_name: str):
    """
    Review one AI-suggested DQ rule at a time.

    Decision states:
    - Approve
    - Reject

    No skip state is allowed because every AI suggestion should be explicitly reviewed.
    """
    global APPROVED_RULES_FROM_WIDGET, REJECTED_RULES_FROM_WIDGET

    APPROVED_RULES_FROM_WIDGET = []
    REJECTED_RULES_FROM_WIDGET = []

    state = {"index": 0}

    title = widgets.HTML(
        value=f"<h4 style='margin:0;'>Human approval for AI-suggested DQ rules: {table_name}</h4>"
    )

    progress_label = widgets.HTML()
    rule_summary = widgets.HTML()

    severity_dropdown = widgets.Dropdown(
        options=["warning", "error"],
        description="Severity",
        layout=widgets.Layout(width="320px"),
    )

    description_box = widgets.Textarea(
        description="Description",
        layout=widgets.Layout(width="780px", height="80px"),
    )

    extras_box = widgets.Textarea(
        description="Extras JSON",
        layout=widgets.Layout(width="780px", height="100px"),
    )

    approve_button = widgets.Button(
        description="Approve",
        button_style="success",
        layout=widgets.Layout(width="220px"),
    )

    reject_button = widgets.Button(
        description="Reject",
        button_style="danger",
        layout=widgets.Layout(width="220px"),
    )

    undo_button = widgets.Button(
        description="Undo Last",
        button_style="warning",
        layout=widgets.Layout(width="220px"),
    )

    status = widgets.HTML()

    form_box = widgets.VBox(
        [
            severity_dropdown,
            description_box,
            extras_box,
            widgets.HBox([approve_button, reject_button, undo_button]),
        ]
    )

    def current_rule():
        idx = state["index"]
        if idx >= len(candidate_rules):
            return None
        return candidate_rules[idx]

    def load_current_rule():
        rule = current_rule()

        progress_label.value = (
            f"<b>Progress:</b> {state['index']} / {len(candidate_rules)} "
            f"&nbsp; | &nbsp; <b>Approved:</b> {len(APPROVED_RULES_FROM_WIDGET)} "
            f"&nbsp; | &nbsp; <b>Rejected:</b> {len(REJECTED_RULES_FROM_WIDGET)}"
        )

        if rule is None:
            total_reviewed = len(APPROVED_RULES_FROM_WIDGET) + len(REJECTED_RULES_FROM_WIDGET)

            rule_summary.value = f"""
            <div style="
                border:1px solid #d1e7dd;
                background:#f0fff4;
                padding:14px;
                border-radius:8px;
                margin-top:8px;
            ">
                <div style="font-size:18px; font-weight:700; color:#166534; margin-bottom:6px;">
                    ✅ Review complete
                </div>
                <div><b>Table:</b> {table_name}</div>
                <div><b>Total rules reviewed:</b> {total_reviewed} / {len(candidate_rules)}</div>
                <div><b>Approved:</b> {len(APPROVED_RULES_FROM_WIDGET)}</div>
                <div><b>Rejected:</b> {len(REJECTED_RULES_FROM_WIDGET)}</div>
                <div style="margin-top:10px; color:#444;">
                    Next step: store <b>APPROVED_RULES_FROM_WIDGET</b> into the metadata table.
                </div>
            </div>
            """

            form_box.layout.display = "none"

            if total_reviewed != len(candidate_rules):
                status.value = (
                    f"<span style='color:#b91c1c; font-weight:600;'>"
                    f"Warning: reviewed {total_reviewed} of {len(candidate_rules)} rules."
                    f"</span>"
                )
            else:
                status.value = (
                    "<span style='color:#166534; font-weight:600;'>"
                    "Approved rules are ready for metadata storage."
                    "</span>"
                )
            return

        rule_id = rule.get("rule_id", "")
        rule_type = rule.get("rule_type", "")
        columns = rule.get("columns", [])

        rule_summary.value = f"""
        <div style="
            border:1px solid #e5e7eb;
            background:#fafafa;
            padding:12px;
            border-radius:8px;
            margin-top:8px;
        ">
            <div style="font-weight:700; margin-bottom:8px;">Rule {state['index'] + 1} of {len(candidate_rules)}</div>
            <div><b>Rule ID:</b> <code>{rule_id}</code></div>
            <div><b>Rule type:</b> <code>{rule_type}</code></div>
            <div><b>Columns:</b> <code>{columns}</code></div>
        </div>
        """

        severity_value = str(rule.get("severity", "warning"))
        severity_dropdown.value = severity_value if severity_value in ["warning", "error"] else "warning"
        description_box.value = str(rule.get("description", ""))

        extras = {
            k: v
            for k, v in rule.items()
            if k not in {"rule_id", "rule_type", "columns", "severity", "description"}
        }
        extras_box.value = json.dumps(extras, indent=2) if extras else "{}"

        form_box.layout.display = ""
        status.value = ""

    def build_current_rule_from_widget():
        rule = current_rule()
        if rule is None:
            status.value = "<span style='color:red'>No current rule to review.</span>"
            return None

        edited_rule = dict(rule)

        try:
            extras = json.loads(extras_box.value or "{}")
            if not isinstance(extras, dict):
                raise ValueError("Extras JSON must be a dictionary.")
        except Exception as exc:
            status.value = f"<span style='color:red'><b>Invalid Extras JSON:</b> {exc}</span>"
            return None

        edited_rule["severity"] = severity_dropdown.value
        edited_rule["description"] = description_box.value

        for key, value in extras.items():
            edited_rule[key] = value

        return edited_rule

    def approve_clicked(_):
        rule = build_current_rule_from_widget()
        if rule is None:
            return

        APPROVED_RULES_FROM_WIDGET.append(rule)
        state["index"] += 1
        load_current_rule()

    def reject_clicked(_):
        rule = build_current_rule_from_widget()
        if rule is None:
            return

        REJECTED_RULES_FROM_WIDGET.append(rule)
        state["index"] += 1
        load_current_rule()

    def undo_clicked(_):
        if state["index"] == 0:
            status.value = "<span style='color:orange'>Nothing to undo.</span>"
            return

        state["index"] -= 1
        current_id = candidate_rules[state["index"]].get("rule_id")

        APPROVED_RULES_FROM_WIDGET[:] = [
            r for r in APPROVED_RULES_FROM_WIDGET if r.get("rule_id") != current_id
        ]
        REJECTED_RULES_FROM_WIDGET[:] = [
            r for r in REJECTED_RULES_FROM_WIDGET if r.get("rule_id") != current_id
        ]

        load_current_rule()

    approve_button.on_click(approve_clicked)
    reject_button.on_click(reject_clicked)
    undo_button.on_click(undo_clicked)

    ui = widgets.VBox(
        [
            title,
            progress_label,
            rule_summary,
            form_box,
            status,
        ],
        layout=widgets.Layout(
            border="1px solid #ddd",
            padding="12px",
            width="850px",
        ),
    )

    load_current_rule()
    ipy_display(ui)

# Backward-compatible aliases (not exported)
launch_sequential_rule_approval_widget = review_dq_rules
launch_sequential_rule_deactivation_widget = review_dq_rule_deactivations
