(function () {
  function normalize(value) { return (value || "").toLowerCase().trim(); }
  function levenshtein(a, b) {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    const prev = new Array(b.length + 1);
    const curr = new Array(b.length + 1);
    for (let j = 0; j <= b.length; j += 1) prev[j] = j;
    for (let i = 1; i <= a.length; i += 1) {
      curr[0] = i;
      for (let j = 1; j <= b.length; j += 1) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
      }
      for (let j = 0; j <= b.length; j += 1) prev[j] = curr[j];
    }
    return prev[b.length];
  }

  function fuzzyTokenMatch(query, haystackTokens) {
    if (!query || query.length < 4 || haystackTokens.length === 0) return false;
    const maxDistance = query.length <= 5 ? 1 : 2;
    return haystackTokens.some((token) => {
      if (Math.abs(token.length - query.length) > maxDistance) return false;
      return levenshtein(query, token) <= maxDistance;
    });
  }

  function scoreEntry(query, entry) {
    if (!query) return 1;
    if (entry.name === query) return 100;
    if (entry.name.startsWith(query)) return 80;
    if (entry.name.includes(query)) return 60;
    if (entry.module.includes(query) || entry.role.includes(query) || entry.starterPath.includes(query)) return 40;
    if (entry.purpose.includes(query) || entry.text.includes(query)) return 30;
    if (fuzzyTokenMatch(query, entry.tokens)) return 10;
    return 0;
  }

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
      name: normalize(row.dataset.callableName),
      module: normalize(row.dataset.callableModule),
      role: normalize(row.dataset.role),
      starterPath: normalize(row.dataset.callableStarterPath),
      purpose: normalize(row.dataset.callablePurpose),
      text: normalize([
        row.dataset.callableName,
        row.dataset.callableModule,
        row.dataset.callableStarterPath,
        row.dataset.role,
        row.dataset.callablePurpose,
      ].join(" ")),
    })).map((entry) => ({ ...entry, tokens: entry.text.split(/[^a-z0-9_]+/).filter(Boolean) }));
    const total = searchable.length;
    function enabledRoles() { return new Set(roleFilters.filter((cb) => cb.checked).map((cb) => normalize(cb.dataset.roleFilter))); }
    function update() {
      const query = normalize(input.value);
      const roles = enabledRoles();
      let matched = 0;
      const visibleEntries = [];
      searchable.forEach((entry) => {
        const score = scoreEntry(query, entry);
        const show = score > 0 && roles.has(entry.role);
        entry.row.hidden = !show;
        if (show) {
          matched += 1;
          visibleEntries.push({ entry, score });
        }
      });
      visibleEntries
        .sort((a, b) => b.score - a.score || a.entry.name.localeCompare(b.entry.name))
        .forEach(({ entry }) => {
          entry.row.parentElement.appendChild(entry.row);
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
