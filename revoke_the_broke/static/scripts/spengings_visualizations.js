document.addEventListener('DOMContentLoaded', function () {
    // Get references to the options and visualization wrappers
    const listOption = document.getElementById('list-option');
    const pieOption = document.getElementById('pie-option');
    const barOption = document.getElementById('bar-option');

    const listWrapper = document.querySelector('.exp-list-wrapper');
    const pieWrapper = document.querySelector('.exp-pie-wrapper');
    const barWrapper = document.querySelector('.exp-bar-wrapper');

    // Function to show the selected visualization and hide others
    function showVisualization(wrapperToShow, chosenOption) {
        // Hide all wrappers
        listWrapper.classList.remove('visible');
        listOption.classList.remove('chosen');

        pieWrapper.classList.remove('visible');
        pieOption.classList.remove('chosen');

        barWrapper.classList.remove('visible');
        barOption.classList.remove('chosen');

        // Show the selected wrapper
        wrapperToShow.classList.add('visible');
        chosenOption.classList.add('chosen');
    }

    // Attach event listeners to each option
    listOption.addEventListener('click', () => showVisualization(listWrapper, listOption));
    pieOption.addEventListener('click', () => showVisualization(pieWrapper, pieOption));
    barOption.addEventListener('click', () => showVisualization(barWrapper, barOption));

    // Optionally, set an initial visible wrapper (e.g., list view)
    showVisualization(listWrapper, listOption);

    // Ensure `chartData` is defined
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
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
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

    // Bar Chart
    const barCtx = document.getElementById('BarChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: chartData.titles,
            datasets: [{
                label: 'Price',
                data: chartData.prices,
                backgroundColor: '#36A2EB',
                borderColor: '#36A2EB',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
