# jupyterhub-docker

## General Setup
1. Create a Personal Access (https://github.com/settings/tokens)

2. Execute: docker login ghcr.io -u {GITHUB_USERNAME}

3. Password is prompted: Copy and paste token

4. To use a specific docker image built in our github organization as a docker spawner image: docker pull ghcr.io/eth-peach-lab/{GITHUB_REPO}:{TAG/BRANCH}

5. Adapt DOCKER_NOTEBOOK_IMAGE accordingly

6. (Optional) add your username to the [project_config.yml](./project_config.yaml) and / or create new groups. Can also be done later.

## Native Authenticator
Works without any further configuration.


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

## Reference:
Adapted from: 
https://github.com/jupyterhub/oauthenticator/blob/main/examples/full/