// statgen/java-api/src/main/java/br/com/statgen/java_api/dto/PlotSplitSplit.java
package br.com.statgen.java_api.dto;

public class PlotSplitSplit {
    private int plot;
    private int block;
    private String mainPlotTreatment; // Fator A
    private String subplotTreatment;  // Fator B
    private String subSubplotTreatment; // Fator C

    public PlotSplitSplit(int plot, int block, String mainPlotTreatment, String subplotTreatment, String subSubplotTreatment) {
        this.plot = plot;
        this.block = block;
        this.mainPlotTreatment = mainPlotTreatment;
        this.subplotTreatment = subplotTreatment;
        this.subSubplotTreatment = subSubplotTreatment;
    }

    // Adicione Getters para todos os 5 campos...
    public int getPlot() { return plot; }
    public int getBlock() { return block; }
    public String getMainPlotTreatment() { return mainPlotTreatment; }
    public String getSubplotTreatment() { return subplotTreatment; }
    public String getSubSubplotTreatment() { return subSubplotTreatment; }
}