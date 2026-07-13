const API = "http://127.0.0.1:8000";

function token() {
    return localStorage.getItem("access_token");
}

async function api(path, method = "GET") {
    const res = await fetch(`${API}${path}`, {
        method,
        headers: { "Authorization": `Bearer ${token()}` }
    });
    return res.json();
}

async function loadTrends() {
    const data = await api("/inventory/smart/trends");

    const labels = [];
    const datasets = [];

    Object.keys(data).forEach(product => {
        const points = data[product];
        const productLabels = points.map(p => p.day);
        const productValues = points.map(p => p.sold);

        labels.push(...productLabels);

        datasets.push({
            label: product,
            data: productValues,
            borderWidth: 2,
            fill: false
        });
    });

    new Chart(document.getElementById("trendChart"), {
        type: "line",
        data: { labels, datasets }
    });
}

async function loadLowStock() {
    const data = await api("/inventory/smart/low-stock");
    document.getElementById("lowStockOutput").textContent =
        JSON.stringify(data, null, 2);
}

async function autoRestock() {
    const data = await api("/inventory/smart/auto-restock", "POST");
    document.getElementById("autoRestockOutput").textContent =
        JSON.stringify(data, null, 2);
}

document.addEventListener("DOMContentLoaded", loadTrends);
