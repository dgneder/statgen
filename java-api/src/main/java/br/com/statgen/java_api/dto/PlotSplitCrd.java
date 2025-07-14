// statgen/java-api/src/main/java/br/com/statgen/java_api/dto/PlotSplitCrd.java
package br.com.statgen.java_api.dto;

public class PlotSplitCrd {
    private int plot;
    private int repetition;
    private String mainPlotTreatment; // Fator A
    private String subplotTreatment;  // Fator B

    public PlotSplitCrd(int plot, int repetition, String mainPlotTreatment, String subplotTreatment) {
        this.plot = plot;
        this.repetition = repetition;
        this.mainPlotTreatment = mainPlotTreatment;
        this.subplotTreatment = subplotTreatment;
    }

    // Adicione Getters para todos os 4 campos...
    public int getPlot() { return plot; }
    public int getRepetition() { return repetition; }
    public String getMainPlotTreatment() { return mainPlotTreatment; }
    public String getSubplotTreatment() { return subplotTreatment; }
}

