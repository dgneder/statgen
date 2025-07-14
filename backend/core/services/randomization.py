# statgen/backend/core/services/randomization.py
import requests # Nossa nova importação!
# ... (outras importações e funções) ...

def generate_dic_layout(num_genotypes: int, num_repetitions: int) -> list:
    """
    Delega a geração do DIC para o microsserviço em R.
    """
    # Endereço da nossa API R
    r_api_url = "http://r_api:8001/randomize/dic" 
    params = {
        "genotypes": num_genotypes,
        "repetitions": num_repetitions
    }

    try:
        # Faz a chamada POST para o serviço R
        response = requests.post(r_api_url, json=params)

        # Lança um erro se a API R retornar um status de erro (4xx ou 5xx)
        response.raise_for_status()

        # Retorna o JSON que o R nos deu
        return response.json()

    except requests.exceptions.RequestException as e:
        # Tratamento de erro: O que acontece se o serviço R estiver offline?
        # Por enquanto, vamos lançar um erro informando a falha na conexão.
        print(f"ERRO DE CONEXÃO COM A API R: {e}")
        raise ConnectionError("Não foi possível conectar ao serviço de análise estatística R.")

def generate_dbc_layout(num_genotypes: int, num_repetitions: int) -> list:
    """Delega a geração do DBC para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/dbc" # Endpoint correto
    params = {"genotypes": num_genotypes, "repetitions": num_repetitions}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO COM A API R: {e}")
        raise ConnectionError("Não foi possível conectar ao serviço de análise estatística R.")

def generate_latinsquare_layout(n: int) -> list:
    """Delega a geração do Quadrado Latino para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/latinsquare"
    params = {"treatments": n}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXÃO COM A API R: {e}")
        raise ConnectionError("Não foi possível conectar ao serviço de análise estatística R.")

def generate_simple_lattice_layout(treatments: int) -> list:
    """Delega a geração do Látice Simples para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/simple-lattice"
    params = {"treatments": treatments}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status() # Lança um erro para status 4xx ou 5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        # Pega erros de conexão ou erros HTTP retornados pelo raise_for_status
        # Tenta extrair a mensagem de erro do R, se houver
        error_message = "Não foi possível conectar ao serviço de análise estatística R."
        try:
            error_details = e.response.json()
            # A API R retorna { "error": ["mensagem"] }
            if 'error' in error_details and error_details['error']:
                error_message = error_details['error'][0]
        except:
            pass # Mantém a mensagem de erro genérica se o JSON falhar
        raise ConnectionError(error_message)

def generate_doubled_lattice_layout(treatments: int) -> list:
    """Delega a geração do Látice Simples Duplicado para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/doubled-lattice"
    params = {"treatments": treatments}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise estatística R."
        try:
            error_details = e.response.json()
            if 'error' in error_details and error_details['error']:
                error_message = error_details['error'][0]
        except:
            pass
        raise ConnectionError(error_message)

