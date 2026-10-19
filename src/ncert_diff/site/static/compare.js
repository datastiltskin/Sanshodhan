// The compare view: two editions of a chapter, page against page.
// Data comes from /data/<book>/pairs.json and /data/<book>/<from>__<to>/<chapter>.json,
// written by the site build. State lives in the URL (from, to, chapter) and the
// settings in localStorage.
(function () {
  var bar = document.getElementById("cmp-bar");
  if (!bar) return;
  var book = bar.dataset.book;
  var images = bar.dataset.images;
  var selFrom = document.getElementById("cmp-from");
  var selTo = document.getElementById("cmp-to");
  var selChapter = document.getElementById("cmp-chapter");
  var rowsEl = document.getElementById("cmp-rows");
  var summaryEl = document.getElementById("cmp-summary");
  var emptyEl = document.getElementById("cmp-empty");
  var fade = document.getElementById("cmp-fade");
  var index = null;
  var current = null; // {key, slug, data}

  // ---- settings (remembered per browser) ----
  var settings = { layout: "split", images: "side", onlyChanged: false, minor: false, fade: 50 };
  try { var saved = JSON.parse(localStorage.getItem("ncert-diff:compare") || "{}"); for (var k in saved) settings[k] = saved[k]; } catch (e) {}
  function saveSettings() { try { localStorage.setItem("ncert-diff:compare", JSON.stringify(settings)); } catch (e) {} }
  function applySettings() {
    rowsEl.className = "cmp-rows layout-" + settings.layout + " images-" + settings.images + (settings.minor ? "" : " minor-off");
    document.body.classList.toggle("onion", settings.images === "onion");
    rowsEl.style.setProperty("--fade", settings.fade / 100);
    var radios = bar.querySelectorAll("input[type=radio]");
    for (var i = 0; i < radios.length; i++) radios[i].checked = settings[radios[i].name] === radios[i].value;
    document.getElementById("cmp-only-changed").checked = settings.onlyChanged;
    document.getElementById("cmp-minor").checked = settings.minor;
    fade.value = settings.fade;
    filterRows();
  }
  bar.addEventListener("change", function (ev) {
    var t = ev.target;
    if (t.name === "layout" || t.name === "images") settings[t.name] = t.value;
    else if (t.id === "cmp-only-changed") settings.onlyChanged = t.checked;
    else if (t.id === "cmp-minor") settings.minor = t.checked;
    else return;
    saveSettings();
    applySettings();
  });
  fade.addEventListener("input", function () { settings.fade = +fade.value; rowsEl.style.setProperty("--fade", settings.fade / 100); saveSettings(); });

  // ---- URL state ----
  function params() { return new URLSearchParams(location.search); }
  function setParams(from, to, chapter) {
    var p = new URLSearchParams();
    p.set("from", from); p.set("to", to); if (chapter) p.set("chapter", chapter);
    history.replaceState(null, "", location.pathname + "?" + p.toString());
  }

  // ---- pickers ----
  function fill(select, options, value) {
    select.innerHTML = "";
    options.forEach(function (o) {
      var opt = document.createElement("option");
      opt.value = o.value; opt.textContent = o.label;
      if (o.value === value) opt.selected = true;
      select.appendChild(opt);
    });
  }
  function editionIndex(id) { for (var i = 0; i < index.editions.length; i++) if (index.editions[i].id === id) return i; return -1; }
  function chapterLabel(c) {
    if (c.status === "dropped") return c.old.number + ". " + c.old.title + " (only in the older edition)";
    if (c.status === "added") return c.new.number + ". " + c.new.title + " (only in the newer edition)";
    var num = c.old.number === c.new.number ? String(c.new.number) : c.old.number + " → " + c.new.number;
    var n = c.changed_pages;
    return num + ". " + c.new.title + (n ? " (" + n + " changed page" + (n === 1 ? "" : "s") + ")" : " (no changes)");
  }
  function setupPickers() {
    var p = params();
    var eds = index.editions;
    var from = p.get("from"), to = p.get("to");
    if (editionIndex(from) < 0) from = eds.length > 1 ? eds[eds.length - 2].id : eds[0].id;
    if (editionIndex(to) < 0 || editionIndex(to) <= editionIndex(from)) to = eds[Math.min(editionIndex(from) + 1, eds.length - 1)].id;
    fill(selFrom, eds.slice(0, -1).map(function (e) { return { value: e.id, label: e.label }; }), from);
    fill(selTo, eds.slice(editionIndex(from) + 1).map(function (e) { return { value: e.id, label: e.label }; }), to);
    var key = from + "__" + to;
    var chapters = (index.pairs[key] || { chapters: [] }).chapters;
    var slug = p.get("chapter");
    if (!chapters.some(function (c) { return c.slug === slug; })) slug = chapters.length ? chapters[0].slug : null;
    fill(selChapter, chapters.map(function (c) { return { value: c.slug, label: chapterLabel(c) }; }), slug);
    setParams(from, to, slug);
    return { key: key, slug: slug, from: from, to: to };
  }
  selFrom.addEventListener("change", function () { setParams(selFrom.value, "", selChapter.value); load(); });
  selTo.addEventListener("change", function () { setParams(selFrom.value, selTo.value, selChapter.value); load(); });
  selChapter.addEventListener("change", function () { setParams(selFrom.value, selTo.value, selChapter.value); load(); });
  document.getElementById("cmp-prev").addEventListener("click", function () { step(-1); });
  document.getElementById("cmp-next").addEventListener("click", function () { step(1); });
  function step(d) {
    var i = selChapter.selectedIndex + d;
    if (i < 0 || i >= selChapter.options.length) return;
    selChapter.selectedIndex = i;
    setParams(selFrom.value, selTo.value, selChapter.value); load();
  }

  // ---- rendering ----
  function pageLabel(side, page) { return (page ? "p. " + page : "no page number") + " · "; }
  function img(edition, dir, page, cls) {
    if (!page) return "";
    var src = images + "/" + book + "/" + edition + "/" + dir + "/p" + String(page).padStart(3, "0") + ".webp";
    return '<a href="' + src + '" target="_blank" rel="noopener"><img loading="lazy" class="' + cls + '" src="' + src + '" alt="Page ' + page + '"></a>';
  }
  function render(state, chapter, data) {
    var oldEd = index.editions[editionIndex(state.from)], newEd = index.editions[editionIndex(state.to)];
    var oldDir = chapter.old && chapter.old.dir, newDir = chapter.new && chapter.new.dir;
    var html = "";
    data.rows.forEach(function (row, i) {
      var classes = "cmp-row" + (row.real ? " real" : "") + (row.minor ? " minor" : "");
      var oldPage = row.old ? row.old.page : null, newPage = row.new ? row.new.page : null;
      html += '<section class="' + classes + '" id="row' + i + '">';
      html += '<div class="cmp-images">';
      html += '<figure class="old">' + (oldPage ? img(state.from, oldDir, oldPage, "under") : '<div class="nopage">No page in the ' + esc(oldEd.label) + "</div>") +
        '<figcaption>' + (oldPage ? "p. " + oldPage + " in the " + esc(oldEd.label) : "") + "</figcaption></figure>";
      html += '<figure class="new">' + (newPage ? img(state.to, newDir, newPage, "over") : '<div class="nopage">No page in the ' + esc(newEd.label) + "</div>") +
        '<figcaption>' + (newPage ? "p. " + newPage + " in the " + esc(newEd.label) : "") + "</figcaption></figure>";
      html += '<figure class="onion-box">' + (oldPage ? img(state.from, oldDir, oldPage, "under") : "") + (newPage ? img(state.to, newDir, newPage, "over") : "") +
        "<figcaption>" + (oldPage ? "p. " + oldPage : "") + (oldPage && newPage ? " over " : "") + (newPage ? "p. " + newPage : "") + "</figcaption></figure>";
      html += "</div>";
      html += '<div class="cmp-texts">';
      html += '<div class="col old text">' + (row.old ? row.old.html : "") + "</div>";
      html += '<div class="col new text">' + (row.new ? row.new.html : "") + "</div>";
      html += '<div class="col unified text">' + row.unified + "</div>";
      html += "</div></section>";
    });
    rowsEl.innerHTML = html;
    var c = data.counts || {};
    var parts = [];
    if (c.deleted) parts.push(c.deleted + " removed");
    if (c.inserted) parts.push(c.inserted + " added");
    if (c.modified) parts.push(c.modified + " reworded");
    summaryEl.textContent = chapter.status === "matched"
      ? (parts.length ? "In this chapter: " + parts.join(", ") + " sentences, over " + data.rows.length + " pages." : "No changes in this chapter beyond minor differences.")
      : (chapter.status === "dropped" ? "This chapter is not in the " + newEd.label + "." : "This chapter is new in the " + newEd.label + ".");
    filterRows();
  }
  function filterRows() {
    var rows = rowsEl.querySelectorAll(".cmp-row");
    var shown = 0;
    for (var i = 0; i < rows.length; i++) {
      var r = rows[i];
      var keep = !settings.onlyChanged || r.classList.contains("real") || (settings.minor && r.classList.contains("minor"));
      r.hidden = !keep;
      if (keep) shown++;
    }
    emptyEl.hidden = shown > 0 || rows.length === 0;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]; }); }

  function load() {
    var state = setupPickers();
    if (!state.slug) { rowsEl.innerHTML = ""; summaryEl.textContent = "No chapters to compare for this pair."; return; }
    var chapter = index.pairs[state.key].chapters.filter(function (c) { return c.slug === state.slug; })[0];
    summaryEl.textContent = "Loading…";
    fetch("/data/" + book + "/" + state.key + "/" + state.slug + ".json")
      .then(function (r) { return r.json(); })
      .then(function (data) { current = { state: state, chapter: chapter, data: data }; render(state, chapter, data); })
      .catch(function () { summaryEl.textContent = "Could not load this comparison."; });
  }

  fetch("/data/" + book + "/pairs.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; applySettings(); load(); })
    .catch(function () { summaryEl.textContent = "Could not load the edition list."; });
})();
