(function () {
  function normalize(value) {
    return (value || "").toLowerCase().trim();
  }

  function initCallableFinder() {
    const container = document.querySelector("[data-callable-finder]");
    const input = document.getElementById("callable-finder-input");
    const status = document.getElementById("callable-finder-status");
    const empty = document.querySelector("[data-callable-finder-empty]");
    const rows = Array.from(document.querySelectorAll(".reference-catalogue-table tbody tr[data-callable-row='true']"));

    if (!container || !input || !status || !empty || rows.length === 0) {
      return;
    }
    if (container.dataset.callableFinderInitialized === "true") {
      return;
    }
    container.dataset.callableFinderInitialized = "true";

    const searchable = rows.map((row) => {
      const fields = [
        row.dataset.callableName,
        row.dataset.callableModule,
        row.dataset.callableStarterPath,
        row.dataset.callableImportance,
        row.dataset.callablePurpose,
      ];
      return { row, text: normalize(fields.join(" ")) };
    });

    const total = searchable.length;

    function update() {
      const query = normalize(input.value);
      let matched = 0;

      searchable.forEach((entry) => {
        const show = query.length === 0 || entry.text.includes(query);
        entry.row.hidden = !show;
        if (show) {
          matched += 1;
        }
      });

      empty.hidden = matched !== 0;
      if (query.length === 0) {
        status.textContent = `Showing all ${total} callables.`;
      } else {
        status.textContent = `Showing ${matched} of ${total} callables.`;
      }
    }

    input.addEventListener("input", update);
    update();
  }

  document.addEventListener("DOMContentLoaded", initCallableFinder);
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(initCallableFinder);
  }
})();
