from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
from .services import randomization
from rest_framework import generics
from rest_framework import permissions
from .models import Experiment
from .serializers import ExperimentSerializer, UserSerializer
from django.contrib.auth.models import User
import math 

# Em vez de uma função simples, agora usamos uma classe que herda de APIView.
# Isso nos dá muito mais poder e flexibilidade.
from rest_framework import generics, permissions # Adicione permissions

class TestEndpoint(APIView):
    """
    Um endpoint de teste para verificar a comunicação, agora usando o poder do DRF.
    """
    def get(self, request, *args, **kwargs):
        """
        Este método lida especificamente com requisições GET.
        """
        data = {
            "message": "Olá do DRF! A API está mais poderosa agora!",
            "author": "Diogo Neder (via Django REST Framework)"
        }
        # Usamos o objeto Response do DRF. Ele lida com a conversão para JSON
        # automaticamente e adiciona cabeçalhos adequados.
        return Response(data, status=status.HTTP_200_OK)

class ExperimentListCreateView(generics.ListCreateAPIView):
    serializer_class = ExperimentSerializer
    # Adicione esta linha para garantir que apenas usuários autenticados possam acessar
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todos os experimentos
        para o usuário autenticado atualmente.
        """
        user = self.request.user
        return Experiment.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Liga o usuário logado ao novo experimento criado.
        """
        serializer.save(owner=self.request.user)

class ExperimentDetailView(generics.RetrieveAPIView):
    serializer_class = ExperimentSerializer
    permission_classes = [permissions.IsAuthenticated] # Proteja esta view também

    def get_queryset(self):
        """
        Garante que um usuário só possa ver detalhes de seus próprios experimentos.
        """
        user = self.request.user
        return Experiment.objects.filter(owner=user)

class UserRegistrationView(generics.CreateAPIView):
    """
    View para registrar novos usuários. Acessível por qualquer um.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Sobrescrevemos a permissão padrão para permitir que qualquer um se registre
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    """
    View para retornar os dados do usuário logado.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retorna o objeto do usuário associado à requisição atual
        return self.request.user

class DICRandomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            num_genotypes = int(request.data.get("genotypes"))
            num_repetitions = int(request.data.get("repetitions"))

            if not (0 < num_genotypes <= 1000 and 0 < num_repetitions <= 100):
                raise ValueError("Valores fora dos limites permitidos (Tratamentos: 1-1000, Repetições/Blocos: 1-100).")
            
            # Se a validação passou, chama o serviço
            layout = randomization.generate_dic_layout(num_genotypes, num_repetitions)
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'genotypes' e 'repetitions' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


            
            # A view agora DELEGA a lógica complexa!
            layout = randomization.generate_dic_layout(num_genotypes, num_repetitions)
            return Response(layout, status=status.HTTP_200_OK)

