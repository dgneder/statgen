# statgen/r_api/logic/randomization_service.R

# Carrega quaisquer bibliotecas que a lógica precise
# (Neste caso, nenhuma externa, mas é uma boa prática)

# Nossa primeira função de serviço pura
generate_dic_layout <- function(genotypes, repetitions) {
  
  # A validação dos parâmetros fica melhor aqui, junto com a lógica.
  if (is.na(genotypes) || is.na(repetitions) || genotypes <= 0 || repetitions <= 0) {
    # Em caso de erro, retornamos uma lista com um elemento de erro.
    return(list(error="Parâmetros 'genotypes' e 'repetitions' devem ser números inteiros positivos."))
  }
  
  treatments <- paste0("T", 1:genotypes)
  full_layout_vector <- rep(treatments, times = repetitions)
  shuffled_layout <- sample(full_layout_vector)
  
  plot_data <- data.frame(treatment = shuffled_layout)
  plot_data$plot <- 1:nrow(plot_data)
  
  repetition_counter <- ave(1:nrow(plot_data), plot_data$treatment, FUN = seq_along)
  plot_data$repetition <- repetition_counter
  
  result <- plot_data[, c("plot", "treatment", "repetition")]
  
  return(result)
}

generate_dbc_layout <- function(genotypes, repetitions) {
  
  # Validação dos parâmetros
  if (is.na(genotypes) || is.na(repetitions) || genotypes <= 0 || repetitions <= 0) {
    return(list(error="Parâmetros 'genotypes' e 'repetitions' (blocos) devem ser números inteiros positivos."))
  }
  
  # Lógica do sorteio para DBC
  base_treatments <- paste0("T", 1:genotypes)
  final_layout_vector <- c() # c() cria um vetor vazio
  
  # Loop para cada bloco (repetição)
  for (block_num in 1:repetitions) {
    # Embaralha os tratamentos para este bloco específico
    shuffled_block <- sample(base_treatments)
    # Adiciona o bloco embaralhado ao nosso layout final
    final_layout_vector <- c(final_layout_vector, shuffled_block)
  }
  
  # Monta o data.frame final
  result <- data.frame(
    plot = 1:length(final_layout_vector),
    # A função rep() é perfeita para criar a coluna de blocos
    block = rep(1:repetitions, each = genotypes),
    treatment = final_layout_vector
  )
  
  return(result)
}

generate_latinsquare_layout <- function(treatments_n) {
  
  n <- as.numeric(treatments_n)
  
  # Validação
  if (is.na(n) || n <= 1 || n > 26) {
    return(list(error="O número de tratamentos (n) deve ser um inteiro entre 2 e 26."))
  }
  
  # Lógica do sorteio para Quadrado Latino
  # Usaremos as letras maiúsculas como nomes de tratamentos (padrão em QL)
  treatments <- LETTERS[1:n]
  
  # 1. Cria um quadrado latino padrão
  square <- matrix(nrow = n, ncol = n)
  for (i in 1:n) {
    # Preenche cada linha com um deslocamento cíclico dos tratamentos
    square[i, ] <- c(treatments[i:n], if (i > 1) treatments[1:(i-1)] else NULL)
  }
  
  # 2. Randomiza o quadrado
  # Embaralha as linhas
  square <- square[sample(1:n), ]
  # Embaralha as colunas
  square <- square[, sample(1:n)]
  
  # 3. Formata o resultado em um data.frame limpo
  # expand.grid cria todas as combinações de linha e coluna
  result <- expand.grid(row = 1:n, column = 1:n)
  # Adiciona os tratamentos do nosso quadrado embaralhado
  result$treatment <- as.vector(square)
  
  return(result)
}

generate_simple_lattice_layout <- function(treatments_t) {
  
  t <- as.numeric(treatments_t)
  k <- sqrt(t)
  
  if (is.na(t) || k %% 1 != 0 || t <= 3 || t > 1000) {
    return(list(error="Número de tratamentos inválido. Deve ser um quadrado perfeito entre 4 e 1000."))
  }
  
  treatments_vector <- 1:t
  shuffled_labels <- sample(treatments_vector)
  square <- matrix(shuffled_labels, nrow = k, byrow = TRUE)
  
  # Usando apply para uma abordagem mais limpa e idiomática em R
  # apply(matriz, 1, funcao) aplica a função a cada linha
  # apply(matriz, 2, funcao) aplica a função a cada coluna
  rep_x_blocks <- apply(square, 1, sample)
  rep_y_blocks <- apply(square, 2, sample)
  
  # A ordem dos blocos também é randomizada
  rep_x_blocks <- rep_x_blocks[, sample(1:k)]
  rep_y_blocks <- rep_y_blocks[, sample(1:k)]

  rep_x_df <- data.frame(
    replication = "X",
    block = rep(1:k, each = k),
    treatment = paste0("T", as.vector(rep_x_blocks))
  )
  
  rep_y_df <- data.frame(
    replication = "Y",
    block = rep((k + 1):(2 * k), each = k),
    treatment = paste0("T", as.vector(rep_y_blocks))
  )
  
  final_layout <- rbind(rep_x_df, rep_y_df)
  final_layout$plot <- 1:nrow(final_layout)
  
  return(final_layout[, c("plot", "replication", "block", "treatment")])
}


