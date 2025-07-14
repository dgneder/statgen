// statgen/java-api/src/main/java/br/com/statgen/java_api/dto/PlotAugmented.java
package br.com.statgen.java_api.dto;

public class PlotAugmented {
    private int plot;
    private int block;
    private String treatment;
    private String type; // "Testemunha" ou "Tratamento"

    public PlotAugmented(int plot, int block, String treatment, String type) {
        this.plot = plot;
        this.block = block;
        this.treatment = treatment;
        this.type = type;
    }

    // Adicione Getters para todos os 4 campos...
    public int getPlot() { return plot; }
    public int getBlock() { return block; }
    public String getTreatment() { return treatment; }
    public String getType() { return type; }
}
