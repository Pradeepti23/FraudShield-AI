// ======================================================
// FRAUDSHIELD-AI DASHBOARD CHARTS
// ======================================================

let fraudChartInstance = null;
let barChartInstance = null;


// ======================================================
// DONUT CHART
// ======================================================
function loadFraudChart(fraud, genuine) {

    const ctx = document.getElementById("fraudChart");

    if (!ctx) return;

    if (fraudChartInstance) {
        fraudChartInstance.destroy();
    }

    fraudChartInstance = new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: ["Fraud", "Genuine"],

            datasets: [{

                data: [fraud, genuine],

                backgroundColor: [
                    "#ef4444",
                    "#22c55e"
                ],

                borderColor: [
                    "#ffffff",
                    "#ffffff"
                ],

                borderWidth: 2,
                hoverOffset: 20

            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {
                        color: "white",
                        font: {
                            size: 14
                        }
                    }

                },

                title: {

                    display: true,

                    text: "Fraud vs Genuine Transactions",

                    color: "white",

                    font: {
                        size: 18
                    }

                }

            }

        }

    });

}


// ======================================================
// BAR CHART
// ======================================================
function loadBarChart(fraud, genuine) {

    const ctx = document.getElementById("barChart");

    if (!ctx) return;

    if (barChartInstance) {
        barChartInstance.destroy();
    }

    barChartInstance = new Chart(ctx, {

        type: "bar",

        data: {

            labels: [
                "Fraud",
                "Genuine"
            ],

            datasets: [{

                label: "Transactions",

                data: [fraud, genuine],

                backgroundColor: [
                    "#ef4444",
                    "#a1e19b"
                ],

                borderRadius: 15,

                borderWidth: 1

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            animation: {
                duration: 1500
            },

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                },

                title: {

                    display: true,

                    text: "Transaction Distribution",

                    color: "white",

                    font: {
                        size: 18
                    }

                }

            },

            scales: {

                x: {

                    ticks: {
                        color: "white"
                    },

                    grid: {
                        color: "rgba(183, 213, 83, 0.1)"
                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {
                        color: "white"
                    },

                    grid: {
                        color: "rgba(255,255,255,0.1)"
                    }

                }

            }

        }

    });

}


// ======================================================
// LOAD CHARTS
// ======================================================
document.addEventListener("DOMContentLoaded", () => {

    loadFraudChart(fraud, genuine);

    loadBarChart(fraud, genuine);

});