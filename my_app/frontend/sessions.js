const API = "http://localhost:8000/sessions";

async function loadSessions() {
    const username = localStorage.getItem("username");

    const res = await fetch(`${API}/${username}`, {
        headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
    });

    const data = await res.json();
    const table = document.getElementById("sessionTable");

    data.forEach(s => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="p-3">${s.device_id}</td>
            <td class="p-3">${s.ip_address}</td>
            <td class="p-3">${s.user_agent}</td>
            <td class="p-3">${s.created_at}</td>
            <td class="p-3">${s.expires_at}</td>
            <td class="p-3">${s.revoked ? "Yes" : "No"}</td>
        `;
        table.appendChild(row);
    });
}

loadSessions();
