import pygame
import random
import os
import sys

# 🔧 CONFIGURAÇÃO PARA CODESPACES
try:
    # Tenta carregar sua imagem
    SUA_IMAGEM = "quebra-cabeça.jpg"
    
    # Se não encontrar, tenta caminhos alternativos
    if not os.path.exists(SUA_IMAGEM):
        caminhos_tentativos = [
            "imagens/sua_imagem.jpg",
            "/workspaces/seu-jogo/sua_imagem.jpg", 
            "/workspaces/seu-jogo/imagens/sua_imagem.jpg",
            "sua_imagem.jpg"
        ]
        
        for caminho in caminhos_tentativos:
            if os.path.exists(caminho):
                SUA_IMAGEM = caminho
                break
                
except Exception as e:
    print(f"⚠️  Aviso: {e}")
    SUA_IMAGEM = "sua_imagem.jpg"

# Inicializa o Pygame
pygame.init()

# Configurações do jogo
LARGURA_TELA, ALTURA_TELA = 1200, 800
TAMANHO_PECA = 130
LINHAS, COLUNAS = 3, 3
LARGURA_QUADRADO = TAMANHO_PECA * COLUNAS
ALTURA_QUADRADO = TAMANHO_PECA * LINHAS

# 🎨 PALETA DE CORES
BRANCO = (255, 255, 255)
PRETO = (50, 50, 50)
CINZA_CLARO = (240, 240, 240)
CINZA_MEDIO = (200, 200, 200)
VERDE_BONITO = (46, 204, 113)
AZUL_BONITO = (52, 152, 219)
LARANJA = (230, 126, 34)
CINZA_ESCURO = (100, 100, 100)

