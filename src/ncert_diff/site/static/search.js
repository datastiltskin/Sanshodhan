// The search page. Pagefind (built into site/pagefind/ by `ncert-diff build`) finds the
// chapter pages that carry the words; this script groups those hits by chapter lineage so
// that one chapter is one result, and draws a chip for every edition of the book: found,
// present but not matching, or absent. See docs/search.md.
(function () {
  "use strict";
  var form = document.getElementById("search-form");
  if (!form) return;
  var qEl = document.getElementById("search-q");
  var sel = {
    klass: document.getElementById("search-class"),
    subject: document.getElementById("search-subject"),
    book: document.getElementById("search-book"),
    edition: document.getElementById("search-edition"),
    chapter: document.getElementById("search-chapter"),
  };
  var resultsEl = document.getElementById("search-results");
  var summaryEl = document.getElementById("search-summary");
  var moreWrap = document.getElementById("search-more-wrap");
  var moreBtn = document.getElementById("search-more");
  var helpEl = document.getElementById("search-help");
  var GROUPS_PER_PAGE = 20;
  var BATCH = 40;

  var catalogue = null; // /search/catalogue.json
  var booksById = {};
  var pagefind = null; // the Pagefind module, loaded on first use
  var pagefindFailed = false;
  var run = null; // the search in progress: {results, next, groups, order, q}

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // ---- pickers ----
  function fill(select, options, value) {
    var keep = value != null ? value : select.value;
    select.innerHTML = "<option value=''>any</option>";
    options.forEach(function (o) {
      var opt = document.createElement("option");
      opt.value = o.value; opt.textContent = o.text;
      select.appendChild(opt);
    });
    select.value = keep;
    if (select.value !== keep) select.value = "";
  }

  function visibleBooks() {
    return catalogue.books.filter(function (b) {
      return (!sel.klass.value || String(b.class) === sel.klass.value) && (!sel.subject.value || b.subject === sel.subject.value);
    });
  }

  function fillBooks(value) {
    fill(sel.book, visibleBooks().map(function (b) { return { value: b.id, text: b.title + " (class " + b.class + ")" }; }), value);
    fillBookDependents();
  }

  function fillBookDependents(edition, chapter) {
    var book = booksById[sel.book.value];
    form.querySelectorAll(".needs-book").forEach(function (l) { l.hidden = !book; });
    if (!book) { sel.edition.value = ""; sel.chapter.value = ""; return; }
    fill(sel.edition, book.editions.map(function (e) { return { value: e.id, text: e.label }; }), edition);
    fill(sel.chapter, book.lineages.map(function (l) { return { value: l.id, text: l.title || l.id }; }), chapter);
  }

  function setParams() {
    var p = new URLSearchParams();
    if (qEl.value.trim()) p.set("q", qEl.value.trim());
    if (sel.klass.value) p.set("class", sel.klass.value);
    if (sel.subject.value) p.set("subject", sel.subject.value);
    if (sel.book.value) p.set("book", sel.book.value);
    if (sel.edition.value) p.set("edition", sel.edition.value);
    if (sel.chapter.value) p.set("chapter", sel.chapter.value);
    var qs = p.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
  }

  function filters() {
    var f = {};
    if (sel.klass.value) f["class"] = sel.klass.value;
    if (sel.subject.value) f.subject = sel.subject.value;
    if (sel.book.value) f.book = sel.book.value;
    if (sel.edition.value) f.edition = sel.edition.value;
    if (sel.book.value && sel.chapter.value) f.lineage = sel.book.value + "/" + sel.chapter.value;
    return f;
  }

  // ---- Pagefind ----
  function loadPagefind() {
    if (pagefind) return Promise.resolve(pagefind);
    return import("/pagefind/pagefind.js").then(function (mod) {
      pagefind = mod;
      return pagefind.options({ excerptLength: 30, highlightParam: "highlight" }).then(function () { return pagefind; });
    }).catch(function () {
      pagefindFailed = true;
      throw new Error("no index");
    });
  }

  // The printed page a hit sits on: each page's text opens with an empty <span id="tNN">,
  // and Pagefind records every element with an id inside the indexed body as an anchor
  // with its word position. The last such anchor at or before the first matching word
  // names the page. (The page sections' own ids sit outside the indexed body.)
  function pageOf(data) {
    var at = data.locations && data.locations.length ? data.locations[0] : null;
    if (at === null) return null;
    var page = null;
    (data.anchors || []).forEach(function (a) {
      if (/^t\d+$/.test(a.id) && a.location <= at) {
        if (page === null || a.location >= page.location) page = a;
      }
    });
    return page ? page.id.slice(1) : null;
  }

  function search(immediate) {
    var q = qEl.value.trim();
    setParams();
    if (!q) {
      run = null;
      resultsEl.innerHTML = "";
      summaryEl.textContent = "";
      moreWrap.hidden = true;
      helpEl.hidden = false;
      return;
    }
    helpEl.hidden = true;
    summaryEl.textContent = "Searching...";
    loadPagefind().then(function (pf) {
      var opts = { filters: filters() };
      return immediate ? pf.search(q, opts) : pf.debouncedSearch(q, opts, 250);
    }).then(function (res) {
      if (res === null) return; // a newer search is on its way
      run = { q: q, results: res.results, next: 0, groups: {}, order: [], target: GROUPS_PER_PAGE };
      return loadMore();
    }).catch(function () {
      if (pagefindFailed) {
        summaryEl.textContent = "The search index was not built for this copy of the site (ncert-diff build writes it to site/pagefind/).";
      } else {
        summaryEl.textContent = "The search failed. Reload the page and try again.";
      }
    });
  }

  // Load hit data in batches, in rank order, until enough chapters are on show.
  function loadMore() {
    var mine = run;
    if (!mine) return Promise.resolve();
    if (mine.order.length >= mine.target || mine.next >= mine.results.length) {
      render();
      return Promise.resolve();
    }
    var batch = mine.results.slice(mine.next, mine.next + BATCH);
    mine.next += batch.length;
    return Promise.all(batch.map(function (r) { return r.data(); })).then(function (datas) {
      if (run !== mine) return;
      datas.forEach(function (d) {
        var m = d.meta || {};
        if (!m.book || !m.edition) return;
        var key = m.book + "/" + (m.lineage || m.chapter);
        var g = mine.groups[key];
        if (!g) {
          g = { book: m.book, lineage: m.lineage, best: d, hits: {} };
          mine.groups[key] = g;
          mine.order.push(key);
        }
        if (!g.hits[m.edition]) g.hits[m.edition] = { url: d.url, page: pageOf(d), chapter: m.chapter };
      });
      return loadMore();
    });
  }

  function chipHtml(cls, text, title, href) {
    var t = " title='" + esc(title) + "'";
    if (href) return "<a class='chip " + cls + "' href='" + esc(href) + "'" + t + ">" + esc(text) + "</a>";
    return "<span class='chip " + cls + "'" + t + ">" + esc(text) + "</span>";
  }

  function render() {
    var mine = run;
    if (!mine) return;
    var html = [];
    var older = 0;
    mine.order.slice(0, mine.target).forEach(function (key) {
      var g = mine.groups[key];
      var book = booksById[g.book];
      if (!book) return;
      var line = null;
      book.lineages.forEach(function (l) { if (l.id === g.lineage) line = l; });
      var chapters = line ? line.chapters : {};
      // "Only in older editions" is judged against complete editions: a partial capture
      // (a few chapters) at the end of the list says nothing about the rest of the book.
      var full = book.editions.filter(function (e) { return !e.partial; });
      var latest = full.length ? full[full.length - 1] : book.editions[book.editions.length - 1];
      var present = full.filter(function (e) { return chapters[e.id]; });
      var newest = present.length ? present[present.length - 1] : null;
      var onlyOlder = !newest || !g.hits[newest.id] || newest.id !== latest.id;
      if (onlyOlder) older += 1;
      var chips = book.editions.map(function (e) {
        var hit = g.hits[e.id];
        if (hit) {
          var href = hit.url + (hit.page ? "#p" + hit.page : "");
          return chipHtml("hit", e.short, e.label + (hit.page ? ", page " + hit.page : ""), href);
        }
        if (chapters[e.id]) return chipHtml("miss", e.short, e.label + ": chapter present, phrase not found", "/" + book.id + "/" + e.id + "/" + chapters[e.id] + "/");
        return chipHtml("absent", e.short, e.label + ": chapter not in this edition", null);
      });
      var best = g.best;
      var bestPage = pageOf(best);
      var title = line && line.title ? line.title : (best.meta.chapter_title || "");
      html.push(
        "<article class='hit-group" + (onlyOlder ? " older" : "") + "'>" +
        "<p class='hit-book'>" + esc(book.title) + ", class " + esc(book.class) + " " + esc(book.subject) +
        (onlyOlder ? " <span class='tag'>only in older editions</span>" : "") + "</p>" +
        "<h2><a href='" + esc(best.url + (bestPage ? "#p" + bestPage : "")) + "'>" + esc(title) + "</a></h2>" +
        "<p class='excerpt'>" + best.excerpt + "</p>" +
        "<p class='hit-from'>From the " + esc(best.meta.edition_label || best.meta.edition) + (bestPage ? ", page " + esc(bestPage) : "") + "</p>" +
        "<p class='chips'>" + chips.join(" ") + "</p>" +
        "</article>"
      );
    });
    resultsEl.innerHTML = html.join("");
    var shown = Math.min(mine.order.length, mine.target);
    var exhausted = mine.next >= mine.results.length;
    var count = exhausted ? mine.order.length : mine.order.length + " or more";
    var what = mine.order.length === 1 && exhausted ? "chapter matches" : "chapters match";
    summaryEl.textContent = shown
      ? count + " " + what + (older ? ", " + older + " of them only in older editions" : "") + (mine.results.length ? " (" + mine.results.length + " chapter pages across editions)" : "")
      : "Nothing found for “" + mine.q + "” with these filters.";
    moreWrap.hidden = !(mine.order.length > shown || !exhausted);
  }

  moreBtn.addEventListener("click", function () {
    if (!run) return;
    run.target += GROUPS_PER_PAGE;
    loadMore();
  });

  // ---- wiring ----
  var typing = null;
  qEl.addEventListener("input", function () {
    clearTimeout(typing);
    typing = setTimeout(function () { search(false); }, 150);
    if (pagefind && qEl.value.trim()) pagefind.preload(qEl.value.trim(), { filters: filters() });
  });
  qEl.addEventListener("focus", function () { loadPagefind().catch(function () {}); });
  form.addEventListener("submit", function (e) { e.preventDefault(); search(true); });
  sel.klass.addEventListener("change", function () { fillBooks(); search(true); });
  sel.subject.addEventListener("change", function () { fillBooks(); search(true); });
  sel.book.addEventListener("change", function () { fillBookDependents(); search(true); });
  sel.edition.addEventListener("change", function () { search(true); });
  sel.chapter.addEventListener("change", function () { search(true); });

  fetch("/search/catalogue.json").then(function (r) { return r.json(); }).then(function (cat) {
    catalogue = cat;
    cat.books.forEach(function (b) { booksById[b.id] = b; });
    var p = new URLSearchParams(location.search);
    var classes = [], subjects = [];
    cat.books.forEach(function (b) {
      if (classes.indexOf(b.class) < 0) classes.push(b.class);
      if (subjects.indexOf(b.subject) < 0) subjects.push(b.subject);
    });
    classes.sort(function (a, b) { return a - b; });
    fill(sel.klass, classes.map(function (c) { return { value: String(c), text: "Class " + c }; }), p.get("class") || "");
    fill(sel.subject, subjects.map(function (s) { return { value: s, text: s }; }), p.get("subject") || "");
    fillBooks(p.get("book") || "");
    fillBookDependents(p.get("edition") || "", p.get("chapter") || "");
    qEl.value = p.get("q") || "";
    search(true);
  }).catch(function () {
    summaryEl.textContent = "The search catalogue could not be loaded.";
  });
})();
