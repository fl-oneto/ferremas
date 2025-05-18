/// Bodeguero /////

document.addEventListener('DOMContentLoaded', function () {

    const pedidosElement = document.getElementById('pedidos');

    if (pedidosElement) {
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
    }

/// VENDEDOR /////
    const vendedorElement = document.getElementById('vendedor');

    
    if (vendedorElement) {
    const vendedorData = {
    pendientes: parseInt(vendedorElement.dataset.pendientes),
    despachados: parseInt(vendedorElement.dataset.despachados)
  };

   const sumtotalpedidos = vendedorData.pendientes + vendedorData.despachados;

  Highcharts.chart('vendedor',{
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie'
    },
    title: {
      text: 'Estado de pedidos (' + sumtotalpedidos + ')'
    },
    tooltip: {
      pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    accessibility: {
      point: { valueSuffix: '%' }
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
          format: '{point.percentage:.1f}%',
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
          name: 'Por Aprobar (' + vendedorData.pendientes + ')',
          y: vendedorData.pendientes
        },
        {
          name: 'Por Despacho (' + vendedorData.despachados + ')',
          y: vendedorData.despachados
        }
      ]
    }]
  });
}
});