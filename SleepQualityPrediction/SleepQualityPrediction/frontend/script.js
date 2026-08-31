// -----------------------------
// Elements
// -----------------------------
const uploadBtn = document.getElementById("uploadBtn");
const csvFile = document.getElementById("csvFile");
const output = document.getElementById("output");
const predictionResult = document.getElementById("predictionResult");
const sleepScoreEl = document.getElementById("sleepScore");

let barChart, pieChart, lineChart;

// -----------------------------
// Convert prediction number â†’ Label + Badge
// -----------------------------
function getPredictionBadge(value) {
  if (value === 0 || value === "0") return `<span class="badge bad">Bad</span>`;
  if (value === 1 || value === "1") return `<span class="badge good">Good</span>`;
  if (value === 2 || value === "2") return `<span class="badge best">Best</span>`;
  return value;
}

// -----------------------------
// Build HTML Table
// -----------------------------
function createTableFromJSON(data) {
  if (!data || !data.length) return "<p>No data to display</p>";

  const cols = Object.keys(data[0]);
  let html = `
    <table>
      <thead>
        <tr>${cols.map(col => `<th>${col}</th>`).join("")}</tr>
      </thead>
      <tbody>
  `;

  data.forEach(row => {
    html += "<tr>";
    cols.forEach(col => {
      let cell = row[col];
      if (col.toLowerCase().includes("pred")) cell = getPredictionBadge(cell);
      html += `<td>${cell}</td>`;
    });
    html += "</tr>";
  });

  html += "</tbody></table>";
  return html;
}

// -----------------------------
// Render Sleep Score Stars
// -----------------------------
function renderSleepScore(data) {
  if (!data || !data.length) return;

  const avgScore = data.reduce((sum, row) => sum + row.predicted_sleep_quality, 0) / data.length;
  const starsCount = Math.round(avgScore + 1); // simple mapping: 0->1, 1->2, 2->3 stars
  sleepScoreEl.innerHTML = "Sleep Score: " + "â­".repeat(starsCount) + "â˜†".repeat(5 - starsCount);
}

// -----------------------------
// Render Charts
// -----------------------------
function renderCharts(data) {
  // Bar Chart: Sleep Hours vs Quality
  const labels = data.map((_, i) => `Row ${i + 1}`);
  const sleepHours = data.map(row => parseFloat(row.sleep_duration || 0));
  const sleepQualities = data.map(row => row.predicted_sleep_quality);

  const barCtx = document.getElementById("barChart").getContext("2d");
  if (barChart) barChart.destroy();
  barChart = new Chart(barCtx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Sleep Hours",
        data: sleepHours,
        backgroundColor: "#4CAF50"
      },{
        label: "Sleep Quality",
        data: sleepQualities,
        backgroundColor: "#673AB7"
      }]
    },
    options: { responsive: true, plugins: { legend: { position: 'top' } } }
  });

  // Pie Chart: Sleep Quality distribution
  const counts = { 0:0, 1:0, 2:0 };
  sleepQualities.forEach(q => counts[q] = (counts[q] || 0) + 1);

  const pieCtx = document.getElementById("pieChart").getContext("2d");
  if (pieChart) pieChart.destroy();
  pieChart = new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Bad","Good","Best"],
      datasets: [{
        data: [counts[0], counts[1], counts[2]],
        backgroundColor: ["#e53935","#4CAF50","#673AB7"]
      }]
    },
    options: { responsive: true }
  });

  // Line Chart: Sleep Quality History
  let history = JSON.parse(localStorage.getItem("sleepHistory") || "[]");
  history = history.concat(sleepQualities);
  localStorage.setItem("sleepHistory", JSON.stringify(history));

  const lineCtx = document.getElementById("lineChart").getContext("2d");
  if (lineChart) lineChart.destroy();
  lineChart = new Chart(lineCtx, {
    type: "line",
    data: {
      labels: history.map((_, i) => `Session ${i+1}`),
      datasets: [{
        label: "Sleep Quality History",
        data: history,
        borderColor: "#0066ff",
        fill: false
      }]
    },
    options: { responsive: true }
  });
}

// -----------------------------
// Upload & Predict
// -----------------------------
uploadBtn.addEventListener("click", async () => {
  if (!csvFile.files.length) {
    alert("Please choose a CSV file.");
    return;
  }

  const file = csvFile.files[0];
  if (!file.name.endsWith(".csv")) {
    alert("Please upload a valid CSV file.");
    return;
  }

  const form = new FormData();
  form.append("file", file);
  predictionResult.innerHTML = "<p>Uploading and predicting...</p>";
  output.innerHTML = "<p>Loading results...</p>";

  try {
    const res = await fetch("/predict_csv", { method: "POST", body: form });
    if (!res.ok) {
      let errData = {};
      try { errData = await res.json(); } catch { errData.detail = await res.text(); }
      predictionResult.innerHTML = `<p style="color:red">Error: ${errData.detail}</p>`;
      return;
    }

    const data = await res.json();

    // Render results
    output.innerHTML = createTableFromJSON(data);
    renderSleepScore(data);
    renderCharts(data);

    // Prediction summary
    const avgPred = Math.round(data.reduce((s,r) => s+r.predicted_sleep_quality,0)/data.length);
    predictionResult.innerHTML = `Average Prediction: ${getPredictionBadge(avgPred)}`;

  } catch (err) {
    predictionResult.innerHTML = `<p style="color:red">Request failed: ${err.message}</p>`;
  }
});


