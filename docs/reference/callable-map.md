# Callable Dependency Map

!!! note "Maintainer diagnostic page"
    This page is generated from source code and is intended for maintainers.
    For normal usage, start with the Function Usage Guide or Function Reference.

<style>
  .md-main__inner:has(.callable-map-shell) {
    max-width: min(1800px, 98vw);
  }
  .callable-map-shell {
    margin-inline: calc(50% - 49vw);
    max-width: 98vw;
  }
  @media (max-width: 1200px) {
    .callable-map-shell {
      margin-inline: 0;
      max-width: 100%;
    }
  }
</style>

<div class="callable-map-shell">
  <iframe
    id="callable-map-standalone"
    src="../../assets/callable-map.html"
    title="Callable lineage explorer"
    scrolling="no"
    style="width:100%;height:78vh;min-height:620px;border:1px solid #2a2f3a;border-radius:8px;overflow:hidden;display:block;"
  ></iframe>
</div>

<script>
  (function () {
    const frame = document.getElementById("callable-map-standalone");
    if (!frame) return;

    const minHeight = 620;
    const maxHeight = 2200;

    const setHeight = (height) => {
      const next = Math.max(minHeight, Math.min(maxHeight, Math.round(height || 0)));
      frame.style.height = `${next}px`;
    };

    window.addEventListener("message", (event) => {
      if (!event.data || event.data.type !== "callable-map-height") return;
      if (event.source !== frame.contentWindow) return;
      setHeight(event.data.height);
    });

    frame.addEventListener("load", () => {
      setHeight(window.innerHeight * 0.82);
    });
  })();
</script>
