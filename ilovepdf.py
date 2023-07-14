import requests
from typing import Optional

class ILovePdf:
    """
    Classe ILovePdf para manipular arquivos PDF usando a API do serviço ILovePDF.

    Para realizar as manipulações com arquivos PDF, é necessário que sejam fornecidas
    as chaves pública e secreta únicas que são obtidas registrando-se para utilizar o
    serviço ILovePDF. O registro deve ser feito aqui: https://developer.ilovepdf.com

    Tarefa(s) implementada(s):
        - ILovePdf.comprimir:   Recebe um arquivo pdf e o comprime
    """

    def __init__(self, chave_publica: str, chave_secreta: str) -> None:
        """
        Inicializa instância de ILovePdf

        * Parâmetros

        chave_publica, chave_secreta:   str
            Podem ser obtidas em https://developer.ilovepdf.com/user/projects
        """

        self.base_url = "https://api.ilovepdf.com/v1"
        
        self.chave_publica = chave_publica
        self.chave_secreta = chave_secreta

        self.headers = dict()

        # Obtém token temporário para realizar as requests
        self._novo_token()

    def comprimir(self, arquivo_input: str, arquivo_output: Optional[str] = None) -> None:
        """
        Comprime o arquivo em `arquivo_input` e o salva em `arquivo_output`
 
        * Parâmetros

        arquivo_input:  str
            Caminho para o arquivo a ser compresso

        arquivo_output: str, opcional
            Caminho em que o arquivo compresso será salvo. Se não for fornecido
            na chamada da função, o nome do arquivo será o mesmo do `arquivo_input`
            adicionado de "_compresso".
        """
        if not arquivo_output:
            arquivo_output = arquivo_input[:-4] + "_compresso.pdf"

        self._nova_tarefa("compress")
        self._adicionar_arquivo(arquivo_input)
        self._processar()
        self._download(arquivo_output)

    def _nova_tarefa(self, tarefa: str) -> None:
        """
        Obtém o servidor e o ID da tarefa para realizar as requests

        * Parâmetros

        tarefa: str
            O nome da tarefa.
            Ex.: "merge", "compress", "pdfjpg", "imgpdf"
        """

        # Inicializar nova lista de arquivos para processar
        self.arquivos = []
        self.tarefa = tarefa

        url = self.base_url + f"/start/{tarefa}"

        # Obter o servidor e o ID da tarefa
        response = self._realizar_request("GET", url).json()
        servidor = response["server"]
        self.tarefa_id = response["task"]

        # Salvar URL do servidor que irá lidar com as requests da tarefa criada
        self.servidor_url = f"https://{servidor}/v1"

    def _adicionar_arquivo(self, arquivo: str) -> None:
        """
        Faz upload do arquivo localizado em 'arquivo' para o servidor

        * Parâmetros

        arquivo:    str
            Caminho para o arquivo
        """

        url = self.servidor_url + "/upload"
        data = {"task": self.tarefa_id}

        with open(arquivo, "rb") as f:
            arquivos = {"file": f}
            response = self._realizar_request(
                "POST", url, data=data, files=arquivos
            ).json()

        self.arquivos.append({
            "server_filename": response["server_filename"],
            "filename": arquivo
        })

    def _processar(self, **kwargs) -> None:
        """
        Executa a última tarefa criada

        * Parâmetro

        kwargs:
            Argumentos necessários para realização de algumas tarefas em específico.
            Atualmente não utilizado em nenhuma implementação.
        """

        url = self.servidor_url + "/process"
        json = {
            "task": self.tarefa_id,
            "tool": self.tarefa,
            "files": self.arquivos
        }
        json.update(kwargs)
        response = self._realizar_request("POST", url, json=json).json()

    def _download(self, arquivo_output: str) -> None:
        """
        Realiza o download do arquivo de output e salva os resultados em 'arquivo_output'.

        * Parâmetro

        arquivo_output: str
            Caminho para o local onde se deseja salvar o arquivo
        """
        
        # Realizar request do arquivo para download
        url = self.servidor_url + f"/download/{self.tarefa_id}"
        response = self._realizar_request("GET", url)

        # Salvar arquivo baixado
        with open(arquivo_output, "wb") as f:
            f.write(response.content)

    def _realizar_request(self, metodo: str, url: str, **kwargs) -> requests.Response:
        """
        Realiza requests e levanta erros HTTP. O parâmetro self.headers é incluído em todas
        as requests.

        * Parametros

        metodo: str
            Método HTTP

        url:    str
            Url do servidor

        kwargs: str
            parâmetros necessários de cada request

        * Retorno
            requests.Response

        * Raise
            requests.exceptions.HTTPError:
                Esse método relançará essa exceção a não ser que a exceção seja resultado 
                do token utilizado ter expirado, caso em que um novo token será solicitado
                e ocorrerá uma nova tentativa de realizar a tarefa solicitada.
        """

        try:
            response = requests.request(metodo, url, headers=self.headers, **kwargs)
            
            # Gera uma exceção HTTPError se o código de status não for 2xx
            response.raise_for_status()      

        except requests.exceptions.HTTPError as e:

            # Status de request não autorizada
            if response.json()["status"] == 401:
                print("Token expirado. Solicitando novo...")
                self._novo_token()
                return self._realizar_request(metodo, url, **kwargs)
                
            print(response.text)
            raise(e)

        return response
    
    def _novo_token(self) -> None:
        """Solicita um novo token para autorizar as requests"""

        url = self.base_url + "/auth"
        data = {"public_key": self.chave_publica}

        response = self._realizar_request("POST", url, data=data).json()
        token = response["token"]
    
        self.headers = {"Authorization": f"Bearer {token}"}


