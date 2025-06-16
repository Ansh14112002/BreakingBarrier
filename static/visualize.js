function renderCategoryChart(categoryScores) {
  const ctx = document.getElementById("categoryChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(categoryScores),
      datasets: [{
        label: "Score (%)",
        data: Object.values(categoryScores),
        backgroundColor: [
          "#42a5f5", "#66bb6a", "#ffca28", "#ef5350"
        ],
        borderRadius: 6,
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: "Category-wise Autism Likelihood",
          color: "#333",
          font: { size: 18 }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { stepSize: 20 }
        }
      }
    }
  });
}