# Versão CORRIGIDA do Látice Duplicado
generate_doubled_lattice_layout <- function(treatments_t) {
  
  t <- as.numeric(treatments_t)
  k <- sqrt(t)
  
  # --- 1. Validação ---
  if (is.na(t) || k %% 1 != 0 || t <= 3 || t > 1000) {
    return(list(error="Número de tratamentos inválido. Deve ser um quadrado perfeito entre 4 e 1000."))
  }
  
  # --- 2. Primeira Randomização (Para Reps X1 e Y1) ---
  
  treatments_vector <- 1:t
  shuffled_labels_1 <- sample(treatments_vector)
  square_1 <- matrix(shuffled_labels_1, nrow = k, byrow = TRUE)
  
  # Blocos X1
  rep_x1_blocks_matrix <- apply(square_1, 1, sample)
  rep_x1_blocks_matrix <- rep_x1_blocks_matrix[, sample(1:k)]
  
  # Blocos Y1
  rep_y1_blocks_matrix <- apply(square_1, 2, sample)
  rep_y1_blocks_matrix <- rep_y1_blocks_matrix[, sample(1:k)]
  
  # --- 3. Segunda Randomização (Para Reps X2 e Y2) ---
  
  shuffled_labels_2 <- sample(treatments_vector)
  square_2 <- matrix(shuffled_labels_2, nrow = k, byrow = TRUE)
  
  # Blocos X2
  rep_x2_blocks_matrix <- apply(square_2, 1, sample)
  rep_x2_blocks_matrix <- rep_x2_blocks_matrix[, sample(1:k)]
  
  # Blocos Y2
  rep_y2_blocks_matrix <- apply(square_2, 2, sample)
  rep_y2_blocks_matrix <- rep_y2_blocks_matrix[, sample(1:k)]
  
  # --- 4. Montagem dos Data Frames ---
  
  rep_x1_df <- data.frame(
    replication = "X1",
    block = rep(1:k, each = k),
    treatment = paste0("T", as.vector(rep_x1_blocks_matrix))
  )
  
  rep_y1_df <- data.frame(
    replication = "Y1",
    block = rep((k + 1):(2 * k), each = k),
    treatment = paste0("T", as.vector(rep_y1_blocks_matrix))
  )
  
  rep_x2_df <- data.frame(
    replication = "X2",
    block = rep((2*k + 1):(3 * k), each = k),
    treatment = paste0("T", as.vector(rep_x2_blocks_matrix))
  )
  
  rep_y2_df <- data.frame(
    replication = "Y2",
    block = rep((3*k + 1):(4 * k), each = k),
    treatment = paste0("T", as.vector(rep_y2_blocks_matrix))
  )
  
  # --- 5. União e Finalização ---
  
  final_layout <- rbind(rep_x1_df, rep_y1_df, rep_x2_df, rep_y2_df)
  final_layout$plot <- 1:nrow(final_layout)
  
  return(final_layout[, c("plot", "replication", "block", "treatment")])
}

generate_alpha_lattice_layout <- function(t, k, r) {

  # Carrega a biblioteca dentro da função
  library(agricolae)

  # Converte parâmetros para numérico
  t <- as.numeric(t)
  k <- as.numeric(k)
  r <- as.numeric(r)

  # Validação dos parâmetros
  if (is.na(t) || is.na(k) || is.na(r) || t <= 0 || k <= 0 || r <= 0) {
    return(list(error="Tratamentos, tamanho do bloco e repetições devem ser números positivos."))
  }
  if (t %% k != 0) {
    return(list(error="O número de tratamentos deve ser um múltiplo do tamanho do bloco."))
  }
  if (t > 1000) {
    return(list(error="O número de tratamentos não pode exceder 1000."))
  }

  # Cria os nomes dos tratamentos
  treatments_vector <- paste0("T", 1:t)

  # A MÁGICA: Usa a função design.alpha() do pacote agricolae
  # Usamos um tryCatch para capturar qualquer erro estatístico da função
  tryCatch({
    design <- design.alpha(treatments_vector, k = k, r = r, seed = round(runif(1, min=0, max=10000)))

    # Extrai o plano do experimento (o "book")
    layout <- design$book

    # Renomeia as colunas para o nosso padrão
    names(layout) <- c("plot", "replication", "block", "treatment")

    # Converte a coluna de replicação para caractere para consistência (ex: "1" -> "R1")
    layout$replication <- paste0("R", layout$replication)

    return(layout)

  }, error = function(e) {
    # Se a função design.alpha falhar, retorna uma mensagem de erro clara
    return(list(error = paste("Erro na geração do Látice-Alfa:", e$message)))
  })
}