def generate_alpha_lattice_layout(treatments: int, k: int, r: int) -> list:
    """Delega a geração do Látice-Alfa para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/alpha-lattice"
    params = {"treatments": treatments, "k": k, "r": r}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise estatística R."
        try:
            error_details = e.response.json()
            if 'error' in error_details and error_details['error']:
                error_message = error_details['error'][0]
        except:
            pass
        raise ConnectionError(error_message)

def generate_factorial_crd_layout(levels_a: int, levels_b: int, r: int) -> list:
    """Delega a geração do DIC Fatorial para o microsserviço em R."""
    r_api_url = "http://r_api:8001/randomize/factorial-crd"
    params = {"levels_a": levels_a, "levels_b": levels_b, "r": r}
    try:
        response = requests.post(r_api_url, json=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise estatística R."
        try:
            error_details = e.response.json()
            if 'error' in error_details and error_details['error']:
                error_message = error_details['error'][0]
        except:
            pass
        raise ConnectionError(error_message)
    
def generate_factorial_axbxc_layout(levels_a: int, levels_b: int, levels_c: int, r: int) -> list:
    """Delega a geração do DIC Fatorial AxBxC para o microsserviço em Java."""
    java_api_url = "http://java-api:8080/api/randomize/factorial-crd-axbxc"
    payload = {"levelsA": levels_a, "levelsB": levels_b, "levelsC": levels_c, "repetitions": r}
    try:
        response = requests.post(java_api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise Java."
        try:
            error_message = e.response.json().get('error', error_message)
        except:
            pass
        raise ConnectionError(error_message)

def generate_factorial_rcbd_layout(levels_a: int, levels_b: int, r: int) -> list:
    """
    Delega a geração do Fatorial em Blocos (AxB) para o microsserviço em Java.
    """
    # URL do nosso serviço Java, usando o nome definido no docker-compose.yml
    java_api_url = "http://java-api:8080/api/randomize/factorial-rcbd-axb"
    
    # Monta o payload. Note que as chaves (levelsA, etc.) devem ser exatamente
    # como definidas na nossa classe DTO FactorialAxBRequest.java
    payload = {
        "levelsA": levels_a,
        "levelsB": levels_b,
        "repetitions": r
    }
    
    try:
        response = requests.post(java_api_url, json=payload)
        # Lança uma exceção se a API Java retornar um erro (status 4xx ou 5xx)
        response.raise_for_status()
        # Se tudo deu certo, retorna o JSON da resposta
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Pega erros de conexão ou erros HTTP
        error_message = "Não foi possível conectar ao serviço de análise Java."
        # Tenta extrair a mensagem de erro específica vinda do Java, se houver
        try:
            error_details = e.response.json()
            if 'error' in error_details:
                error_message = error_details['error']
        except:
            # Mantém a mensagem de erro genérica se não conseguir ler o JSON do erro
            pass
        raise ConnectionError(error_message)

def generate_factorial_axbxc_rcbd_layout(levels_a: int, levels_b: int, levels_c: int, r: int) -> list:
    """
    Delega a geração do Fatorial AxBxC em Blocos para o microsserviço em Java.
    """
    # 1. URL do nosso serviço Java, usando o nome definido no docker-compose.yml
    java_api_url = "http://java-api:8080/api/randomize/factorial-rcbd-axbxc"
    
    # 2. Monta o payload JSON. As chaves devem ser EXATAMENTE como na classe DTO Java (camelCase).
    payload = {
        "levelsA": levels_a,
        "levelsB": levels_b,
        "levelsC": levels_c,
        "repetitions": r
    }
    
    try:
        # 3. Faz a chamada POST para o serviço Java
        response = requests.post(java_api_url, json=payload)
        
        # 4. Lança uma exceção se a API Java retornar um erro (status 4xx ou 5xx)
        response.raise_for_status()
        
        # 5. Se tudo deu certo, retorna o JSON da resposta (a lista de parcelas)
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # 6. Bloco para tratar erros de comunicação ou erros retornados pela API Java
        error_message = "Não foi possível conectar ao serviço de análise Java."
        
        # Tenta extrair a mensagem de erro específica vinda do Java, se houver
        if e.response is not None:
            try:
                error_details = e.response.json()
                if 'error' in error_details:
                    error_message = error_details['error']
            except ValueError: # Caso a resposta de erro não seja um JSON válido
                pass
                
        raise ConnectionError(error_message)

def generate_split_plot_rcbd_layout(levels_a: int, levels_b: int, r: int) -> list:
    """
    Delega a geração do Delineamento em Parcelas Subdivididas em DBC
    para o microsserviço em Java.
    """
    # 1. URL do nosso serviço Java, usando o nome definido no docker-compose.yml
    java_api_url = "http://java-api:8080/api/randomize/split-plot-rcbd"
    
    # 2. Monta o payload JSON com as chaves em camelCase, como o DTO Java espera
    payload = {
        "levelsA": levels_a,
        "levelsB": levels_b,
        "repetitions": r
    }
    
    try:
        # 3. Faz a chamada POST para o serviço Java
        response = requests.post(java_api_url, json=payload)
        
        # 4. Lança uma exceção se a API Java retornar um erro (status 4xx ou 5xx)
        response.raise_for_status()
        
        # 5. Se tudo deu certo, retorna o JSON da resposta
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # 6. Bloco para tratar erros de comunicação ou erros retornados pela API Java
        error_message = "Não foi possível conectar ao serviço de análise Java."
        
        # Tenta extrair a mensagem de erro específica vinda do Java, se houver
        if e.response is not None:
            try:
                error_details = e.response.json()
                if 'error' in error_details:
                    error_message = error_details['error']
            except ValueError:
                # Mantém a mensagem de erro genérica se não conseguir ler o JSON do erro
                pass
                
        raise ConnectionError(error_message)

def generate_split_plot_crd_layout(levels_a: int, levels_b: int, r: int) -> list:
    """Delega a geração da Parcela Subdividida em DIC para o microsserviço em Java."""
    java_api_url = "http://java-api:8080/api/randomize/split-plot-crd"
    payload = {"levelsA": levels_a, "levelsB": levels_b, "repetitions": r}
    try:
        response = requests.post(java_api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise Java."
        if e.response is not None:
            try:
                error_details = e.response.json()
                if 'error' in error_details: error_message = error_details['error']
            except ValueError: pass
        raise ConnectionError(error_message)


def generate_split_split_plot_crd_layout(levels_a: int, levels_b: int, levels_c: int, r: int) -> list:
    """Delega a geração da Parcela Sub-subdividida em DIC para o microsserviço em Java."""
    java_api_url = "http://java-api:8080/api/randomize/split-split-plot-crd"
    payload = {
        "levelsA": levels_a,
        "levelsB": levels_b,
        "levelsC": levels_c,
        "repetitions": r
    }
    try:
        response = requests.post(java_api_url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = "Não foi possível conectar ao serviço de análise Java."
        if e.response is not None:
            try:
                error_details = e.response.json()
                if 'error' in error_details:
                    error_message = error_details['error']
            except ValueError:
                pass
        raise ConnectionError(error_message)

def generate_augmented_block_layout_java(new_treatments: int, check_treatments: int, blocks: int) -> list:
    """
    Delega a geração do Delineamento em Blocos Aumentados para o microsserviço em Java.
    """
    # 1. URL do nosso serviço Java, usando o nome definido no docker-compose.yml
    java_api_url = "http://java-api:8080/api/randomize/augmented-block"
    
    # 2. Monta o payload JSON. As chaves (newTreatments, etc.) devem ser EXATAMENTE
    #    como definidas na nossa classe DTO AugmentedBlockRequest.java (camelCase).
    payload = {
        "newTreatments": new_treatments,
        "checkTreatments": check_treatments,
        "blocks": blocks
    }
    
    try:
        # 3. Faz a chamada POST, enviando o payload como JSON.
        response = requests.post(java_api_url, json=payload)
        
        # 4. Lança uma exceção se a API Java retornar um erro (status 4xx ou 5xx).
        response.raise_for_status()
        
        # 5. Se tudo deu certo, retorna o JSON da resposta.
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # 6. Bloco para tratar erros de comunicação ou erros retornados pela API Java.
        error_message = "Não foi possível conectar ao serviço de análise Java."
        
        # Tenta extrair a mensagem de erro específica vinda do Java, se houver.
        if e.response is not None:
            try:
                error_details = e.response.json()
                if 'error' in error_details:
                    error_message = error_details['error']
            except ValueError:
                # Mantém a mensagem de erro genérica se não conseguir ler o JSON do erro.
                pass
                
        raise ConnectionError(error_message)
