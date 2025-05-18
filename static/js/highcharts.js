
/// Bodeguero /////
document.addEventListener("DOMContentLoaded", function () {
  const pedidosElement = document.getElementById("pedidos");

  if (pedidosElement) {
    const pedidosData = {
      enPreparacion: parseInt(pedidosElement.dataset.enPreparacion),
      listos: parseInt(pedidosElement.dataset.listos),
    };

    sumtotalpedidos = pedidosData.enPreparacion + pedidosData.listos;

    Highcharts.chart("pedidos", {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: "pie",
      },
      title: {
        text: "Estado de pedidos 'Bodeguero' (" + sumtotalpedidos + ")",
      },
      tooltip: {
        pointFormat: "{series.name}: <b>{point.percentage}%</b>",
      },
      accessibility: {
        point: {
          valueSuffix: "%",
        },
      },
      plotOptions: {
        pie: {
          allowPointSelect: false,
          cursor: "pointer",
          dataLabels: [
            {
              enabled: false,
              distance: 20,
            },
            {
              enabled: true,
              distance: -40,
              format: "{point.percentage}%",
              style: {
                fontSize: "1.1em",
                textOutline: "none",
                opacity: 0.7,
              },
              filter: {
                operator: ">",
                property: "percentage",
                value: 10,
              },
            },
          ],
          showInLegend: true,
        },
      },
      series: [
        {
          name: "Porcentaje",
          colorByPoint: true,
          data: [
            {
              name: "En Preparación" + " (" + pedidosData.enPreparacion + ")",
              y: pedidosData.enPreparacion,
            },
            {
              name: "Listos" + " (" + pedidosData.listos + ")",
              y: pedidosData.listos,
            },
          ],
        },
      ],
    });
  }

  /// VENDEDOR /////
  const vendedorElement = document.getElementById("vendedor");

  if (vendedorElement) {
    const vendedorData = {
      pendientes: parseInt(vendedorElement.dataset.pendientes),
      despachados: parseInt(vendedorElement.dataset.despachados),
    };

    const sumtotalpedidos = vendedorData.pendientes + vendedorData.despachados;

    Highcharts.chart("vendedor", {
      chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: "pie",
      },
      title: {
        text: "Estado de pedidos 'Vendedor' (" + sumtotalpedidos + ")",
      },
      tooltip: {
        pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>",
      },
      accessibility: {
        point: { valueSuffix: "%" },
      },
      plotOptions: {
        pie: {
          allowPointSelect: false,
          cursor: "pointer",
          dataLabels: [
            {
              enabled: false,
              distance: 20,
            },
            {
              enabled: true,
              distance: -40,
              format: "{point.percentage:.1f}%",
              style: {
                fontSize: "1.1em",
                textOutline: "none",
                opacity: 0.7,
              },
              filter: {
                operator: ">",
                property: "percentage",
                value: 10,
              },
            },
          ],
          showInLegend: true,
        },
      },
      series: [
        {
          name: "Porcentaje",
          colorByPoint: true,
          data: [
            {
              name: "Por Aprobar (" + vendedorData.pendientes + ")",
              y: vendedorData.pendientes,
            },
            {
              name: "Por Despacho (" + vendedorData.despachados + ")",
              y: vendedorData.despachados,
            },
          ],
        },
      ],
    });
  }

  const ventasElement = document.getElementById("ventas");
  if (ventasElement) {
    const totals = {
      dayBefore: parseFloat(ventasElement.dataset.before) ,
      yesterday: parseFloat(ventasElement.dataset.yesterday),
      today: parseFloat(ventasElement.dataset.today),
    };

    // Build the date labels (or pull them from more data-* attrs if you prefer)
    const now = new Date();
    const fmt = (d) =>
      d.toLocaleDateString("es-CL", {
        weekday: "short",
        month: "short",
        day: "numeric",
      });
    const labels = [
      fmt(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 2)),
      fmt(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1)),
      fmt(now),
    ];

    // Highcharts column chart
    Highcharts.chart("ventas", {
      chart: { type: "column" },
      title: { text: "Monto Recaudado en CLP (Últimos 3 Días)" },
      xAxis: { categories: labels, crosshair: true },
      yAxis: { title: { text: "Monto" }, allowDecimals: false },
      tooltip: { pointFormat: "<b>${point.y:,.0f}</b>" },
      plotOptions: {
        column: {
          colorByPoint: true,
          dataLabels: { enabled: true, format: "${y:,.0f}" },
        },
      },
      series: [
        {
          name: "Recaudado",
          data: [totals.dayBefore, totals.yesterday, totals.today],
        },
      ],
    });
  }
});
