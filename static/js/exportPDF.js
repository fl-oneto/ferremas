document.getElementById('btn-descargar').addEventListener('click', async () => {
  const elem   = document.getElementById('reporte-pdf');   // bloque a exportar
  const canvas = await html2canvas(elem, { scale: 2 });    // mayor resolución
  const img    = canvas.toDataURL('image/png');

  const { jsPDF } = window.jspdf;
  const pdf = new jsPDF({ orientation: 'p', unit: 'pt', format: 'a4' });

  // Ajusta la imagen al ancho de la página manteniendo proporción
  const pageWidth  = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  const imgProps   = pdf.getImageProperties(img);
  const imgHeight  = (imgProps.height * pageWidth) / imgProps.width;

  pdf.addImage(img, 'PNG', 0, 0, pageWidth, imgHeight);
  pdf.save('reporte.pdf');
});
