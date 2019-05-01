$.ajax({
    type: 'GET',
    dataType: "json",
    url: $('#pieChart').data("url"),
    success: function (response) {
        console.log(response)
        var labels = response.labels
        var data = response.data
        var ctx = document.getElementById('pieChart').getContext('2d');
        var theHelp = Chart.helpers;
        $(window).on('load', function () {
            var pieChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '# клеток',
                        data: data,
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
                    cutoutPercentage: 40,
                    animation: {
                        animateRotate: true,
                        animateScale: true,
                    },
                    legend: {
                        display: false,
                    }
                },
            });
        });
    }
});
