package br.com.statgen.java_api.service;

import org.springframework.stereotype.Service;
import br.com.statgen.java_api.dto.FactorialRequest;
import br.com.statgen.java_api.dto.Plot;
import br.com.statgen.java_api.dto.PlotAugmented;
import br.com.statgen.java_api.dto.AugmentedBlockRequest;
import br.com.statgen.java_api.dto.FactorialAxBRequest;
import br.com.statgen.java_api.dto.PlotAxB;
import br.com.statgen.java_api.dto.PlotSplitCrd;
import br.com.statgen.java_api.dto.PlotSplitPlot;
import br.com.statgen.java_api.dto.PlotSplitSplit;
import br.com.statgen.java_api.dto.PlotSplitSplitCrd;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class RandomizationService {

    // --- PRIMEIRO MÉTODO (DIC em FATORIAL AxBxC) ---
    public List<Plot> generateFactorialCrd(FactorialRequest request) {
        int a = request.getLevelsA();
        int b = request.getLevelsB();
        int c = request.getLevelsC();
        int r = request.getRepetitions();

        if (a > 100 || b > 100 || c > 100 || r > 100 || a < 1 || b < 1 || c < 1 || r < 1) {
            throw new IllegalArgumentException("Níveis dos fatores e repetições devem estar entre 1 e 100.");
        }

        List<String> allCombinations = new ArrayList<>();
        for (int i = 1; i <= a; i++) {
            for (int j = 1; j <= b; j++) {
                for (int l = 1; l <= c; l++) {
                    allCombinations.add(String.format("A%d-B%d-C%d", i, j, l));
                }
            }
        }

        List<String> fullLayout = new ArrayList<>();
        for (int i = 0; i < r; i++) {
            fullLayout.addAll(allCombinations);
        }

        Collections.shuffle(fullLayout);

        List<Plot> finalLayout = new ArrayList<>();
        Map<String, Integer> repetitionCounter = new HashMap<>();
        for (int i = 0; i < fullLayout.size(); i++) {
            String combination = fullLayout.get(i);
            int currentRep = repetitionCounter.getOrDefault(combination, 0) + 1;
            repetitionCounter.put(combination, currentRep);
            
            String[] factors = combination.split("-");
            
            finalLayout.add(new Plot(
                i + 1,
                currentRep,
                factors[0],
                factors[1],
                factors[2]
            ));
        }
        return finalLayout;
    }

    // --- SEGUNDO MÉTODO (FATORIAL AxB em Blocos) ---
    // Ele agora está DENTRO da classe RandomizationService
    public List<PlotAxB> generateFactorialRcbd(FactorialAxBRequest request) {
        int a = request.getLevelsA();
        int b = request.getLevelsB();
        int r = request.getRepetitions();

        if (a > 100 || b > 100 || r > 100 || a < 1 || b < 1 || r < 1) {
            throw new IllegalArgumentException("Níveis dos fatores e repetições devem estar entre 1 e 100.");
        }

        List<String> treatmentCombinations = new ArrayList<>();
        for (int i = 1; i <= a; i++) {
            for (int j = 1; j <= b; j++) {
                treatmentCombinations.add(String.format("A%d-B%d", i, j));
            }
        }

        List<String> fullRandomizedLayout = new ArrayList<>();
        for (int i = 0; i < r; i++) {
            List<String> blockTreatments = new ArrayList<>(treatmentCombinations);
            Collections.shuffle(blockTreatments);
            fullRandomizedLayout.addAll(blockTreatments);
        }
        
        List<PlotAxB> finalLayout = new ArrayList<>();
        for (int i = 0; i < fullRandomizedLayout.size(); i++) {
            String combination = fullRandomizedLayout.get(i);
            String[] factors = combination.split("-");
            
            int currentBlock = (i / treatmentCombinations.size()) + 1;
            
            finalLayout.add(new PlotAxB(
                i + 1,
                currentBlock,
                factors[0],
                factors[1]
            ));
        }
        return finalLayout;
    }
    // DBC em Fatorial Triplo
    public List<Plot> generateFactorialRcbdAxbxc(FactorialRequest request) {
    int a = request.getLevelsA();
    int b = request.getLevelsB();
    int c = request.getLevelsC();
    int r = request.getRepetitions(); // Repetições são os blocos

    // Validação dos limites
    if (a > 100 || b > 100 || c > 100 || r > 100 || a < 1 || b < 1 || c < 1 || r < 1) {
        throw new IllegalArgumentException("Níveis dos fatores e repetições devem estar entre 1 e 100.");
    }

    // 1. Gera a lista com todas as combinações de tratamentos
    List<String> treatmentCombinations = new ArrayList<>();
    for (int i = 1; i <= a; i++) {
        for (int j = 1; j <= b; j++) {
            for (int l = 1; l <= c; l++) {
                treatmentCombinations.add(String.format("A%d-B%d-C%d", i, j, l));
            }
        }
    }

    // 2. Lógica de Blocos: para cada bloco (repetição), embaralha os tratamentos
    List<String> fullRandomizedLayout = new ArrayList<>();
    for (int i = 0; i < r; i++) {
        List<String> blockTreatments = new ArrayList<>(treatmentCombinations);
        Collections.shuffle(blockTreatments);
        fullRandomizedLayout.addAll(blockTreatments);
    }

    // 3. Monta a resposta final
    List<Plot> finalLayout = new ArrayList<>();
    for (int i = 0; i < fullRandomizedLayout.size(); i++) {
        String combination = fullRandomizedLayout.get(i);
        String[] factors = combination.split("-");

        // Calcula o bloco/repetição atual
        int currentBlock = (i / treatmentCombinations.size()) + 1;

        finalLayout.add(new Plot(
            i + 1,       // Parcela
            currentBlock,
            factors[0],  // Fator A
            factors[1],  // Fator B
            factors[2]   // Fator C
        ));
    }

    return finalLayout;
    }

    public List<PlotSplitPlot> generateSplitPlotRcbd(FactorialAxBRequest request) {
    int levelsA = request.getLevelsA(); // Tratamentos da Parcela
    int levelsB = request.getLevelsB(); // Tratamentos da Subparcela
    int r = request.getRepetitions();   // Blocos

    if (levelsA > 100 || levelsB > 100 || r > 100 || levelsA < 1 || levelsB < 1 || r < 1) {
        throw new IllegalArgumentException("Fatores e blocos devem estar entre 1 e 100.");
    }

    // 1. Gera os nomes dos tratamentos para cada fator
    List<String> mainPlotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsA; i++) { mainPlotTreatments.add("A" + i); }

    List<String> subplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsB; i++) { subplotTreatments.add("B" + i); }

    // 2. Executa a lógica de casualização aninhada
    List<PlotSplitPlot> finalLayout = new ArrayList<>();
    int plotCounter = 1;

    for (int blockNum = 1; blockNum <= r; blockNum++) {
        // Randomiza os tratamentos da PARCELA PRINCIPAL dentro deste bloco
        List<String> shuffledMainPlots = new ArrayList<>(mainPlotTreatments);
        Collections.shuffle(shuffledMainPlots);

        for (String mainPlot : shuffledMainPlots) {
            // Randomiza os tratamentos da SUBPARCELA dentro desta parcela principal
            List<String> shuffledSubplots = new ArrayList<>(subplotTreatments);
            Collections.shuffle(shuffledSubplots);
            
            for (String subplot : shuffledSubplots) {
                finalLayout.add(new PlotSplitPlot(
                    plotCounter++,
                    blockNum,
                    mainPlot,
                    subplot
                ));
            }
        }
    }
    return finalLayout;
    }
