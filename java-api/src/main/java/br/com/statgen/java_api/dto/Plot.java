// statgen/java-api/src/main/java/br/com/statgen/java_api/Plot.java
package br.com.statgen.java_api.dto;

public class Plot {
    private int plot;
    private int repetition;
    private String factorA;
    private String factorB;
    private String factorC;

    // Construtor
    public Plot(int plot, int repetition, String factorA, String factorB, String factorC) {
        this.plot = plot;
        this.repetition = repetition;
        this.factorA = factorA;
        this.factorB = factorB;
        this.factorC = factorC;
    }

    // Getters
    public int getPlot() { return plot; }
    public int getRepetition() { return repetition; }
    public String getFactorA() { return factorA; }
    public String getFactorB() { return factorB; }
    public String getFactorC() { return factorC; }
}