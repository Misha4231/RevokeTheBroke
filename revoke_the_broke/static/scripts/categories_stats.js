document.addEventListener('DOMContentLoaded', function () {
    if (typeof chartData === 'undefined') {
        console.error('chartData is not defined');
        return;
    }

    // Pie Chart
    const pieCtx = document.getElementById('PieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: chartData.titles,
            datasets: [{
                data: chartData.prices,
                backgroundColor: chartData.colors,
                hoverOffset: 4
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
});