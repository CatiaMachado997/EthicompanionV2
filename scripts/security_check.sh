#!/bin/bash
# 🔐 Security Check Script
# Verifica se há API keys expostas no código

echo "🔍 Verificando segurança do projeto..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar API keys expostas
check_exposed_keys() {
    echo -e "\n${YELLOW}🔍 Procurando por API keys expostas...${NC}"
    
    # Padrões de API keys conhecidos
    patterns=(
        "AIza[0-9A-Za-z_-]{35}"     # Google API Key
        "tvly-[a-zA-Z0-9]{32,}"     # Tavily API Key  
        "sk-[a-zA-Z0-9]{48,}"       # OpenAI API Key
        "gsk_[a-zA-Z0-9]{52,}"      # Google AI Studio
    )
    
    found_keys=false
    
    for pattern in "${patterns[@]}"; do
        results=$(grep -r -E "$pattern" . \
            --exclude-dir=node_modules \
            --exclude-dir=.git \
            --exclude-dir=__pycache__ \
            --exclude-dir=venv \
            --exclude-dir=.venv \
            --exclude="*.log" \
            --exclude=".env*" \
            --exclude="security_check.sh" \
            2>/dev/null)
        
        if [ ! -z "$results" ]; then
            echo -e "${RED}❌ ALERTA: Possível API key encontrada!${NC}"
            echo "$results"
            found_keys=true
        fi
    done
    
    if [ "$found_keys" = false ]; then
        echo -e "${GREEN}✅ Nenhuma API key exposta encontrada no código${NC}"
        return 0
    else
        return 1
    fi
}

# Função para verificar .env
check_env_file() {
    echo -e "\n${YELLOW}🔍 Verificando arquivo .env...${NC}"
    
    if [ -f ".env" ]; then
        echo -e "${GREEN}✅ Arquivo .env encontrado${NC}"
        
        # Verificar se .env está no .gitignore
        if grep -q "\.env" .gitignore 2>/dev/null; then
            echo -e "${GREEN}✅ .env está protegido no .gitignore${NC}"
        else
            echo -e "${RED}❌ CRÍTICO: .env NÃO está no .gitignore!${NC}"
            return 1
        fi
        
        # Verificar se tem as chaves necessárias
        if grep -q "GOOGLE_API_KEY" .env && grep -q "TAVILY_API_KEY" .env; then
            echo -e "${GREEN}✅ API keys estão configuradas no .env${NC}"
        else
            echo -e "${YELLOW}⚠️  Algumas API keys podem estar faltando no .env${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
        echo -e "${YELLOW}   Crie um .env com suas API keys${NC}"
    fi
}

# Função para verificar se .env está sendo commitado
check_git_status() {
    echo -e "\n${YELLOW}🔍 Verificando status do Git...${NC}"
    
    if git status --porcelain 2>/dev/null | grep -q "\.env"; then
        echo -e "${RED}❌ CRÍTICO: Arquivo .env está sendo commitado!${NC}"
        echo -e "${RED}   Execute: git reset HEAD .env${NC}"
        return 1
    else
        echo -e "${GREEN}✅ .env não está sendo commitado${NC}"
    fi
}

# Função principal
main() {
    echo "🛡️  Ethic Companion - Security Check"
    echo "=================================="
    
    check_exposed_keys
    keys_result=$?
    
    check_env_file
    env_result=$?
    
    check_git_status  
    git_result=$?
    
    echo -e "\n📊 Resumo da Verificação:"
    if [ $keys_result -eq 0 ] && [ $env_result -eq 0 ] && [ $git_result -eq 0 ]; then
        echo -e "${GREEN}✅ Projeto está seguro!${NC}"
        exit 0
    else
        echo -e "${RED}❌ Problemas de segurança encontrados!${NC}"
        echo -e "${YELLOW}   Corrija os problemas antes de fazer commit${NC}"
        exit 1
    fi
}

# Executar
main
