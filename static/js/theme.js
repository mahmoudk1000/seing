function toggleDarkTheme() {
  var body = document.getElementsByTagName("body")[0];
  var theme = body.classList.contains("body") ? "dark-theme" : "default-theme";
  body.classList.toggle(theme);
  // body.classList.toggle("dark-theme");
  // save the selected theme to the session
  sessionStorage.setItem("theme", theme);
  localStorage.setItem("theme", theme)
}
