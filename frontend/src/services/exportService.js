import jsPDF from "jspdf";
import "jspdf-autotable";

export const exportService = {
  /**
   * Exportar proyecto a PDF
   */
  async exportarProyectoPDF(proyecto, gastos = []) {
    try {
      const doc = new jsPDF("p", "mm", "a4");
      const pageWidth = doc.internal.pageSize.getWidth();
      const margin = 20;
      let yPosition = 20;

      // Configuración de fuentes
      doc.setFont("helvetica");

      // ============= ENCABEZADO =============
      // Logo (opcional - puedes agregar una imagen)
      doc.setFillColor(102, 126, 234); // Color primario
      doc.rect(0, 0, pageWidth, 40, "F");

      doc.setTextColor(255, 255, 255);
      doc.setFontSize(24);
      doc.setFont("helvetica", "bold");
      doc.text("SIGPP - Universidad de Cartagena", margin, 15);

      doc.setFontSize(14);
      doc.setFont("helvetica", "normal");
      doc.text("Sistema de Gestión de Proyectos de Grado", margin, 25);

      // Fecha de generación
      doc.setFontSize(10);
      doc.text(
        `Generado el: ${new Date().toLocaleDateString("es-CO", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
        })}`,
        margin,
        33
      );

      yPosition = 50;

      // ============= INFORMACIÓN DEL PROYECTO =============
      doc.setTextColor(0, 0, 0);
      doc.setFontSize(20);
      doc.setFont("helvetica", "bold");
      doc.text("INFORMACIÓN DEL PROYECTO", margin, yPosition);
      yPosition += 10;

      // Línea decorativa
      doc.setDrawColor(102, 126, 234);
      doc.setLineWidth(1);
      doc.line(margin, yPosition, pageWidth - margin, yPosition);
      yPosition += 8;

      // Código y Estado
      doc.setFontSize(11);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(102, 126, 234);
      doc.text("Código del Proyecto:", margin, yPosition);
      doc.setFont("helvetica", "normal");
      doc.setTextColor(0, 0, 0);
      doc.text(proyecto.codigo_proyecto, margin + 50, yPosition);

      doc.setFont("helvetica", "bold");
      doc.setTextColor(102, 126, 234);
      doc.text("Estado:", pageWidth - margin - 50, yPosition);
      doc.setFont("helvetica", "normal");
      doc.setTextColor(0, 0, 0);
      doc.text(
        this.formatEstado(proyecto.estado),
        pageWidth - margin - 25,
        yPosition
      );
      yPosition += 8;

      // Nombre del proyecto
      doc.setFontSize(16);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(0, 0, 0);
      const nombreLines = doc.splitTextToSize(
        proyecto.nombre,
        pageWidth - 2 * margin
      );
      doc.text(nombreLines, margin, yPosition);
      yPosition += nombreLines.length * 8 + 5;

      // Descripción
      doc.setFontSize(11);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(102, 126, 234);
      doc.text("Descripción:", margin, yPosition);
      yPosition += 6;

      doc.setFont("helvetica", "normal");
      doc.setTextColor(60, 60, 60);
      const descripcionLines = doc.splitTextToSize(
        proyecto.descripcion,
        pageWidth - 2 * margin
      );
      doc.text(descripcionLines, margin, yPosition);
      yPosition += descripcionLines.length * 5 + 8;

      // Objetivos
      doc.setFont("helvetica", "bold");
      doc.setTextColor(102, 126, 234);
      doc.text("Objetivos:", margin, yPosition);
      yPosition += 6;

      doc.setFont("helvetica", "normal");
      doc.setTextColor(60, 60, 60);
      const objetivosLines = doc.splitTextToSize(
        proyecto.objetivos,
        pageWidth - 2 * margin
      );
      doc.text(objetivosLines, margin, yPosition);
      yPosition += objetivosLines.length * 5 + 10;

      // Verificar si necesitamos nueva página
      if (yPosition > 250) {
        doc.addPage();
        yPosition = 20;
      }

      // Información adicional en tabla
      doc.autoTable({
        startY: yPosition,
        head: [["Campo", "Información"]],
        body: [
          ["Profesor Asesor", proyecto.profesor_nombre || "Sin asignar"],
          [
            "Fecha de Creación",
            new Date(proyecto.fecha_creacion).toLocaleDateString("es-CO"),
          ],
          [
            "Última Modificación",
            new Date(proyecto.fecha_ultima_modificacion).toLocaleDateString(
              "es-CO"
            ),
          ],
        ],
        theme: "grid",
        headStyles: {
          fillColor: [102, 126, 234],
          textColor: 255,
          fontSize: 11,
          fontStyle: "bold",
        },
        bodyStyles: {
          fontSize: 10,
        },
        margin: { left: margin, right: margin },
      });

      yPosition = doc.lastAutoTable.finalY + 15;

      // ============= PRESUPUESTO =============
      doc.addPage();
      yPosition = 20;

      doc.setFontSize(18);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(0, 0, 0);
      doc.text("PRESUPUESTO DEL PROYECTO", margin, yPosition);
      yPosition += 10;

      doc.setDrawColor(102, 126, 234);
      doc.setLineWidth(1);
      doc.line(margin, yPosition, pageWidth - margin, yPosition);
      yPosition += 10;

      // Tabla de resumen presupuestal
      const saldoDisponible =
        (proyecto.presupuesto_asignado || 0) - proyecto.presupuesto_ejecutado;

      doc.autoTable({
        startY: yPosition,
        head: [["Concepto", "Monto (COP)"]],
        body: [
          [
            "Presupuesto Estimado",
            this.formatMoney(proyecto.presupuesto_estimado),
          ],
          [
            "Presupuesto Asignado",
            this.formatMoney(proyecto.presupuesto_asignado || 0),
          ],
          [
            "Presupuesto Ejecutado",
            this.formatMoney(proyecto.presupuesto_ejecutado),
          ],
          ["Saldo Disponible", this.formatMoney(saldoDisponible)],
        ],
        theme: "striped",
        headStyles: {
          fillColor: [16, 185, 129],
          textColor: 255,
          fontSize: 11,
          fontStyle: "bold",
        },
        bodyStyles: {
          fontSize: 11,
        },
        columnStyles: {
          1: { halign: "right", fontStyle: "bold" },
        },
        margin: { left: margin, right: margin },
      });

      yPosition = doc.lastAutoTable.finalY + 15;

      // Items del presupuesto
      if (proyecto.items_presupuesto && proyecto.items_presupuesto.length > 0) {
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.text("Desglose del Presupuesto", margin, yPosition);
        yPosition += 8;

        const itemsData = proyecto.items_presupuesto.map((item, index) => [
          `Item ${index + 1}`,
          item.concepto,
          item.justificacion,
          this.formatMoney(item.costo),
        ]);

        doc.autoTable({
          startY: yPosition,
          head: [["#", "Concepto", "Justificación", "Costo (COP)"]],
          body: itemsData,
          theme: "grid",
          headStyles: {
            fillColor: [102, 126, 234],
            textColor: 255,
            fontSize: 10,
            fontStyle: "bold",
          },
          bodyStyles: {
            fontSize: 9,
          },
          columnStyles: {
            0: { cellWidth: 20, halign: "center" },
            1: { cellWidth: 40 },
            2: { cellWidth: 80 },
            3: { cellWidth: 30, halign: "right", fontStyle: "bold" },
          },
          margin: { left: margin, right: margin },
        });

        // Total
        yPosition = doc.lastAutoTable.finalY + 5;
        const totalPresupuesto = proyecto.items_presupuesto.reduce(
          (sum, item) => sum + (item.costo || 0),
          0
        );

        doc.setFillColor(102, 126, 234);
        doc.rect(margin, yPosition, pageWidth - 2 * margin, 10, "F");

        doc.setTextColor(255, 255, 255);
        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.text("TOTAL PRESUPUESTO:", margin + 5, yPosition + 7);
        doc.text(
          this.formatMoney(totalPresupuesto),
          pageWidth - margin - 5,
          yPosition + 7,
          { align: "right" }
        );
      }

      // ============= GASTOS =============
      if (gastos && gastos.length > 0) {
        doc.addPage();
        yPosition = 20;

        doc.setTextColor(0, 0, 0);
        doc.setFontSize(18);
        doc.setFont("helvetica", "bold");
        doc.text("GASTOS REGISTRADOS", margin, yPosition);
        yPosition += 10;

        doc.setDrawColor(102, 126, 234);
        doc.setLineWidth(1);
        doc.line(margin, yPosition, pageWidth - margin, yPosition);
        yPosition += 10;

        const gastosData = gastos.map((gasto) => [
          `#${gasto.id}`,
          gasto.concepto,
          this.formatMoney(gasto.monto),
          this.formatEstado(gasto.estado),
          new Date(gasto.creado_en).toLocaleDateString("es-CO"),
        ]);

        doc.autoTable({
          startY: yPosition,
          head: [["ID", "Concepto", "Monto (COP)", "Estado", "Fecha"]],
          body: gastosData,
          theme: "striped",
          headStyles: {
            fillColor: [239, 68, 68],
            textColor: 255,
            fontSize: 10,
            fontStyle: "bold",
          },
          bodyStyles: {
            fontSize: 9,
          },
          columnStyles: {
            0: { cellWidth: 20, halign: "center" },
            1: { cellWidth: 70 },
            2: { cellWidth: 30, halign: "right", fontStyle: "bold" },
            3: { cellWidth: 30, halign: "center" },
            4: { cellWidth: 30, halign: "center" },
          },
          margin: { left: margin, right: margin },
        });

        // Resumen de gastos
        yPosition = doc.lastAutoTable.finalY + 10;
        const totalGastos = gastos.reduce(
          (sum, g) => sum + parseFloat(g.monto || 0),
          0
        );
        const gastosAprobados = gastos.filter(
          (g) => g.estado === "aprobado"
        ).length;
        const gastosPendientes = gastos.filter(
          (g) => g.estado === "pendiente"
        ).length;

        doc.autoTable({
          startY: yPosition,
          body: [
            ["Total de Gastos:", gastos.length.toString()],
            ["Gastos Aprobados:", gastosAprobados.toString()],
            ["Gastos Pendientes:", gastosPendientes.toString()],
            ["Monto Total:", this.formatMoney(totalGastos)],
          ],
          theme: "plain",
          bodyStyles: {
            fontSize: 11,
            fontStyle: "bold",
          },
          columnStyles: {
            0: { cellWidth: 50 },
            1: { cellWidth: 50, halign: "right" },
          },
          margin: { left: pageWidth - margin - 100 },
        });
      }

      // ============= PIE DE PÁGINA =============
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(128, 128, 128);
        doc.text(
          `Página ${i} de ${pageCount} | SIGPP - Universidad de Cartagena`,
          pageWidth / 2,
          doc.internal.pageSize.getHeight() - 10,
          { align: "center" }
        );
      }

      // Guardar PDF
      const filename = `Proyecto_${
        proyecto.codigo_proyecto
      }_${new Date().getTime()}.pdf`;
      doc.save(filename);

      return { success: true, filename };
    } catch (error) {
      console.error("Error al generar PDF:", error);
      throw new Error("No se pudo generar el PDF");
    }
  },

  /**
   * Exportar gastos a Excel (CSV)
   */
  exportarGastosCSV(gastos, nombreProyecto) {
    const headers = [
      "ID",
      "Concepto",
      "Monto",
      "Estado",
      "Fecha",
      "Soporte URL",
    ];
    const rows = gastos.map((gasto) => [
      gasto.id,
      gasto.concepto,
      gasto.monto,
      this.formatEstado(gasto.estado),
      new Date(gasto.creado_en).toLocaleDateString("es-CO"),
      gasto.soporte_url || "N/A",
    ]);

    let csvContent = headers.join(",") + "\n";
    rows.forEach((row) => {
      csvContent += row.map((cell) => `"${cell}"`).join(",") + "\n";
    });

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute(
      "download",
      `Gastos_${nombreProyecto}_${new Date().getTime()}.csv`
    );
    link.style.visibility = "hidden";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },

  /**
   * Exportar items de presupuesto a Excel (CSV)
   */
  exportarPresupuestoCSV(items, nombreProyecto) {
    const headers = ["Item", "Concepto", "Justificación", "Costo"];
    const rows = items.map((item, index) => [
      `Item ${index + 1}`,
      item.concepto,
      item.justificacion,
      item.costo,
    ]);

    let csvContent = headers.join(",") + "\n";
    rows.forEach((row) => {
      csvContent += row.map((cell) => `"${cell}"`).join(",") + "\n";
    });

    const totalPresupuesto = items.reduce(
      (sum, item) => sum + (item.costo || 0),
      0
    );
    csvContent += `\n"TOTAL","","","${totalPresupuesto}"\n`;

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);

    link.setAttribute("href", url);
    link.setAttribute(
      "download",
      `Presupuesto_${nombreProyecto}_${new Date().getTime()}.csv`
    );
    link.style.visibility = "hidden";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },

  // Utilidades
  formatMoney(value) {
    return (
      "$" +
      new Intl.NumberFormat("es-CO", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value || 0)
    );
  },

  formatEstado(estado) {
    const estados = {
      borrador: "Borrador",
      pendiente_validacion: "Pendiente de Validación",
      validado_asesor: "Validado por Asesor",
      activo: "Activo",
      rechazado: "Rechazado",
      finalizado: "Finalizado",
      pendiente: "Pendiente",
      aprobado: "Aprobado",
    };
    return estados[estado] || estado;
  },
};
