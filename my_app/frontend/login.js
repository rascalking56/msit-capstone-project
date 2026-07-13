document.getElementById("loginBtn").onclick = async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password, device_id: "web-client" })
    });

    const data = await res.json();

    if (data.access_token) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
        localStorage.setItem("username", username);

        // Decode role from JWT
        const payload = JSON.parse(atob(data.access_token.split(".")[1]));
        localStorage.setItem("role", payload.role);

        window.location.href = "admin.html";
    } else {
        alert("Invalid login");
    }
};
