// statgen/java-api/src/main/java/br/com/statgen/java_api/RandomizationController.java
package br.com.statgen.java_api.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import br.com.statgen.java_api.dto.AugmentedBlockRequest;
import br.com.statgen.java_api.dto.FactorialAxBRequest;
import br.com.statgen.java_api.dto.FactorialRequest;
import br.com.statgen.java_api.dto.Plot;
import br.com.statgen.java_api.dto.PlotAugmented;
import br.com.statgen.java_api.dto.PlotAxB;
import br.com.statgen.java_api.dto.PlotSplitCrd;
import br.com.statgen.java_api.dto.PlotSplitPlot;
import br.com.statgen.java_api.dto.PlotSplitSplit;
import br.com.statgen.java_api.dto.PlotSplitSplitCrd;
import br.com.statgen.java_api.service.RandomizationService;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/randomize")
public class RandomizationController {

    private final RandomizationService randomizationService;

    // Injeção de dependência do nosso serviço
    public RandomizationController(RandomizationService randomizationService) {
        this.randomizationService = randomizationService;
    }

    @PostMapping("/factorial-crd-axbxc")
    public ResponseEntity<?> createFactorialCrd(@RequestBody FactorialRequest request) {
        try {
            List<Plot> layout = randomizationService.generateFactorialCrd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            // Retorna um erro 400 Bad Request com a mensagem da validação
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    @PostMapping("/factorial-rcbd-axb")
    public ResponseEntity<?> createFactorialRcbd(@RequestBody FactorialAxBRequest request) {
        try {
            List<PlotAxB> layout = randomizationService.generateFactorialRcbd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    @PostMapping("/factorial-rcbd-axbxc")
    public ResponseEntity<?> createFactorialRcbdAxbxc(@RequestBody FactorialRequest request) {
        try {
            List<Plot> layout = randomizationService.generateFactorialRcbdAxbxc(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    @PostMapping("/split-plot-rcbd")
    public ResponseEntity<?> createSplitPlotRcbd(@RequestBody FactorialAxBRequest request) {
        try {
            List<PlotSplitPlot> layout = randomizationService.generateSplitPlotRcbd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    @PostMapping("/split-split-plot-rcbd")
    public ResponseEntity<?> createSplitSplitPlotRcbd(@RequestBody FactorialRequest request) {
        try {
            List<PlotSplitSplit> layout = randomizationService.generateSplitSplitPlotRcbd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/split-plot-crd")
    public ResponseEntity<?> createSplitPlotCrd(@RequestBody FactorialAxBRequest request) {
        try {
            List<PlotSplitCrd> layout = randomizationService.generateSplitPlotCrd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }

    @PostMapping("/split-split-plot-crd")
    public ResponseEntity<?> createSplitSplitPlotCrd(@RequestBody FactorialRequest request) {
        try {
            List<PlotSplitSplitCrd> layout = randomizationService.generateSplitSplitPlotCrd(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    @PostMapping("/augmented-block")
    public ResponseEntity<?> createAugmentedBlockLayout(@RequestBody AugmentedBlockRequest request) {
        try {
            List<PlotAugmented> layout = randomizationService.generateAugmentedBlockLayout(request);
            return ResponseEntity.ok(layout);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