class QuebraCabecaOrganizado:
    def __init__(self):
        # 🔧 CONFIGURAÇÃO PARA CODESPACES
        try:
            self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        except pygame.error as e:
            print(f"❌ Erro ao criar janela: {e}")
            print("🔧 Tentando modo alternativo...")
            # Modo alternativo para servidores
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            pygame.display.init()
            self.tela = pygame.display.set_mode((1, 1))  # Janela mínima
            
        pygame.display.set_caption("🎮 Quebra-Cabeça - Codespaces")
        self.relogio = pygame.time.Clock()
        
        # Fontes
        self.fonte_titulo = pygame.font.Font(None, 36)
        self.fonte_normal = pygame.font.Font(None, 28)
        self.fonte_pequena = pygame.font.Font(None, 22)
        
        self.imagem_original = None
        self.pecas = []
        
        # Áreas do jogo
        self.area_montagem = pygame.Rect(80, 60, LARGURA_QUADRADO, ALTURA_QUADRADO)
        self.area_pecas = pygame.Rect(80, 480, 500, 250)
        self.area_instrucoes = pygame.Rect(650, 60, 450, 400)
        
        self.peca_arrastando = None
        self.offset_x = 0
        self.offset_y = 0
        self.movimentos = 0
        self.jogo_iniciado = False
        
        # Carrega a imagem
        self.carregar_imagem_automaticamente()
    
    def carregar_imagem_automaticamente(self):
        """Tenta carregar a imagem automaticamente"""
        print(f"🔍 Procurando imagem: {SUA_IMAGEM}")
        
        if os.path.exists(SUA_IMAGEM):
            if self.carregar_imagem(SUA_IMAGEM):
                print("✅ Imagem carregada com sucesso!")
                self.jogo_iniciado = True
                self.embaralhar_pecas()
            else:
                print("❌ Erro ao carregar, criando exemplo...")
                self.criar_imagem_exemplo()
        else:
            print("📸 Imagem não encontrada, criando exemplo...")
            # Lista arquivos disponíveis
            print("📁 Arquivos na pasta:")
            for arquivo in os.listdir('.'):
                if arquivo.lower().endswith(('.jpg', '.png', '.jpeg')):
                    print(f"   🖼️  {arquivo}")
            self.criar_imagem_exemplo()
    
    def carregar_imagem(self, caminho):
        """Carrega e prepara a imagem para o quebra-cabeça"""
        try:
            imagem = pygame.image.load(caminho)
            self.imagem_original = pygame.transform.scale(imagem, (LARGURA_QUADRADO, ALTURA_QUADRADO))
            self.criar_pecas()
            self.jogo_iniciado = True
            self.movimentos = 0
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar imagem: {e}")
            return False
    
    def criar_pecas(self):
        """Cria peças com visual moderno"""
        self.pecas = []
        
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca_surface = pygame.Surface((TAMANHO_PECA, TAMANHO_PECA), pygame.SRCALPHA)
                
                rect = pygame.Rect(coluna * TAMANHO_PECA, linha * TAMANHO_PECA, 
                                 TAMANHO_PECA, TAMANHO_PECA)
                peca_surface.blit(self.imagem_original, (0, 0), rect)
                
                # Borda arredondada
                pygame.draw.rect(peca_surface, BRANCO, (0, 0, TAMANHO_PECA, TAMANHO_PECA), 4, border_radius=8)
                pygame.draw.rect(peca_surface, PRETO, (0, 0, TAMANHO_PECA, TAMANHO_PECA), 2, border_radius=8)
                
                # Posição inicial
                x = self.area_pecas.x + 20 + random.randint(0, 350)
                y = self.area_pecas.y + 20 + random.randint(0, 180)
                
                self.pecas.append({
                    'surface': peca_surface,
                    'posicao_correta': (linha, coluna),
                    'rect': pygame.Rect(x, y, TAMANHO_PECA, TAMANHO_PECA),
                    'na_posicao_correta': False,
                    'travada': False,
                    'sombra_rect': pygame.Rect(x + 3, y + 3, TAMANHO_PECA, TAMANHO_PECA)
                })
    
    def embaralhar_pecas(self):
        """Embaralha as peças e destrava todas"""
        for peca in self.pecas:
            peca['rect'].x = self.area_pecas.x + 20 + random.randint(0, 350)
            peca['rect'].y = self.area_pecas.y + 20 + random.randint(0, 180)
            peca['sombra_rect'].x = peca['rect'].x + 3
            peca['sombra_rect'].y = peca['rect'].y + 3
            peca['na_posicao_correta'] = False
            peca['travada'] = False
        self.movimentos = 0
    
    def verificar_e_travar_peca(self, peca):
        """Verifica e trava a peça se estiver na posição correta"""
        if not peca['rect'].colliderect(self.area_montagem):
            return False
        
        # Calcula a posição na grade
        rel_x = peca['rect'].x - self.area_montagem.x
        rel_y = peca['rect'].y - self.area_montagem.y
        
        linha = rel_y // TAMANHO_PECA
        coluna = rel_x // TAMANHO_PECA
        
        if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
            esta_correta = (linha, coluna) == peca['posicao_correta']
            
            if esta_correta:
                peca['rect'].x = self.area_montagem.x + coluna * TAMANHO_PECA
                peca['rect'].y = self.area_montagem.y + linha * TAMANHO_PECA
                peca['sombra_rect'].x = peca['rect'].x + 3
                peca['sombra_rect'].y = peca['rect'].y + 3
                peca['travada'] = True
                peca['na_posicao_correta'] = True
                return True
        
        return False
    
    def criar_imagem_exemplo(self):
        """Cria uma imagem de exemplo bonita"""
        print("🎨 Criando imagem de exemplo...")
        self.imagem_original = pygame.Surface((LARGURA_QUADRADO, ALTURA_QUADRADO))
        
        # Gradiente de fundo
        for y in range(ALTURA_QUADRADO):
            for x in range(LARGURA_QUADRADO):
                r = int(100 + 155 * x / LARGURA_QUADRADO)
                g = int(100 + 155 * y / ALTURA_QUADRADO)
                b = 200
                self.imagem_original.set_at((x, y), (r, g, b))
        
        # Texto central
        fonte = pygame.font.Font(None, 48)
        texto = fonte.render("QUEBRA-CABEÇA", True, BRANCO)
        rect_texto = texto.get_rect(center=(LARGURA_QUADRADO//2, ALTURA_QUADRADO//2))
        
        # Sombra do texto
        texto_sombra = fonte.render("QUEBRA-CABEÇA", True, (30, 30, 30))
        self.imagem_original.blit(texto_sombra, (rect_texto.x + 3, rect_texto.y + 3))
        self.imagem_original.blit(texto, rect_texto)
        
        # Cria as peças
        self.criar_pecas()
        self.jogo_iniciado = True
        self.embaralhar_pecas()
    
    def todas_pecas_corretas(self):
        """Verifica se todas as peças estão na posição correta"""
        for peca in self.pecas:
            if not peca['na_posicao_correta']:
                return False
        return True
    
    def desenhar(self):
        """Desenha toda a interface do jogo"""
        # Fundo branco
        self.tela.fill(BRANCO)
        
        # 1. ÁREA DE MONTAGEM
        pygame.draw.rect(self.tela, BRANCO, self.area_montagem)
        pygame.draw.rect(self.tela, AZUL_BONITO, self.area_montagem, 4, border_radius=12)
        
        # Grade de referência
        for i in range(1, LINHAS):
            pygame.draw.line(self.tela, CINZA_CLARO, 
                           (self.area_montagem.x, self.area_montagem.y + i * TAMANHO_PECA),
                           (self.area_montagem.x + LARGURA_QUADRADO, self.area_montagem.y + i * TAMANHO_PECA), 2)
        
        for i in range(1, COLUNAS):
            pygame.draw.line(self.tela, CINZA_CLARO, 
                           (self.area_montagem.x + i * TAMANHO_PECA, self.area_montagem.y),
                           (self.area_montagem.x + i * TAMANHO_PECA, self.area_montagem.y + ALTURA_QUADRADO), 2)
        
        # Título da área de montagem
        texto_montagem = self.fonte_titulo.render("📍 MONTE AQUI", True, AZUL_BONITO)
        self.tela.blit(texto_montagem, (self.area_montagem.x, self.area_montagem.y - 40))
        
        # 2. ÁREA DE PEÇAS EMBARALHADAS
        pygame.draw.rect(self.tela, CINZA_CLARO, self.area_pecas, border_radius=12)
        pygame.draw.rect(self.tela, PRETO, self.area_pecas, 2, border_radius=12)
        
        texto_pecas = self.fonte_titulo.render("🧩 PEÇAS EMBARALHADAS", True, PRETO)
        self.tela.blit(texto_pecas, (self.area_pecas.x, self.area_pecas.y - 35))
        
        # 3. ÁREA DE INSTRUÇÕES
        pygame.draw.rect(self.tela, CINZA_CLARO, self.area_instrucoes, border_radius=12)
        pygame.draw.rect(self.tela, AZUL_BONITO, self.area_instrucoes, 3, border_radius=12)
        
        titulo = self.fonte_titulo.render("📋 COMO JOGAR", True, AZUL_BONITO)
        self.tela.blit(titulo, (self.area_instrucoes.x + 20, self.area_instrucoes.y + 20))
        
        instrucoes = [
            "1. Arraste as peças de baixo",
            "2. Solte no quadro branco",
            "3. Peça gruda quando estiver certa",
            "4. Complete para vencer!"
        ]
        
        for i, texto in enumerate(instrucoes):
            surf = self.fonte_normal.render(texto, True, PRETO)
            self.tela.blit(surf, (self.area_instrucoes.x + 30, self.area_instrucoes.y + 80 + i * 45))
        
        # Botão embaralhar
        botao_rect = pygame.Rect(self.area_instrucoes.x + 50, self.area_instrucoes.y + 280, 350, 60)
        pygame.draw.rect(self.tela, VERDE_BONITO, botao_rect, border_radius=15)
        pygame.draw.rect(self.tela, PRETO, botao_rect, 2, border_radius=15)
        
        texto_botao = self.fonte_normal.render("🔄 EMBARALHAR TUDO", True, BRANCO)
        texto_rect = texto_botao.get_rect(center=botao_rect.center)
        self.tela.blit(texto_botao, texto_rect)
        self.botao_embaralhar_rect = botao_rect
        
        # Informações do jogo
        texto_info = self.fonte_normal.render(f"✅ Peças corretas: {sum(1 for p in self.pecas if p['na_posicao_correta'])}/{len(self.pecas)}", True, VERDE_BONITO)
        self.tela.blit(texto_info, (self.area_instrucoes.x + 50, self.area_instrucoes.y + 360))
        
        # 4. DESENHA AS PEÇAS
        for peca in self.pecas:
            if not peca['travada']:
                pygame.draw.rect(self.tela, CINZA_ESCURO, peca['sombra_rect'], border_radius=8)
            
            self.tela.blit(peca['surface'], peca['rect'])
            
            if peca['travada']:
                pygame.draw.rect(self.tela, VERDE_BONITO, peca['rect'], 6, border_radius=8)
            else:
                pygame.draw.rect(self.tela, PRETO, peca['rect'], 2, border_radius=8)
        
        # 5. MENSAGEM DE VITÓRIA
        if self.todas_pecas_corretas():
            rect_vitoria = pygame.Rect(LARGURA_TELA//2 - 250, 300, 500, 120)
            pygame.draw.rect(self.tela, VERDE_BONITO, rect_vitoria, border_radius=20)
            pygame.draw.rect(self.tela, BRANCO, rect_vitoria, 4, border_radius=20)
            
            texto_vitoria = self.fonte_titulo.render("🎉 PARABÉNS! VOCÊ VENCEU! 🎉", True, BRANCO)
            rect_texto = texto_vitoria.get_rect(center=rect_vitoria.center)
            self.tela.blit(texto_vitoria, rect_texto)
        
        pygame.display.flip()
    
    def executar(self):
        """Loop principal do jogo"""
        print("🎮 Iniciando jogo no Codespaces...")
        print("💡 Dica: Use a aba 'Ports' para ver a visualização")
        
        executando = True
        
        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if hasattr(self, 'botao_embaralhar_rect') and self.botao_embaralhar_rect.collidepoint(pos):
                        self.embaralhar_pecas()
                    
                    for peca in reversed(self.pecas):
                        if peca['rect'].collidepoint(pos) and not peca['travada']:
                            self.peca_arrastando = peca
                            self.offset_x = peca['rect'].x - pos[0]
                            self.offset_y = peca['rect'].y - pos[1]
                            self.pecas.remove(peca)
                            self.pecas.append(peca)
                            break
                
                elif evento.type == pygame.MOUSEBUTTONUP:
                    if self.peca_arrastando:
                        self.movimentos += 1
                        self.verificar_e_travar_peca(self.peca_arrastando)
                        self.peca_arrastando = None
                
                elif evento.type == pygame.MOUSEMOTION:
                    if self.peca_arrastando and not self.peca_arrastando['travada']:
                        pos = pygame.mouse.get_pos()
                        self.peca_arrastando['rect'].x = pos[0] + self.offset_x
                        self.peca_arrastando['rect'].y = pos[1] + self.offset_y
                        self.peca_arrastando['sombra_rect'].x = self.peca_arrastando['rect'].x + 3
                        self.peca_arrastando['sombra_rect'].y = self.peca_arrastando['rect'].y + 3
            
            self.desenhar()
            self.relogio.tick(60)
        
        pygame.quit()
        sys.exit()

# 🚀 EXECUÇÃO NO CODESPACES
if __name__ == "__main__":
    print("=" * 50)
    print("🎮 QUEBRA-CABEÇA - CODESPACES")
    print("=" * 50)
    
    # Verifica se está no Codespaces
    if 'CODESPACES' in os.environ:
        print("🌐 Ambiente: GitHub Codespaces")
    else:
        print("💻 Ambiente: Local")
    
    print(f"📁 Diretório: {os.getcwd()}")
    print(f"🖼️  Imagem: {SUA_IMAGEM}")
    print("=" * 50)
    
    jogo = QuebraCabecaOrganizado()
    jogo.executar()