class DBCRandomizationView(APIView):
    """
    Realiza o sorteio de um Delineamento em Blocos Casualizados (DBC).
    Recebe via POST:
    {
        "genotypes": (int) número de tratamentos/genótipos,
        "repetitions": (int) número de blocos/repetições
    }
    Devolve o plano do experimento em JSON.
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            num_genotypes = int(request.data.get("genotypes"))
            num_repetitions = int(request.data.get("repetitions")) # Aqui, repetições = blocos

            # --- VALIDAÇÃO COMPLETA APLICADA ---
            if not (0 < num_genotypes <= 1000 and 0 < num_repetitions <= 100):
                raise ValueError("Valores fora dos limites permitidos (Tratamentos: 1-1000, Blocos: 1-100).")
            
            # Se a validação passou, chama o serviço que contata a API R
            layout = randomization.generate_dbc_layout(num_genotypes, num_repetitions)
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Captura o ValueError e usa sua mensagem específica no retorno da API
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Captura outros erros, como chaves faltando no JSON ou tipos inadequados
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'genotypes' e 'repetitions' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Retorna um erro se não conseguir conectar à API R
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 2. A Lógica do Sorteio para DBC
        # Cria a lista base de tratamentos
        treatments = [f'T{i+1}' for i in range(num_genotypes)]
        
        final_layout = []
        plot_counter = 1
        
        # O laço principal: iteramos sobre cada bloco
        for block_num in range(1, num_repetitions + 1):
            # Para cada bloco, criamos uma cópia fresca da lista de tratamentos
            block_treatments = treatments.copy()
            
            # Embaralhamos os tratamentos APENAS DENTRO deste bloco
            np.random.shuffle(block_treatments)
            
            # Adicionamos os tratamentos embaralhados do bloco ao layout final
            for treatment_code in block_treatments:
                final_layout.append({
                    "plot": plot_counter,
                    "block": block_num,
                    "treatment": treatment_code
                })
                plot_counter += 1

        return Response(final_layout, status=status.HTTP_200_OK)

# statgen/backend/core/views.py

# ... (importações e classes existentes) ...
import string # Usaremos para gerar tratamentos A, B, C...

class LatinSquareRandomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            n = int(request.data.get("treatments"))

            # --- VALIDAÇÃO ATUALIZADA PARA O NOVO LIMITE ---
            if not (1 < n <= 200):
                raise ValueError("O número de tratamentos para o Quadrado Latino deve estar entre 2 e 200.")
            
            # Se a validação passou, chama o serviço
            layout = randomization.generate_latinsquare_layout(n)
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Retorna a mensagem de erro específica do ValueError
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Retorna uma mensagem para dados ausentes/malformados
            return Response(
                {"error": "Dado ausente ou em formato incorreto. Forneça 'treatments' como um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Retorna um erro se não conseguir conectar à API R
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SimpleLatticeRandomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            treatments = int(request.data.get("treatments"))
            
            # --- VALIDAÇÃO COMPLETA APLICADA ---
            # Verifica se é um quadrado perfeito
            k = math.isqrt(treatments) # isqrt é eficiente para raízes quadradas inteiras
            if k * k != treatments:
                raise ValueError("O número de tratamentos para o Látice deve ser um quadrado perfeito (ex: 9, 16, 25...).")

            # Verifica os limites
            if not (3 < treatments <= 1000):
                raise ValueError("O número de tratamentos para o Látice Simples deve estar entre 4 e 1000.")

            # Se a validação passou, chama o serviço
            layout = randomization.generate_simple_lattice_layout(treatments)
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response(
                {"error": "Dado ausente ou em formato incorreto. Forneça 'treatments' como um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DoubledLatticeRandomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            treatments = int(request.data.get("treatments"))
            # A validação (quadrado perfeito, limites) será feita na view do Látice Simples.
            # Aqui podemos ter uma validação mais simples ou confiar na do R.
            # Por consistência, vamos adicionar a validação aqui também.
            k = math.isqrt(treatments)
            if k * k != treatments:
                raise ValueError("O número de tratamentos para o Látice deve ser um quadrado perfeito (ex: 9, 16, 25...).")
            if not (3 < treatments <= 1000): # Usando o mesmo limite
                raise ValueError("O número de tratamentos para o Látice Duplicado deve estar entre 4 e 1000.")

            layout = randomization.generate_doubled_lattice_layout(treatments)
            return Response(layout, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response(
                {"error": "Dado ausente ou em formato incorreto. Forneça 'treatments' como um número inteiro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AlphaLatticeRandomizationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            treatments = int(request.data.get("treatments"))
            k = int(request.data.get("k"))
            r = int(request.data.get("r"))

            # Validações podem ser adicionadas aqui também, se desejado

            layout = randomization.generate_alpha_lattice_layout(treatments, k, r)
            return Response(layout, status=status.HTTP_200_OK)
        except (TypeError, ValueError, KeyError):
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'treatments', 'k', e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FactorialCRDView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            r = int(request.data.get("r"))
            
            # Validação simples no backend
            if not (levels_a > 0 and levels_b > 0 and r > 0):
                raise ValueError("Níveis dos fatores e repetições devem ser maiores que zero.")

            layout = randomization.generate_factorial_crd_layout(levels_a, levels_b, r)
            return Response(layout, status=status.HTTP_200_OK)
        except (TypeError, ValueError, KeyError):
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'treatments', 'k', e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class FactorialAxBCView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            levels_c = int(request.data.get("levels_c"))
            r = int(request.data.get("r"))

            layout = randomization.generate_factorial_axbxc_layout(levels_a, levels_b, levels_c, r)
            return Response(layout, status=status.HTTP_200_OK)
        except (TypeError, ValueError, KeyError):
            return Response({"error": "Dados inválidos ou ausentes."}, status=status.HTTP_400_BAD_REQUEST)
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class FactorialRCBDView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            r = int(request.data.get("r"))

            # Validação dos limites que definimos
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < r <= limit):
                raise ValueError(f"Níveis dos fatores e repetições devem estar entre 1 e {limit}.")

            # Se a validação passou, chama o serviço que contata a API Java
            layout = randomization.generate_factorial_rcbd_layout(levels_a, levels_b, r)
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Retorna a mensagem de erro específica do ValueError (da nossa validação)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Retorna uma mensagem para dados ausentes/malformados
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b' e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Retorna um erro se não conseguir conectar à API Java
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class FactorialAxBCRCBDView(APIView):
    """
    View para o Delineamento Fatorial AxBxC em Blocos Casualizados.
    Recebe os níveis dos fatores A, B, C e o número de repetições (blocos).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # 1. Pega e converte os parâmetros da requisição
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            levels_c = int(request.data.get("levels_c"))
            r = int(request.data.get("r"))

            # 2. Valida os limites para proteger o sistema
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < levels_c <= limit and 0 < r <= limit):
                raise ValueError(f"Níveis dos fatores e repetições devem estar entre 1 e {limit}.")

            # 3. Chama o serviço que fará a requisição para a API Java
            layout = randomization.generate_factorial_axbxc_rcbd_layout(levels_a, levels_b, levels_c, r)
            
            # 4. Retorna a resposta de sucesso com o layout
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Captura erros de validação
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Captura erros de dados ausentes ou malformados
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b', 'levels_c' e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Captura erros de comunicação com a API Java
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SplitPlotRCBDView(APIView):
    """
    View para o Delineamento em Parcelas Subdivididas em Blocos Casualizados.
    Recebe os níveis do Fator A (parcela), Fator B (subparcela) e o número de blocos (r).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # 1. Pega e converte os parâmetros da requisição
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            r = int(request.data.get("r"))

            # 2. Valida os limites que definimos
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < r <= limit):
                raise ValueError(f"Níveis dos fatores e blocos devem estar entre 1 e {limit}.")

            # 3. Chama o serviço que fará a requisição para a API Java
            layout = randomization.generate_split_plot_rcbd_layout(levels_a, levels_b, r)
            
            # 4. Retorna a resposta de sucesso com o layout
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Captura erros de validação (ex: fora do limite)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Captura erros de dados ausentes ou com formato errado no JSON
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b' e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Captura erros de comunicação com a API Java
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SplitSplitPlotRCBDView(APIView):
    """
    View para o Delineamento em Parcelas Sub-subdivididas em Blocos Casualizados.
    Recebe os níveis dos fatores A, B, C e o número de blocos (r).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # 1. Pega e converte os parâmetros da requisição do frontend.
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            levels_c = int(request.data.get("levels_c"))
            r = int(request.data.get("r"))

            # 2. Valida os limites para proteger o sistema.
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < levels_c <= limit and 0 < r <= limit):
                raise ValueError(f"Os níveis dos fatores e o número de blocos devem estar entre 1 e {limit}.")

            # 3. Chama o serviço Python, que por sua vez chama a API Java.
            layout = randomization.generate_split_split_plot_rcbd_layout(levels_a, levels_b, levels_c, r)
            
            # 4. Retorna a resposta de sucesso com o layout do sorteio.
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Captura erros de validação (ex: fora do limite).
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Captura erros de dados ausentes ou com formato errado no JSON.
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b', 'levels_c' e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Captura erros de comunicação com a API Java.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SplitPlotCRDView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            r = int(request.data.get("r"))
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < r <= limit):
                raise ValueError(f"Os níveis dos fatores e as repetições devem estar entre 1 e {limit}.")
            layout = randomization.generate_split_plot_crd_layout(levels_a, levels_b, r)
            return Response(layout, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response({"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b' e 'r' como números."}, status=status.HTTP_400_BAD_REQUEST)
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SplitSplitPlotCRDView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            levels_a = int(request.data.get("levels_a"))
            levels_b = int(request.data.get("levels_b"))
            levels_c = int(request.data.get("levels_c"))
            r = int(request.data.get("r"))
            limit = 100
            if not (0 < levels_a <= limit and 0 < levels_b <= limit and 0 < levels_c <= limit and 0 < r <= limit):
                raise ValueError(f"Os níveis dos fatores e as repetições devem estar entre 1 e {limit}.")
            layout = randomization.generate_split_split_plot_crd_layout(levels_a, levels_b, levels_c, r)
            return Response(layout, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'levels_a', 'levels_b', 'levels_c' e 'r' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AugmentedBlockJavaView(APIView):
    """
    View para o Delineamento em Blocos Aumentados, utilizando o microsserviço em Java.
    Recebe o número de novos tratamentos, testemunhas e o número de blocos.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # 1. Pega e converte os parâmetros da requisição.
            new_treatments = int(request.data.get("new_treatments"))
            check_treatments = int(request.data.get("check_treatments"))
            blocks = int(request.data.get("blocks"))

            # 2. Valida os limites que definimos.
            if not (0 < new_treatments <= 1000 and 0 < check_treatments <= 1000 and 0 < blocks <= 100):
                raise ValueError("Valores fora dos limites permitidos (Tratamentos/Testemunhas: 1-1000, Blocos: 1-100).")

            # --- CORREÇÃO APLICADA AQUI ---
            # 3. Chama a função de serviço correta, que aponta para a API Java.
            layout = randomization.generate_augmented_block_layout_java(new_treatments, check_treatments, blocks)
            
            # 4. Retorna a resposta de sucesso com o layout do sorteio.
            return Response(layout, status=status.HTTP_200_OK)

        except ValueError as e:
            # Captura erros de validação.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, KeyError):
            # Captura erros de dados ausentes ou com formato errado no JSON.
            return Response(
                {"error": "Dados ausentes ou em formato incorreto. Forneça 'new_treatments', 'check_treatments' e 'blocks' como números."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ConnectionError as e:
            # Captura erros de comunicação com a API Java.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
