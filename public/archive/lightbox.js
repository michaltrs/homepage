// Lightbox for archive image links
(function () {
  var overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = '<img>';
  document.body.appendChild(overlay);
  var img = overlay.querySelector('img');

  document.addEventListener('click', function (e) {
    var link = e.target.closest('a.lightbox');
    if (!link) return;
    e.preventDefault();
    img.src = link.href;
    overlay.classList.add('active');
  });

  overlay.addEventListener('click', function () {
    overlay.classList.remove('active');
    img.src = '';
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('active')) {
      overlay.classList.remove('active');
      img.src = '';
    }
  });
})();