// Adicione este método dentro da classe RandomizationService
public List<PlotSplitSplit> generateSplitSplitPlotRcbd(FactorialRequest request) {
    int levelsA = request.getLevelsA();
    int levelsB = request.getLevelsB();
    int levelsC = request.getLevelsC();
    int r = request.getRepetitions();

    // Validação dos limites
    if (levelsA > 100 || levelsB > 100 || levelsC > 100 || r > 100 || levelsA < 1 || levelsB < 1 || levelsC < 1 || r < 1) {
        throw new IllegalArgumentException("Fatores e blocos devem estar entre 1 e 100.");
    }

    // 1. Gera os nomes dos tratamentos para cada fator
    List<String> mainPlotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsA; i++) { mainPlotTreatments.add("A" + i); }

    List<String> subplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsB; i++) { subplotTreatments.add("B" + i); }

    List<String> subSubplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsC; i++) { subSubplotTreatments.add("C" + i); }

    // 2. Lógica da casualização triplamente aninhada
    List<PlotSplitSplit> finalLayout = new ArrayList<>();
    int plotCounter = 1;

    for (int blockNum = 1; blockNum <= r; blockNum++) {
        List<String> shuffledMainPlots = new ArrayList<>(mainPlotTreatments);
        Collections.shuffle(shuffledMainPlots); // Randomiza Fator A dentro do bloco

        for (String mainPlot : shuffledMainPlots) {
            List<String> shuffledSubplots = new ArrayList<>(subplotTreatments);
            Collections.shuffle(shuffledSubplots); // Randomiza Fator B dentro da parcela principal

            for (String subplot : shuffledSubplots) {
                List<String> shuffledSubSubplots = new ArrayList<>(subSubplotTreatments);
                Collections.shuffle(shuffledSubSubplots); // Randomiza Fator C dentro da subparcela

                for (String subSubplot : shuffledSubSubplots) {
                    finalLayout.add(new PlotSplitSplit(
                        plotCounter++,
                        blockNum,
                        mainPlot,
                        subplot,
                        subSubplot
                    ));
                }
            }
        }
    }
    return finalLayout;
    }
    public List<PlotSplitCrd> generateSplitPlotCrd(FactorialAxBRequest request) {
    int levelsA = request.getLevelsA();
    int levelsB = request.getLevelsB();
    int r = request.getRepetitions();

    if (levelsA > 100 || levelsB > 100 || r > 100 || levelsA < 1 || levelsB < 1 || r < 1) {
        throw new IllegalArgumentException("Fatores e repetições devem estar entre 1 e 100.");
    }

    // 1. Gera os nomes dos tratamentos
    List<String> mainPlotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsA; i++) { mainPlotTreatments.add("A" + i); }

    List<String> subplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsB; i++) { subplotTreatments.add("B" + i); }

    // 2. Cria a lista completa de todas as parcelas principais (A * r)
    List<String> allMainPlots = new ArrayList<>();
    for (int i = 0; i < r; i++) {
        allMainPlots.addAll(mainPlotTreatments);
    }

    // 3. Randomiza completamente a ordem das parcelas principais
    Collections.shuffle(allMainPlots);

    // 4. Monta o layout final, randomizando as subparcelas dentro de cada parcela principal
    List<PlotSplitCrd> finalLayout = new ArrayList<>();
    Map<String, Integer> repetitionCounter = new HashMap<>();
    
    for (int i = 0; i < allMainPlots.size(); i++) {
        String mainPlot = allMainPlots.get(i);
        
        // Randomiza os tratamentos da SUBPARCELA para esta instância da parcela principal
        List<String> shuffledSubplots = new ArrayList<>(subplotTreatments);
        Collections.shuffle(shuffledSubplots);

        // Calcula a repetição para a parcela principal
        int currentRep = repetitionCounter.getOrDefault(mainPlot, 0) + 1;
        repetitionCounter.put(mainPlot, currentRep);

        for (int j = 0; j < shuffledSubplots.size(); j++) {
            finalLayout.add(new PlotSplitCrd(
                (i * levelsB) + j + 1, // Calcula o número da parcela global
                currentRep,
                mainPlot,
                shuffledSubplots.get(j)
            ));
        }
    }
    
    return finalLayout;
}

