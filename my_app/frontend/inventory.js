const API = "http://localhost:8000/inventory";

async function fetchData(endpoint) {
    const res = await fetch(`${API}/${endpoint}`, {
        headers: { "Authorization": `Bearer ${localStorage.getItem("access_token")}` }
    });
    return res.json();
}

async function loadInventory() {
    const data = await fetchData("trends");

    new Chart(document.getElementById("inventoryChart"), {
        type: "line",
        data: {
            labels: data.map(d => d.day),
            datasets: [{
                label: "Stock",
                data: data.map(d => d.stock),
                borderColor: "red",
                fill: false
            }]
        }
    });
}

async function loadPredictions() {
    const data = await fetchData("smart/predictions");
    const list = document.getElementById("predictionList");

    data.forEach(item => {
        const li = document.createElement("li");
        li.textContent = `${item.product}: ${item.prediction}`;
        list.appendChild(li);
    });
}

loadInventory();
loadPredictions();
