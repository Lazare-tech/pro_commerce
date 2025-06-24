// Graph
var ctx = document.getElementById("myChart");

var myChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [
      "Chemises",
      "Chaussures",
      "Sacs-à-main",
      "Bijoux",
      "Mèches",
      "Perruques",
      "Maquillages",
    ],
    datasets: [
      {
        data: [8, 4, 1, 24, 29, 92, 34],
        lineTension: 0,
        backgroundColor: "transparent",
        borderColor: "#007bff",
        borderWidth: 4,
        pointBackgroundColor: "#007bff",
      },
    ],
  },
  options: {
    scales: {
      yAxes: [
        {
          ticks: {
            beginAtZero: false,
          },
        },
      ],
    },
    legend: {
      display: false,
    },
  },
});