public List<PlotSplitSplitCrd> generateSplitSplitPlotCrd(FactorialRequest request) {
    int levelsA = request.getLevelsA();
    int levelsB = request.getLevelsB();
    int levelsC = request.getLevelsC();
    int r = request.getRepetitions();

    // Validação
    if (levelsA > 100 || levelsB > 100 || levelsC > 100 || r > 100 || levelsA < 1 || levelsB < 1 || levelsC < 1 || r < 1) {
        throw new IllegalArgumentException("Fatores e repetições devem estar entre 1 e 100.");
    }

    // Gera os nomes dos tratamentos
    List<String> mainPlotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsA; i++) { mainPlotTreatments.add("A" + i); }

    List<String> subplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsB; i++) { subplotTreatments.add("B" + i); }

    List<String> subSubplotTreatments = new ArrayList<>();
    for (int i = 1; i <= levelsC; i++) { subSubplotTreatments.add("C" + i); }

    // Cria a lista completa de unidades da parcela principal (A x r)
    List<String> allMainPlots = new ArrayList<>();
    for (int i = 0; i < r; i++) {
        allMainPlots.addAll(mainPlotTreatments);
    }
    
    // Casualiza completamente as parcelas principais (lógica do DIC)
    Collections.shuffle(allMainPlots);

    // Monta o layout final
    List<PlotSplitSplitCrd> finalLayout = new ArrayList<>();
    Map<String, Integer> repetitionCounter = new HashMap<>();
    int plotCounter = 1;
    
    for (String mainPlot : allMainPlots) {
        // Para cada parcela principal, casualiza as subparcelas
        List<String> shuffledSubplots = new ArrayList<>(subplotTreatments);
        Collections.shuffle(shuffledSubplots);
        
        // Calcula a repetição correta para a parcela principal
        int currentRep = repetitionCounter.getOrDefault(mainPlot, 0) + 1;
        repetitionCounter.put(mainPlot, currentRep);

        for (String subplot : shuffledSubplots) {
            // Para cada subparcela, casualiza as sub-subparcelas
            List<String> shuffledSubSubplots = new ArrayList<>(subSubplotTreatments);
            Collections.shuffle(shuffledSubSubplots);

            for (String subSubplot : shuffledSubSubplots) {
                finalLayout.add(new PlotSplitSplitCrd(
                    plotCounter++,
                    currentRep,
                    mainPlot,
                    subplot,
                    subSubplot
                ));
            }
        }
    }
    return finalLayout;
}

