package br.com.statgen.java_api.dto;

public class FactorialAxBRequest {
    // --- Campos Privados ---
    private int levelsA;
    private int levelsB;
    private int repetitions;

    // --- Getters (para ler os valores) ---
    public int getLevelsA() {
        return levelsA;
    }

    public int getLevelsB() {
        return levelsB;
    }

    public int getRepetitions() {
        return repetitions;
    }
    
    // --- Setters (para o Spring poder escrever os valores do JSON) ---
    public void setLevelsA(int levelsA) {
        this.levelsA = levelsA;
    }

    public void setLevelsB(int levelsB) {
        this.levelsB = levelsB;
    }

    public void setRepetitions(int repetitions) {
        this.repetitions = repetitions;
    }
}