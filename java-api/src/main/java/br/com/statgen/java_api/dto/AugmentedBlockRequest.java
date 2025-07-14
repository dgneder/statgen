// statgen/java-api/src/main/java/br/com/statgen/java_api/dto/AugmentedBlockRequest.java
package br.com.statgen.java_api.dto;

public class AugmentedBlockRequest {
    private int newTreatments;
    private int checkTreatments;
    private int blocks;

    // Adicione Getters e Setters para todos os 3 campos...
    public int getNewTreatments() { return newTreatments; }
    public void setNewTreatments(int newTreatments) { this.newTreatments = newTreatments; }
    public int getCheckTreatments() { return checkTreatments; }
    public void setCheckTreatments(int checkTreatments) { this.checkTreatments = checkTreatments; }
    public int getBlocks() { return blocks; }
    public void setBlocks(int blocks) { this.blocks = blocks; }
}
