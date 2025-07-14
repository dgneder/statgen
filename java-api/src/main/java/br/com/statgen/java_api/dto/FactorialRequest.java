// statgen/java-api/src/main/java/br/com/statgen/java_api/FactorialRequest.java
package br.com.statgen.java_api.dto;

public class FactorialRequest {
    private int levelsA;
    private int levelsB;
    private int levelsC;
    private int repetitions;

    // Getters e Setters (necessários para o Spring mapear o JSON)
    public int getLevelsA() { return levelsA; }
    public void setLevelsA(int levelsA) { this.levelsA = levelsA; }

    public int getLevelsB() { return levelsB; }
    public void setLevelsB(int levelsB) { this.levelsB = levelsB; }

    public int getLevelsC() { return levelsC; }
    public void setLevelsC(int levelsC) { this.levelsC = levelsC; }

    public int getRepetitions() { return repetitions; }
    public void setRepetitions(int repetitions) { this.repetitions = repetitions; }
}