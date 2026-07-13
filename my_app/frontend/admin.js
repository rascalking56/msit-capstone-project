// Load navbar
fetch("navbar.html")
    .then(res => res.text())
    .then(html => document.getElementById("navbar").innerHTML = html);

// Role enforcement
const role = localStorage.getItem("role");
if (role !== "admin") {
    alert("Access denied: Admins only");
    window.location.href = "login.html";
}
