var ctx = document.getElementById('pieChart').getContext('2d');
var theHelp = Chart.helpers;
var pieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Purple', 'Orange'],
        datasets: [{
            label: '# клеток',
            data: [12, 19, 3, 5, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
        }]
    },
    options: {
        events: ['mousemove', 'touchstart'],
        animation: {
            animateRotate: false,
            animateScale: true,
        },
        legend: {
            display: false,
        }
    },
});