public List<PlotAugmented> generateAugmentedBlockLayout(AugmentedBlockRequest request) {
    int t = request.getNewTreatments();
    int c = request.getCheckTreatments();
    int b = request.getBlocks();

    // Validação
    if (t <= 0 || c <= 0 || b <= 0 || t > 1000 || c > 1000 || b > 100) {
        throw new IllegalArgumentException("Parâmetros devem ser positivos e dentro dos limites.");
    }
    if (t % b != 0) {
        throw new IllegalArgumentException("O número de Novos Tratamentos deve ser um múltiplo do número de Blocos.");
    }

    // 1. Cria as listas de nomes
    List<String> checkLabels = new ArrayList<>();
    for (int i = 1; i <= c; i++) { checkLabels.add("C" + i); }

    List<String> newLabels = new ArrayList<>();
    for (int i = 1; i <= t; i++) { newLabels.add("T" + i); }

    // 2. Randomiza e particiona os novos tratamentos
    Collections.shuffle(newLabels);
    List<List<String>> newTreatmentsPerBlock = new ArrayList<>();
    int newTreatmentsPerBlockSize = t / b;
    for (int i = 0; i < t; i += newTreatmentsPerBlockSize) {
        newTreatmentsPerBlock.add(newLabels.subList(i, i + newTreatmentsPerBlockSize));
    }
    
    // 3. Monta o layout final
    List<PlotAugmented> finalLayout = new ArrayList<>();
    int plotCounter = 1;

    for (int i = 0; i < b; i++) {
        // Para cada bloco, pega todas as testemunhas e uma partição dos novos tratamentos
        List<String> currentBlockTreatments = new ArrayList<>(checkLabels);
        currentBlockTreatments.addAll(newTreatmentsPerBlock.get(i));
        
        // Randomiza a ordem de todos os tratamentos dentro do bloco
        Collections.shuffle(currentBlockTreatments);
        
        for (String treatment : currentBlockTreatments) {
            String type = treatment.startsWith("C") ? "Testemunha" : "Tratamento";
            finalLayout.add(new PlotAugmented(
                plotCounter++,
                i + 1, // Número do Bloco
                treatment,
                type
            ));
        }
    }
    return finalLayout;
}
    
} // <-- A CHAVE DE FECHAMENTO DA CLASSE AGORA ESTÁ AQUI, NO FINAL DO ARQUIVO.