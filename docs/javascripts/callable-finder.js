(function () {
  function normalize(value) { return (value || "").toLowerCase().trim(); }
  function initCallableFinder() {
    const container = document.querySelector("[data-callable-finder]");
    const input = document.getElementById("callable-finder-input");
    const status = document.getElementById("callable-finder-status");
    const empty = document.querySelector("[data-callable-finder-empty]");
    const rows = Array.from(document.querySelectorAll("[data-callable-row='true']"));
    const roleFilters = Array.from(document.querySelectorAll("[data-role-filter]"));
    if (!container || !input || !status || !empty || rows.length === 0) return;
    if (container.dataset.callableFinderInitialized === "true") return;
    container.dataset.callableFinderInitialized = "true";
    const searchable = rows.map((row) => ({
      row,
      role: normalize(row.dataset.role),
      text: normalize([
        row.dataset.callableName,
        row.dataset.callableModule,
        row.dataset.callableStarterPath,
        row.dataset.role,
        row.dataset.callablePurpose,
      ].join(" ")),
    }));
    const total = searchable.length;
    function enabledRoles() { return new Set(roleFilters.filter((cb) => cb.checked).map((cb) => normalize(cb.dataset.roleFilter))); }
    function update() {
      const query = normalize(input.value);
      const roles = enabledRoles();
      let matched = 0;
      searchable.forEach((entry) => {
        const show = (query.length === 0 || entry.text.includes(query)) && roles.has(entry.role);
        entry.row.hidden = !show;
        if (show) matched += 1;
      });
      empty.hidden = matched !== 0;
      status.textContent = `Showing ${matched} of ${total} callables.`;
    }
    input.addEventListener("input", update);
    roleFilters.forEach((cb) => cb.addEventListener("change", update));
    update();
  }
  document.addEventListener("DOMContentLoaded", initCallableFinder);
  if (typeof document$ !== "undefined" && document$.subscribe) document$.subscribe(initCallableFinder);
})();
