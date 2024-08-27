Aqui está um GitFlow básico que segue as características que você mencionou:

### Estrutura de Branches

- **`main`**: 
  - É a branch principal e sagrada. 
  - Nenhum código deve ser mergeado diretamente nesta branch até o final do projeto, quando todo o desenvolvimento estiver concluído e testado.
  
- **`develop`**: 
  - É a branch secundária onde o desenvolvimento contínuo ocorre.
  - Todas as novas funcionalidades devem ser mergeadas na `develop` através de Pull Requests (PR).

- **Branches de Funcionalidade**:
  - Cada integrante da equipe criará uma branch específica para a funcionalidade que está desenvolvendo.
  - As branches de funcionalidades seguem o padrão de nome `feature/nome-da-funcionalidade`.
  - Exemplos: `feature/autenticacao`, `feature/dashboard`, `feature/api-integracao`.

### Fluxo de Trabalho

1. **Criar Branch de Funcionalidade**:
   - Sempre crie uma nova branch a partir da `develop`.
   - Nomeie a branch seguindo o padrão `feature/nome-da-funcionalidade`.

2. **Desenvolvimento**:
   - Faça commits frequentes e pequenos na sua branch de funcionalidade.

3. **Commits**:
   - Use o padrão de commits com uma estrutura que descreva claramente a mudança:
     ```
     [Tipo]: Descrição da mudança
     ```
     - **Tipos comuns**:
       - `feat`: Adição de uma nova funcionalidade.
       - `fix`: Correção de bugs.
       - `refactor`: Refatoração de código.
       - `docs`: Mudanças na documentação.
       - `style`: Alterações de estilo (formatação, etc.).
       - `test`: Adicionando testes.
       - `chore`: Outras mudanças que não modificam o código ou os testes (ex.: mudanças na configuração do build).

     - **Exemplos**:
       - `feat: adiciona autenticação de usuário`
       - `fix: corrige bug na função de login`
       - `refactor: melhora lógica de validação de formulário`

4. **Pull Request (PR)**:
   - Após concluir o desenvolvimento de uma funcionalidade, abra um PR da sua branch para a `develop`.
   - Descreva claramente as mudanças realizadas no PR.
   - Pelo menos um outro membro da equipe deve revisar o PR antes de ele ser mergeado.

5. **Merge na Develop**:
   - Após a aprovação do PR, realize o merge na `develop`.
   - Se houver conflitos, resolva-os antes de fazer o merge.

6. **Finalização do Projeto**:
   - Quando todas as funcionalidades estiverem desenvolvidas, testadas e integradas na `develop`, o código final será mergeado na `main`.

### Resumo dos Padrões

- **Branches**:
  - `main`: Branch sagrada para versão final.
  - `develop`: Branch secundária para desenvolvimento contínuo.
  - `feature/nome-da-funcionalidade`: Branches para desenvolvimento de funcionalidades.

- **Commits**:
  - Padrão: `[Tipo]: Descrição da mudança`
  - Tipos: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`.

- **Pull Requests (PR)**:
  - Todos os PRs devem ser revisados antes do merge.
