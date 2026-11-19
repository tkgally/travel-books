// Remembers the "show page numbers" choice between pages. The site works without this file.
(function () {
  var box = document.getElementById('showpb');
  if (!box) return;
  var on = false;
  try { on = localStorage.getItem('showpb') === '1'; } catch (e) {}
  if (location.hash.indexOf('#pg-') === 0) on = true;
  function apply() { document.documentElement.classList.toggle('showpb', box.checked); }
  box.checked = on; apply();
  box.addEventListener('change', function () {
    apply();
    try { localStorage.setItem('showpb', box.checked ? '1' : '0'); } catch (e) {}
  });
})();
