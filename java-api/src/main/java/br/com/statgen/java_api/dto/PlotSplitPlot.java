// statgen/java-api/src/main/java/br/com/statgen/java_api/dto/PlotSplitPlot.java
package br.com.statgen.java_api.dto;

public class PlotSplitPlot {
    private int plot;
    private int block; // Bloco é a repetição
    private String mainPlotTreatment; // Fator A
    private String subplotTreatment; // Fator B

    public PlotSplitPlot(int plot, int block, String mainPlotTreatment, String subplotTreatment) {
        this.plot = plot;
        this.block = block;
        this.mainPlotTreatment = mainPlotTreatment;
        this.subplotTreatment = subplotTreatment;
    }

    // Adicione Getters para todos os campos...
    public int getPlot() { return plot; }
    public int getBlock() { return block; }
    public String getMainPlotTreatment() { return mainPlotTreatment; }
    public String getSubplotTreatment() { return subplotTreatment; }
}