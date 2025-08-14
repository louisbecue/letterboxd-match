document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form[action="/compare"]');
  if (!form) return;

  form.addEventListener('submit', () => {
    document.body.classList.add('loading');
  });
});