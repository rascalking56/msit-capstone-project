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

function makeChart(id, label, labels, data, color="blue") {
    new Chart(document.getElementById(id), {
        type: "line",
        data: {
            labels,
            datasets: [{
                label,
                data,
                borderColor: color,
                fill: false
            }]
        }
    });
}

async function loadDailySales() {
    const data = await api("/analytics/sales/daily");
    makeChart(
        "dailySalesChart",
        "Daily Sales",
        data.map(x => x.day),
        data.map(x => x.total),
        "blue"
    );
}

async function loadWeeklySales() {
    const data = await api("/analytics/sales/weekly");
    makeChart(
        "weeklySalesChart",
        "Weekly Sales",
        data.map(x => x.week),
        data.map(x => x.total),
        "green"
    );
}

async function loadMonthlySales() {
    const data = await api("/analytics/sales/monthly");
    makeChart(
        "monthlySalesChart",
        "Monthly Sales",
        data.map(x => x.month),
        data.map(x => x.total),
        "purple"
    );
}

async function loadRevenue() {
    const data = await api("/analytics/revenue");
    makeChart(
        "revenueChart",
        "Revenue ($)",
        data.map(x => x.day),
        data.map(x => x.revenue),
        "orange"
    );
}

async function loadCustomerPatterns() {
    const data = await api("/analytics/customers/patterns");

    new Chart(document.getElementById("customerChart"), {
        type: "bar",
        data: {
            labels: data.map(x => x.customer),
            datasets: [{
                label: "Total Spent ($)",
                data: data.map(x => x.total_spent),
                backgroundColor: "red"
            }]
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadDailySales();
    loadWeeklySales();
    loadMonthlySales();
    loadRevenue();
    loadCustomerPatterns();
});
