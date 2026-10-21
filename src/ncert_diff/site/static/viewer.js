// Change toggles and the edition switcher. Preferences are remembered per browser.
(function () {
  var body = document.body;
  var BASE = document.documentElement.getAttribute("data-base") || "";
  function bind(id, cls, onByDefault) {
    var box = document.getElementById(id);
    if (!box) return;
    var key = "ncert-diff:" + id;
    var saved = null;
    try { saved = localStorage.getItem(key); } catch (e) {}
    var on = saved === null ? onByDefault : saved === "1";
    box.checked = on;
    function apply() {
      body.classList.toggle(cls, !box.checked);
      try { localStorage.setItem(key, box.checked ? "1" : "0"); } catch (e) {}
    }
    box.addEventListener("change", apply);
    apply();
  }
  bind("toggle-changes", "changes-off", true);
  bind("toggle-minor", "minor-off", false);
  if (!document.getElementById("toggle-minor")) body.classList.add("minor-off");
  var sw = document.getElementById("edition-switch");
  if (sw) sw.addEventListener("change", function () { location.href = sw.value + location.hash; });
  // Arriving from the search page: mark the search words on this page (Pagefind's own script).
  if (new URLSearchParams(location.search).has("highlight")) {
    import(BASE + "/pagefind/pagefind-highlight.js").then(function () {
      new PagefindHighlight({ highlightParam: "highlight" });
    }).catch(function () {});
  }
})();
