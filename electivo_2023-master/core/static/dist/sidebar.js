document.getElementById("expand-side-bar").addEventListener("click",(function(){var e=document.getElementById("sidebar");e.classList.contains("to-left")?e.classList.remove("to-left"):e.classList.add("to-left")})),document.querySelectorAll("img.svg").forEach((function(e){var t=e.getAttribute("src");fetch(t).then((function(t){t.text().then((function(t){var n=(new DOMParser).parseFromString(t,"image/svg+xml");e.replaceWith(n.documentElement)}))}))}));