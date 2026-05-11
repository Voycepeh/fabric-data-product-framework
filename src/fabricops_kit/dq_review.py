import json
try:
    import ipywidgets as widgets
    from IPython.display import display as ipy_display
except ImportError:  # pragma: no cover
    widgets = None
    ipy_display = None



def _require_ipywidgets() -> None:
    if widgets is None or ipy_display is None:
        raise ImportError("ipywidgets and IPython are required for DQ review widgets. Install the dq-review extra.")
APPROVED_RULES_FROM_WIDGET = []
REJECTED_RULES_FROM_WIDGET = []


def review_dq_rules(candidate_rules, table_name: str):
    """Review AI-suggested DQ rules sequentially with explicit approve/reject decisions.

    Parameters
    ----------
    candidate_rules : list[dict]
        Candidate rule dictionaries extracted from AI responses.
    table_name : str
        Logical table name displayed in the widget header.

    Returns
    -------
    None
        Displays an interactive widget and updates module-level review result lists.

    Raises
    ------
    ImportError
        If ``ipywidgets`` is unavailable in the current runtime.
    """
    _require_ipywidgets()
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



DEACTIVATED_RULES_FROM_WIDGET = []
KEPT_ACTIVE_RULES_FROM_WIDGET = []

def review_dq_rule_deactivations(active_rules, table_name: str):
    """Review active DQ rules one at a time for governed deactivation actions.

    Parameters
    ----------
    active_rules : list[dict]
        Active rule dictionaries loaded from rule metadata.
    table_name : str
        Logical table name displayed in the widget header.

    Returns
    -------
    None
        Displays an interactive widget and updates module-level review result lists.

    Raises
    ------
    ImportError
        If ``ipywidgets`` is unavailable in the current runtime.

    Notes
    -----
    Decisions are explicit per rule: keep active or deactivate. Deactivation requires a reason.
    """
    _require_ipywidgets()
    global DEACTIVATED_RULES_FROM_WIDGET, KEPT_ACTIVE_RULES_FROM_WIDGET
    DEACTIVATED_RULES_FROM_WIDGET = []
    KEPT_ACTIVE_RULES_FROM_WIDGET = []

    state = {"index": 0}
    title = widgets.HTML(value=f"<h4 style='margin:0;'>DQ rule deactivation review: {table_name}</h4>")
    progress = widgets.HTML()
    summary = widgets.HTML()
    reason_box = widgets.Textarea(description="Reason", placeholder="Required when deactivating", layout=widgets.Layout(width="780px", height="90px"))
    keep_button = widgets.Button(description="Keep Active", button_style="success", layout=widgets.Layout(width="220px"))
    deactivate_button = widgets.Button(description="Deactivate", button_style="danger", layout=widgets.Layout(width="220px"))
    undo_button = widgets.Button(description="Undo Last", button_style="warning", layout=widgets.Layout(width="220px"))
    status = widgets.HTML()

    form_box = widgets.VBox([reason_box, widgets.HBox([keep_button, deactivate_button, undo_button])])

    def current_rule():
        if state["index"] >= len(active_rules):
            return None
        return active_rules[state["index"]]

    def refresh():
        rule = current_rule()
        progress.value = f"<b>Progress:</b> {state['index']} / {len(active_rules)} &nbsp;|&nbsp; <b>Kept:</b> {len(KEPT_ACTIVE_RULES_FROM_WIDGET)} &nbsp;|&nbsp; <b>Deactivated:</b> {len(DEACTIVATED_RULES_FROM_WIDGET)}"
        if rule is None:
            form_box.layout.display = "none"
            summary.value = f"<div style='border:1px solid #d1e7dd;background:#f0fff4;padding:14px;border-radius:8px;margin-top:8px;'><div style='font-size:18px;font-weight:700;color:#166534;margin-bottom:6px;'>✅ Deactivation review complete</div><div><b>Table:</b> {table_name}</div><div><b>Reviewed:</b> {len(KEPT_ACTIVE_RULES_FROM_WIDGET)+len(DEACTIVATED_RULES_FROM_WIDGET)} / {len(active_rules)}</div><div><b>Kept active:</b> {len(KEPT_ACTIVE_RULES_FROM_WIDGET)}</div><div><b>Deactivated:</b> {len(DEACTIVATED_RULES_FROM_WIDGET)}</div></div>"
            status.value = "<span style='color:#166534; font-weight:600;'>Deactivation review decisions are ready for metadata append.</span>"
            return
        summary.value = f"<div style='border:1px solid #e5e7eb;background:#fafafa;padding:12px;border-radius:8px;margin-top:8px;'><div style='font-weight:700;margin-bottom:8px;'>Rule {state['index']+1} of {len(active_rules)}</div><div><b>Rule ID:</b> <code>{rule.get('rule_id','')}</code></div><div><b>Rule type:</b> <code>{rule.get('rule_type','')}</code></div><div><b>Columns:</b> <code>{rule.get('columns',[])}</code></div></div>"
        reason_box.value = ""
        form_box.layout.display = ""
        status.value = ""

    def keep_clicked(_):
        rule=current_rule()
        if rule is None: return
        KEPT_ACTIVE_RULES_FROM_WIDGET.append(rule)
        state['index'] += 1
        refresh()

    def deactivate_clicked(_):
        rule=current_rule()
        if rule is None: return
        reason=str(reason_box.value).strip()
        if not reason:
            status.value = "<span style='color:red'><b>Deactivation reason is required.</b></span>"
            return
        DEACTIVATED_RULES_FROM_WIDGET.append({"rule": rule, "action_reason": reason})
        state['index'] += 1
        refresh()

    def undo_clicked(_):
        if state['index']==0:
            status.value = "<span style='color:orange'>Nothing to undo.</span>"
            return
        state['index'] -= 1
        rid = active_rules[state['index']].get('rule_id')
        KEPT_ACTIVE_RULES_FROM_WIDGET[:] = [r for r in KEPT_ACTIVE_RULES_FROM_WIDGET if r.get('rule_id') != rid]
        DEACTIVATED_RULES_FROM_WIDGET[:] = [r for r in DEACTIVATED_RULES_FROM_WIDGET if r.get('rule',{}).get('rule_id') != rid]
        refresh()

    keep_button.on_click(keep_clicked)
    deactivate_button.on_click(deactivate_clicked)
    undo_button.on_click(undo_clicked)

    ui = widgets.VBox([title, progress, summary, form_box, status], layout=widgets.Layout(border="1px solid #ddd", padding="12px", width="850px"))
    refresh()
    ipy_display(ui)

# Backward-compatible aliases (not exported)
launch_sequential_rule_approval_widget = review_dq_rules
launch_sequential_rule_deactivation_widget = review_dq_rule_deactivations
