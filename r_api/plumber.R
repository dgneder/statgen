# statgen/r_api/plumber.R

library(plumber)

# Carrega todas as nossas funções de lógica do arquivo de serviço
source("logic/randomization_service.R")


#* @apiTitle Statgen R API
#* @apiDescription Microsserviço para análises estatísticas.

# --- Endpoint DIC ---
#* Sorteia um Delineamento Inteiramente Casualizado (DIC)
#* @post /randomize/dic
function(req, res) { # Removemos os parâmetros da assinatura
  # Lemos o corpo da requisição JSON
  params <- req$body
  # Chamamos a função de serviço com os valores de dentro do JSON
  layout <- generate_dic_layout(params$genotypes, params$repetitions)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}


# --- Endpoint DBC ---
#* Sorteia um Delineamento em Blocos Casualizados (DBC)
#* @post /randomize/dbc
function(req, res) { # Removemos os parâmetros da assinatura
  params <- req$body
  layout <- generate_dbc_layout(params$genotypes, params$repetitions)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}


# --- Endpoint Quadrado Latino ---
#* Sorteia um Delineamento em Quadrado Latino
#* @post /randomize/latinsquare
function(req, res) { # Removemos os parâmetros da assinatura
  params <- req$body
  layout <- generate_latinsquare_layout(params$treatments)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}

# --- Endpoint Látice Simples ---
#* Sorteia um Delineamento em Látice Simples
#* @post /randomize/simple-lattice
function(req, res) { # Removemos os parâmetros da assinatura
  params <- req$body
  layout <- generate_simple_lattice_layout(params$treatments)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}

# --- Endpoint Látice Simples Duplicado ---
#* Sorteia um Delineamento em Látice Simples Duplicado (4 reps)
#* @param treatments:int O número de tratamentos (deve ser um quadrado perfeito)
#* @post /randomize/doubled-lattice
function(req, res) {
  # Lógica correta restaurada:
  params <- req$body
  layout <- generate_doubled_lattice_layout(params$treatments)
  
  # Verifica se a função de lógica retornou um erro e ajusta o status HTTP
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  
  # Retorna o resultado (seja o data.frame do layout ou a lista de erro)
  return(layout)
}

# --- Endpoint Látice-Alfa ---
#* Sorteia um Delineamento Látice-Alfa
#* @param treatments:int O número de tratamentos
#* @param k:int O tamanho do bloco
#* @param r:int O número de replicações
#* @post /randomize/alpha-lattice
function(req, res) {
  params <- req$body
  layout <- generate_alpha_lattice_layout(params$treatments, params$k, params$r)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}

# --- Endpoint DIC Fatorial (AxB) ---
#* Sorteia um DIC Fatorial AxB
#* @param levels_a:int O número de níveis do Fator A
#* @param levels_b:int O número de níveis do Fator B
#* @param r:int O número de repetições
#* @post /randomize/factorial-crd
function(req, res) {
  params <- req$body
  layout <- generate_factorial_crd_layout(params$levels_a, params$levels_b, params$r)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}

# --- Endpoint Blocos Aumentados ---
#* Sorteia um Delineamento em Blocos Aumentados
#* @param new_treatments:int O número de novos tratamentos
#* @param check_treatments:int O número de testemunhas
#* @param blocks:int O número de blocos
#* @post /randomize/augmented-block
function(req, res) {
  params <- req$body
  layout <- generate_augmented_design_layout(params$new_treatments, params$check_treatments, params$blocks)
  
  if ("error" %in% names(layout)) {
    res$status <- 400
  }
  return(layout)
}
