package br.com.statgen.java_api.dto;

public class PlotAxB {
    // --- Campos Privados ---
    private int plot;
    private int repetition;
    private String factorA;
    private String factorB;

    // --- Construtor ---
    // Usamos um construtor para criar facilmente novos objetos PlotAxB
    public PlotAxB(int plot, int repetition, String factorA, String factorB) {
        this.plot = plot;
        this.repetition = repetition;
        this.factorA = factorA;
        this.factorB = factorB;
    }

    // --- Getters Públicos ---
    // O Spring usará os getters para ler os valores e construir o JSON de resposta
    
    public int getPlot() {
        return plot;
    }

    public int getRepetition() {
        return repetition;
    }

    public String getFactorA() {
        return factorA;
    }

    public String getFactorB() {
        return factorB;
    }
}