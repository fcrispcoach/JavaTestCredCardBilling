import os
import sys
from github import Github, RateLimitExceededException
import boto3
import json
import time

def analyze_code_with_claude(branch_name, repo_url, token):
    try:
        if token:
            g = Github(token)
        else:
            g = Github()  
        
        repo_name = repo_url.split('/')[-1]
        user_name = repo_url.split('/')[-2]
        repo = g.get_user(user_name).get_repo(repo_name)
        branch = repo.get_branch(branch_name)
        files = repo.get_git_tree(branch_name, recursive=True).tree

        code_snippets = []
        for file in files:
            if file.path.endswith('.java'):
                file_content = repo.get_contents(file.path, ref=branch_name)
                code_snippets.append(file_content.decoded_content.decode())

        if not code_snippets:
            print("Nenhum arquivo .java encontrado no repositório.")
            return {}

        prompt = f"""
        Analise o seguinte código Java com base nos seguintes critérios e forneça uma resposta separada para cada um deles:
        1. Pontos críticos na estrutura do código.
        2. Pontos críticos nos testes unitários.
        3. Pontos críticos nos testes de integração.
        4. Se o código segue a arquitetura hexagonal.
        5. A estrutura e a qualidade geral do código.
        6. Se o código está pronto para produção (Sim ou Não).

        Código Java:
        {''.join(code_snippets)}
        """

        client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Log para depuração
        print("Prompt enviado para o Bedrock:")
        print(prompt)

        response = client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1500,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        response_body = response['body'].read().decode('utf-8')
        print("Resposta do Bedrock:", response_body)  

        result = json.loads(response_body)
        messages = result.get('content', [])

        analysis_text = "\n".join([msg.get('text', '') for msg in messages])

        analysis = {
            "branch": branch_name,
            "Pontos críticos na estrutura do código": "",
            "Pontos críticos nos testes unitários": "",
            "Pontos críticos nos testes de integração": "",
            "Se o código segue a arquitetura hexagonal": "",
            "A estrutura e a qualidade geral do código": "",
            "Se o código está pronto para produção": "",
            "Deploy produção": ""
        }

        lines = analysis_text.split('\n')
        current_key = None

        for line in lines:
            line = line.strip()
            if line.startswith('1. '):
                current_key = "Pontos críticos na estrutura do código"
                analysis[current_key] = line[3:].strip()
            elif line.startswith('2. '):
                current_key = "Pontos críticos nos testes unitários"
                analysis[current_key] = line[3:].strip()
            elif line.startswith('3. '):
                current_key = "Pontos críticos nos testes de integração"
                analysis[current_key] = line[3:].strip()
            elif line.startswith('4. '):
                current_key = "Se o código segue a arquitetura hexagonal"
                analysis[current_key] = line[3:].strip()
            elif line.startswith('5. '):
                current_key = "A estrutura e a qualidade geral do código"
                analysis[current_key] = line[3:].strip()
            elif line.startswith('6. '):
                current_key = "Se o código está pronto para produção"
                analysis[current_key] = line[3:].strip()

                if "não" in line.lower() or "não está completamente pronto" in line.lower():
                    analysis["Deploy produção"] = "Não"
                else:
                    analysis["Deploy produção"] = "Sim"
            elif current_key:
                analysis[current_key] += ' ' + line.strip()

        for key in analysis:
            analysis[key] = analysis[key].strip()

        return analysis

    except Exception as e:
        print(f"Erro durante a análise do código: {str(e)}")
        return {}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python scripts/analyze_with_bedrock.py <repositório> <branch>")
        sys.exit(1)

    repository = sys.argv[1]  # Formato: owner/repo
    branch_name = sys.argv[2]
    repo_url = f"https://github.com/{repository}"
    token = os.getenv('GITHUB_TOKEN')

    # Verifique se as credenciais da AWS estão disponíveis
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    print(f"Repo URL: {repo_url}")
    print(f"AWS Access Key ID: {'****' if aws_access_key_id else 'Not found'}")
    print(f"AWS Secret Access Key: {'****' if aws_secret_access_key else 'Not found'}")

    analysis = analyze_code_with_claude(branch_name, repo_url, token)
    print(json.dumps(analysis, indent=4))
