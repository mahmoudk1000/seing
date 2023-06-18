function toggleDarkTheme() {
  const body = document.getElementsByTagName("body")[0];
  const isDarkTheme = body.classList.contains('dark-theme');

  if (isDarkTheme) {
    body.classList.remove('dark-theme');
    sessionStorage.setItem('theme', 'light');
  } else {
    body.classList.add('dark-theme');
    sessionStorage.setItem('theme', 'dark');
  }
}
