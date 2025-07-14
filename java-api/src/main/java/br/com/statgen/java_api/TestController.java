package br.com.statgen.java_api;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController // 1. Anotação que transforma a classe em um controlador de API REST
@RequestMapping("/api") // 2. Define um prefixo de URL para todos os métodos nesta classe
public class TestController {

    // 3. Mapeia requisições GET para /test (que se torna /api/test)
    @GetMapping("/test")
    public Map<String, String> getTestMessage() {
        // 4. Retorna um Mapa, que o Spring automaticamente converte para JSON
        return Map.of("message", "Olá do Statgen-Java via IDE!");
    }
}
