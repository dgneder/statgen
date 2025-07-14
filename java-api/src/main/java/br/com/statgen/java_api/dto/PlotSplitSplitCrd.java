package br.com.statgen.java_api.dto;

public class PlotSplitSplitCrd {
    private int plot;
    private int repetition;
    private String mainPlotTreatment;
    private String subplotTreatment;
    private String subSubplotTreatment;

    public PlotSplitSplitCrd(int plot, int repetition, String mainPlotTreatment, String subplotTreatment, String subSubplotTreatment) {
        this.plot = plot;
        this.repetition = repetition;
        this.mainPlotTreatment = mainPlotTreatment;
        this.subplotTreatment = subplotTreatment;
        this.subSubplotTreatment = subSubplotTreatment;
    }

    // Getters Completos
    public int getPlot() { return plot; }
    public int getRepetition() { return repetition; }
    public String getMainPlotTreatment() { return mainPlotTreatment; }
    public String getSubplotTreatment() { return subplotTreatment; }
    public String getSubSubplotTreatment() { return subSubplotTreatment; }
}