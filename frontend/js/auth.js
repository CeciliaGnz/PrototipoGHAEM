document.addEventListener("DOMContentLoaded", function() {
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", function(e) {
        e.preventDefault();
        localStorage.removeItem("token"); // Elimina el JWT del almacenamiento
        window.location.href = "../../../index.html"; // Redirige al login
      });
    }
  });