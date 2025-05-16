document.addEventListener('DOMContentLoaded', function () {
    const pedidosElement = document.getElementById('pedidos');

    const pedidosData = {
        enPreparacion: parseInt(pedidosElement.dataset.enPreparacion),
        listos: parseInt(pedidosElement.dataset.listos)
    };

    sumtotalpedidos = pedidosData.enPreparacion + pedidosData.listos

    Highcharts.chart('pedidos', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Estado de pedidos'+ ' ('+sumtotalpedidos+')'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: false,
                cursor: 'pointer',
                dataLabels: [{
                    enabled: false,
                    distance: 20
                    }, {
                    enabled: true,
                    distance: -40,
                    format: '{point.percentage}%',
                    style: {
                        fontSize: '1.1em',
                        textOutline: 'none',
                        opacity: 0.7
                    },
                    filter: {
                        operator: '>',
                        property: 'percentage',
                        value: 10
                    }
                }],
                showInLegend: true
            }
        },
        series: [{
            name: 'Porcentaje',
            colorByPoint: true,
            data: [
                {
                    name: 'En Preparación'+' ('+pedidosData.enPreparacion+')',
                    y: pedidosData.enPreparacion
                },
                {
                    name: 'Listos'+' ('+pedidosData.listos+')',
                    y: pedidosData.listos
                }
            ]
        }]
    });
});

