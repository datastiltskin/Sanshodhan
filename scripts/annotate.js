// Review annotations: select text, press Flag, say what is wrong. Injected by
// scripts/annotate_server.py into locally served pages only. Notes are posted to
// /_annotations and land in review/annotations.jsonl.
(function () {
  "use strict";
  var KINDS = [
    ["extraction", "extraction fault (text differs from the page)"],
    ["role", "wrong role (should be a note, caption, table, heading...)"],
    ["diff", "diff is wrong (a change that is not one, or a missed one)"],
    ["source", "the book itself has it this way"],
    ["other", "other"],
  ];
  var style = document.createElement("style");
  style.textContent =
    "#an-btn{position:absolute;z-index:50;font:600 .8rem system-ui,sans-serif;padding:.25rem .6rem;border-radius:4px;border:1px solid #b33;background:#fff3f3;color:#b33;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.2)}" +
    "#an-box{position:absolute;z-index:51;width:min(26rem,92vw);background:#fff;color:#111;border:1px solid #999;border-radius:6px;padding:.7rem .8rem;box-shadow:0 4px 16px rgba(0,0,0,.25);font:.85rem system-ui,sans-serif}" +
    "#an-box blockquote{margin:.2rem 0 .5rem;padding:.2rem .5rem;border-left:3px solid #b33;max-height:6rem;overflow:auto;font-family:Georgia,serif;color:#333}" +
    "#an-box select,#an-box textarea{width:100%;font:inherit;margin:.2rem 0 .5rem;box-sizing:border-box}#an-box textarea{height:4.5rem}" +
    "#an-box .row{display:flex;gap:.5rem;justify-content:flex-end}#an-box button{font:inherit;padding:.25rem .8rem;cursor:pointer}" +
    "#an-box .meta{color:#666;font-size:.75rem;margin-bottom:.3rem}" +
    "#an-panel{position:fixed;right:.6rem;bottom:.6rem;z-index:49;font:.8rem system-ui,sans-serif}" +
    "#an-panel summary{cursor:pointer;background:#fff;border:1px solid #999;border-radius:4px;padding:.25rem .6rem;list-style:none}" +
    "#an-panel ul{background:#fff;border:1px solid #999;border-radius:6px;padding:.5rem .8rem;margin:.3rem 0 0;max-width:24rem;max-height:40vh;overflow:auto;list-style:none}" +
    "#an-panel li{margin:.3rem 0;border-bottom:1px solid #eee;padding-bottom:.3rem}#an-panel li b{color:#b33}#an-panel li button{font-size:.7rem;margin-left:.4rem}" +
    "mark.an-mark{background:#ffe08a}";
  document.head.appendChild(style);

  var btn = document.createElement("button");
  btn.id = "an-btn"; btn.type = "button"; btn.textContent = "Flag"; btn.hidden = true;
  document.body.appendChild(btn);
  var box = null, pending = null;

  function pageOf(node) {
    // Chapter pages: <section class="page" id="pNN">. Compare pages: the row's figcaptions
    // name the two page numbers, and the column says which side the text is from.
    var el = node.nodeType === 1 ? node : node.parentElement;
    var sec = el.closest("section.page");
    if (sec) return { page: sec.id.replace(/^p/, ""), side: "" };
    var row = el.closest(".cmp-row");
    if (row) {
      var col = el.closest(".col");
      var side = col ? (col.classList.contains("old") ? "old" : col.classList.contains("new") ? "new" : "unified") : "";
      var caps = Array.prototype.map.call(row.querySelectorAll("figcaption"), function (c) { return c.textContent.trim(); });
      return { page: caps.join(" | ") || row.id, side: side };
    }
    return { page: "", side: "" };
  }

  function contextOf(node) {
    var el = node.nodeType === 1 ? node : node.parentElement;
    var unit = el.closest(".s, p, li, h1, h2, h3, td, aside, figcaption") || el;
    return (unit.textContent || "").trim().replace(/\s+/g, " ").slice(0, 600);
  }

  document.addEventListener("mouseup", function (e) {
    if (box && box.contains(e.target)) return;
    setTimeout(function () {
      var sel = window.getSelection();
      var text = sel && sel.toString().trim();
      if (!text || box) { btn.hidden = true; return; }
      var range = sel.getRangeAt(0), rect = range.getBoundingClientRect();
      pending = { text: text, node: range.startContainer, rect: rect };
      btn.style.left = (window.scrollX + rect.right + 6) + "px";
      btn.style.top = (window.scrollY + rect.top - 4) + "px";
      btn.hidden = false;
    }, 0);
  });

  btn.addEventListener("click", function () {
    if (!pending) return;
    var where = pageOf(pending.node), ctx = contextOf(pending.node), text = pending.text;
    btn.hidden = true;
    box = document.createElement("div");
    box.id = "an-box";
    box.innerHTML =
      '<div class="meta">' + location.pathname + location.search + (where.page ? " · page " + where.page : "") + (where.side ? " · " + where.side + " side" : "") + "</div>" +
      "<blockquote></blockquote>" +
      "<select>" + KINDS.map(function (k) { return '<option value="' + k[0] + '">' + k[1] + "</option>"; }).join("") + "</select>" +
      '<textarea placeholder="What is wrong, and what should it be? (optional)"></textarea>' +
      '<div class="row"><button type="button" class="cancel">Cancel</button><button type="button" class="save">Save flag</button></div>';
    box.querySelector("blockquote").textContent = text;
    box.style.left = Math.max(8, Math.min(window.scrollX + pending.rect.left, window.scrollX + window.innerWidth - 440)) + "px";
    box.style.top = (window.scrollY + pending.rect.bottom + 8) + "px";
    document.body.appendChild(box);
    box.querySelector("textarea").focus();
    box.querySelector(".cancel").onclick = close;
    box.querySelector(".save").onclick = function () {
      var payload = {
        path: location.pathname + location.search, page: where.page, side: where.side,
        text: text, context: ctx, kind: box.querySelector("select").value, note: box.querySelector("textarea").value.trim(),
      };
      fetch("/_annotations", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json(); })
        .then(function () { close(); refresh(); })
        .catch(function (err) { alert("Could not save: " + err); });
    };
    document.addEventListener("keydown", onKey);
  });

  function onKey(e) { if (e.key === "Escape") close(); }
  function close() {
    if (box) { box.remove(); box = null; }
    document.removeEventListener("keydown", onKey);
    pending = null;
    var sel = window.getSelection(); if (sel) sel.removeAllRanges();
  }

  // The panel: this page's flags, with delete.
  var panel = document.createElement("details");
  panel.id = "an-panel";
  panel.innerHTML = "<summary>Flags: 0 here</summary><ul></ul>";
  document.body.appendChild(panel);

  function refresh() {
    fetch("/_annotations?path=" + encodeURIComponent(location.pathname + location.search))
      .then(function (r) { return r.json(); })
      .then(function (data) {
        panel.querySelector("summary").textContent = "Flags: " + data.notes.length + " here, " + data.total + " in all";
        var ul = panel.querySelector("ul");
        ul.innerHTML = "";
        data.notes.forEach(function (n) {
          var li = document.createElement("li");
          li.innerHTML = "<b></b> <span class='t'></span><br><i></i> <button type='button'>delete</button>";
          li.querySelector("b").textContent = n.kind + (n.page ? " p" + n.page : "") + (n.side ? " " + n.side : "");
          li.querySelector(".t").textContent = "“" + n.text.slice(0, 80) + (n.text.length > 80 ? "…" : "") + "”";
          li.querySelector("i").textContent = n.note || "";
          li.querySelector("button").onclick = function () {
            fetch("/_annotations?id=" + n.id, { method: "DELETE" }).then(refresh);
          };
          ul.appendChild(li);
        });
      })
      .catch(function () {});
  }
  refresh();
  // The compare view rewrites its address as the selects change, so refresh on that too.
  var lastHref = location.href;
  setInterval(function () { if (location.href !== lastHref) { lastHref = location.href; refresh(); } }, 1000);
})();
