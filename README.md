# Classe ILovePdf

A classe `ILovePdf` foi criada para manipular arquivos PDF utilizando a API do serviço ILovePDF.

Para realizar manipulações em arquivos PDF, você precisa fornecer as chaves pública e secreta únicas obtidas ao se registrar para usar o serviço ILovePDF. O registro pode ser feito [aqui](https://developer.ilovepdf.com).

## Tarefa(s) Implementada(s)

- **comprimir**: Comprime um arquivo PDF.

## Uso

Aqui está um exemplo de como usar a classe `ILovePdf` para comprimir um arquivo PDF:

```python
# Instancia a classe ILovePdf com suas chaves pública e secreta
ilovepdf = ILovePdf(chave_publica, chave_secreta)

# Comprime o arquivo PDF
ilovepdf.comprimir(arquivo_input, arquivo_output)
```

## Construtor

### ILovePdf(chave_publica: str, chave_secreta: str)

Cria uma instância da classe `ILovePdf`.

#### Parâmetros

- `chave_publica` (str): Sua chave pública obtida no portal de desenvolvedores do ILovePDF.
- `chave_secreta` (str): Sua chave secreta obtida no portal de desenvolvedores do ILovePDF.

## Métodos

### comprimir(arquivo_input: str, arquivo_output: Optional[str] = None) -> None

Comprime o arquivo PDF especificado por `arquivo_input` e o salva como `arquivo_output`.

#### Parâmetros

- `arquivo_input` (str): O caminho para o arquivo de entrada a ser comprimido.

- `arquivo_output` (Optional[str], padrão=None): O caminho onde o arquivo comprimido será salvo. Se não for fornecido, o arquivo de saída terá o mesmo nome do arquivo `arquivo_input`, com "_compresso" adicionado como sufixo.

---

Por favor, observe que você precisa ter uma conta válida e obter as chaves pública e secreta necessárias no portal de desenvolvedores do ILovePDF para usar essa classe efetivamente.