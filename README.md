# jupyterhub-docker

## General Setup
1. Create a Personal Access (https://github.com/settings/tokens)

2. Execute: docker login ghcr.io -u {GITHUB_USERNAME}

3. Password is prompted: Copy and paste token

4. To use a specific docker image built in our github organization as a docker spawner image: docker pull ghcr.io/eth-peach-lab/{GITHUB_REPO}:{TAG/BRANCH}. e.g., pull the puzzleme extension image: `docker pull ghcr.io/eth-peach-lab/collaborative-learning-extension-jupyter:VERSION`

5. (Optional) Adapt DOCKER_NOTEBOOK_IMAGE accordingly

6. (Optional) add your username to the groups within [project_config.yml](./project_config.yaml) and / or create new groups. Can also be done later.

## OAuth Authenticator
1. Create a new OAuth Application (Github: https://github.com/settings/applications/new)  
For a local setup:  
    - Homepage URL: http://localhost:8000
    - Authorization callback URL: http://localhost:8000/hub/oauth_callback
2. Create an "env" file in [/oauth](./oauth/) with the following:   
OAUTH_CLIENT_ID={ID}  
OAUTH_CLIENT_SECRET={SECRET}  
OAUTH_CALLBACK_URL={URL}  
Locally the callback url is set to: http://localhost:8000/hub/oauth_callback
3. Add your username to the "admins" file in [/oauth](./oauth/)

## Run JupyterHub
1. (Optional - Step 4 takes care) Build ./Dockerfile by executing: ```docker build --pull --rm  -t jupyterhub-oauth ./oauth```
2. (Optional) Execute the copier ```docker compose -f "./oauth/docker_compose.copier.yml" up -d --build```
3. Make sure the Image: DOCKER_NOTEBOOK_IMAGE is available.
4. Run the fitting docker-compose for jupyter-hub:
    - local: ```docker compose -f "./oauth/docker_compose.local.yml" up -d --build```
    - ETH server: ```docker compose -f "./oauth/docker_compose.yml" up -d --build```

### Copier / testfiles
The Copier container copies the [testfiles folder](./oauth/testfiles/) into a shared named docker volume. 
This volume is then mounted into each users' working directory. Within this
folder users can only edit existing files but not create or delete any documents / directories.




## Reference:
Adapted from: 
https://github.com/jupyterhub/oauthenticator/blob/main/examples/full/