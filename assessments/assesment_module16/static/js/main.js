// WriteSphere — Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

  // ============================
  // Scroll Reveal
  // ============================
  const revealElements = document.querySelectorAll('.reveal');
  if (revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    revealElements.forEach(el => revealObserver.observe(el));
  }

  // ============================
  // Mobile Nav Toggle
  // ============================
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      navMenu.classList.toggle('open');
      this.setAttribute('aria-expanded', navMenu.classList.contains('open'));
    });

    document.addEventListener('click', function (e) {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('open');
      }
    });
  }

  // ============================
  // Auto-dismiss alerts
  // ============================
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(100%)';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ============================
  // Like Button (AJAX)
  // ============================
  const likeBtn = document.getElementById('likeBtn');
  if (likeBtn) {
    likeBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = this.dataset.url;
      const countEl = document.getElementById('likeCount');
      const csrf = document.querySelector('[name=csrfmiddlewaretoken]') ||
        { value: getCookie('csrftoken') };

      fetch(url, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
        .then(r => r.json())
        .then(data => {
          if (data.liked) {
            this.classList.add('liked');
            this.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg> Liked · <span id="likeCount">${data.count}</span>`;
          } else {
            this.classList.remove('liked');
            this.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/></svg> Like · <span id="likeCount">${data.count}</span>`;
          }
        })
        .catch(console.error);
    });
  }

  // ============================
  // Reply Toggle
  // ============================
  document.querySelectorAll('.reply-toggle').forEach(btn => {
    btn.addEventListener('click', function () {
      const targetId = this.dataset.target;
      const form = document.getElementById(targetId);
      if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
      }
    });
  });

  // ============================
  // Image Preview on Upload
  // ============================
  const coverInput = document.getElementById('id_cover_image');
  const coverPreview = document.getElementById('coverPreview');
  if (coverInput && coverPreview) {
    coverInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          coverPreview.src = e.target.result;
          coverPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // ============================
  // Cookie helper
  // ============================
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

});
