import os

yaml_content = """
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {client_auth_data}
    server: https://{cluster}.k8s.ondigitalocean.com
  name: do-sgp1-{{cookiecutter.project_slug}}
contexts:
- context:
    cluster: do-sgp1-{{cookiecutter.project_slug}}
    user: do-sgp1-{{cookiecutter.project_slug}}-admin
  name: do-sgp1-{{cookiecutter.project_slug}}
current-context: do-sgp1-{{cookiecutter.project_slug}}
kind: Config
users:
- name: do-sgp1-{{cookiecutter.project_slug}}-admin
  user:
    token: {token}
"""

TOKEN = os.environ.get("K8S_TOKEN")
CLUSTER = os.environ.get("K8S_CLUSTER")
AUTH_DATA = os.environ.get("K8S_AUTH_DATA")


def main():
    content = yaml_content.format(
        cluster=CLUSTER, token=TOKEN, client_auth_data=AUTH_DATA
    )
    config = open("kubeconfig", "w")
    config.write(content)
    config.close()


if __name__ == "__main__":
    main()