generate_factorial_crd_layout <- function(levels_a, levels_b, r) {
  
  # Converte parâmetros para numérico
  a <- as.numeric(levels_a)
  b <- as.numeric(levels_b)
  reps <- as.numeric(r)
  
  # Validação
  if (is.na(a) || is.na(b) || is.na(reps) || a <= 0 || b <= 0 || reps <= 0) {
    return(list(error="Níveis dos fatores e repetições devem ser números inteiros positivos."))
  }
  if ((a * b) > 1000) { # Limite total de tratamentos
      return(list(error="O número total de tratamentos (A x B) não pode exceder 1000."))
  }
  
  # 1. Gera os nomes dos níveis para cada fator
  factor_a_labels <- paste0("A", 1:a)
  factor_b_labels <- paste0("B", 1:b)
  
  # 2. A MÁGICA: expand.grid cria um data.frame com todas as combinações
  all_combinations <- expand.grid(factor_a = factor_a_labels, factor_b = factor_b_labels)
  
  # 3. Replica o conjunto completo de tratamentos
  full_layout_df <- do.call("rbind", replicate(reps, all_combinations, simplify = FALSE))
  
  # 4. Randomiza a ordem das linhas (casualização completa)
  randomized_layout <- full_layout_df[sample(nrow(full_layout_df)), ]
  
  # 5. Adiciona colunas de parcela e repetição
  randomized_layout$plot <- 1:nrow(randomized_layout)
  
  # A lógica para calcular a repetição de cada combinação
  randomized_layout$treatment_combination <- paste(randomized_layout$factor_a, randomized_layout$factor_b, sep="-")
  randomized_layout$repetition <- ave(1:nrow(randomized_layout), randomized_layout$treatment_combination, FUN = seq_along)
  
  # Remove a coluna auxiliar e retorna o resultado ordenado
  return(randomized_layout[, c("plot", "repetition", "factor_a", "factor_b")])
}

# --- BLOCOS AUMENTADOS (VERSÃO REVISADA E CORRIGIDA) ---
generate_augmented_design_layout <- function(new_treatments, check_treatments, blocks) {
  # Carrega a biblioteca necessária
  # Envolver em suppressPackageStartupMessages para um log mais limpo
  suppressPackageStartupMessages(library(agricolae))
  
  t <- as.numeric(new_treatments)
  c <- as.numeric(check_treatments)
  b <- as.numeric(blocks)
  
  # Validação robusta
  if (is.na(t) || is.na(c) || is.na(b) || t <= 0 || c <= 0 || b <= 0) {
    return(list(error="Tratamentos, testemunhas e blocos devem ser números inteiros positivos."))
  }
  if (t > 1000 || c > 1000 || b > 100) {
    return(list(error="Valores excedem os limites (Tratamentos/Testemunhas: 1000, Blocos: 100)."))
  }
  if (t %% b != 0) {
    return(list(error="O número de Novos Tratamentos deve ser um múltiplo do número de Blocos."))
  }
  
  # Cria os vetores de nomes
  new_trts_labels <- paste0("T", 1:t)
  check_trts_labels <- paste0("C", 1:c)
  
  # Bloco tryCatch para capturar erros da função do pacote
  layout_obj <- tryCatch({
    # Gera o design
    design <- design.dau(check_trts_labels, new_trts_labels, r = b, seed = round(runif(1, min=0, max=10000)))
    
    # Formata o resultado
    layout <- design$book
    layout$type <- ifelse(grepl("C", layout$trt), "Testemunha", "Tratamento")
    names(layout) <- c("plot", "block", "treatment", "type")
    
    # Retorna o data.frame formatado
    return(layout[, c("plot", "block", "treatment", "type")])
    
  }, error = function(e) {
    # Se a função design.dau() falhar, retorna uma lista de erro clara
    return(list(error = paste("Erro estatístico na geração do delineamento:", e$message)))
  })
  
  return(layout_obj)
}

}
