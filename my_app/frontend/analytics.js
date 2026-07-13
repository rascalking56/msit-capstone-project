const API = "http://127.0.0.1:8000";

function token() {
    return localStorage.getItem("access_token");
}

async function api(path) {
    const res = await fetch(`${API}${path}`, {
        headers: { "Authorization": `Bearer ${token()}` }
    });
    return res.json();
}

async function loadSalesChart() {
    const data = await api("/analytics/sales");

    const labels = data.map(x => x.day);
    const values = data.map(x => x.total_quantity);

    new Chart(document.getElementById("salesChart"), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Sales",
                data: values,
                borderColor: "blue",
                fill: false
            }]
        }
    });
}

async function loadRevenueChart() {
    const data = await api("/analytics/revenue");

    const labels = data.map(x => x.day);
    const values = data.map(x => x.revenue);

    new Chart(document.getElementById("revenueChart"), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label: "Revenue ($)",
                data: values,
                borderColor: "green",
                fill: false
            }]
        }
    });
}

async function loadTopProductsChart() {
    const data = await api("/analytics/top-products");

    const labels = data.map(x => x.name);
    const values = data.map(x => x.total_sold);

    new Chart(document.getElementById("topProductsChart"), {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Units Sold",
                data: values,
                backgroundColor: "orange"
            }]
        }
    });
}

async function loadLowStock() {
    const data = await api("/analytics/low-stock");
    document.getElementById("lowStockOutput").textContent =
        JSON.stringify(data, null, 2);
}

document.addEventListener("DOMContentLoaded", () => {
    loadSalesChart();
    loadRevenueChart();
    loadTopProductsChart();
    loadLowStock();
});
