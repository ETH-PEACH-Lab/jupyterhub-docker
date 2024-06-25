# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
import yaml
import sys
import shutil 

with open('/rooms_config.yaml', 'r') as file:
    project_config = yaml.safe_load(file)
from oauthenticator.github import LocalGitHubOAuthenticator

c = get_config()  # noqa: F821
c.JupyterHub.authenticator_class = LocalGitHubOAuthenticator
c.LocalGitHubOAuthenticator.create_system_users = True
c.JupyterHub.admin_users = admin = set()
c.OAuthenticator.allow_all = True
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']

join = os.path.join

here = os.path.dirname(__file__)
root = os.environ.get('OAUTHENTICATOR_DIR', here)
sys.path.insert(0, root)

with open(join(root, 'admins')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        admin.add(parts[0])
            
# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.
# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.NotebookApp.server_extensions = [
    'extension'
]
# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]
c.DockerSpawner.cmd = None
# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = {'network_mode': network_name}

notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

def pre_spawn_hook(spawner):
    spawner.args.append("--LabApp.collaborative=True")
    spawner.volumes['oauth_jupyterhub-testfiles'] = os.path.join(notebook_dir, 'testfiles')

c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir}
c.DockerSpawner.pre_spawn_hook = pre_spawn_hook
c.Spawner.ip = '0.0.0.0'

c.DockerSpawner.ip = c.Spawner.ip
c.Spawner.environment.update({"JUPYTERHUB_SINGLEUSER_APP": "jupyter-server"})
c.DockerSpawner.environment = c.Spawner.environment
c.Spawner.env_keep = [
    'JUPYTER_CONFIG_DIR'
]
c.DockerSpawner.env_keep = c.Spawner.env_keep

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8080

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"

# Authenticate users with Native Authenticator
c.JupyterHub.load_roles = []

c.JupyterHub.load_groups = {
    "collaborative": [],
    "instructors": [],
}
for instructor_name in project_config["instructors"]:
    print(instructor_name)
    c.JupyterHub.load_groups["instructors"].append(instructor_name)

for project_name, project in project_config["rooms"].items():
    # get the members of the room
    members = project.get("members", [])
    # create groups for the project
    members_project_name = f"{project_name}-members"
    instructors_project_name = f"{project_name}-instructors"
    if members is None:
        members = []

    c.JupyterHub.load_groups[members_project_name] = members

    # define a new user for the room
    collab_user = f"{project_name}-room"
    # add the collab user to the 'collaborative' group
    # so we can identify it as a collab account
    c.JupyterHub.load_groups["collaborative"].append(collab_user)

    # finally, grant members of the room
    # access to the collab user's server,
    # and the admin UI so they can start/stop the server
    c.JupyterHub.load_roles.append(
        {
            "name": f"collab-access-{instructors_project_name}",
            "scopes": [
                f"access:servers!user={collab_user}",
                f"admin:servers!user={collab_user}",
                "admin-ui",
                f"list:users!user={collab_user}",
            ],
            "groups": ["instructors"],
        }
    )
    c.JupyterHub.load_roles.append(
        {
            "name": f"collab-access-{members_project_name}",
            "scopes": [
                f"access:servers!user={collab_user}",
                f"admin:servers!user={collab_user}",
                "admin-ui",
                f"list:users!user={collab_user}",
            ],
            "groups": [members_project_name],
        }
    )
