# Backend auto deployment using github
---
Here we are going to automate backend deployment using bigga configuration on a remote instance. Setup contains two parts. Please follow the below steps to complete the auto deployment.

## Get Docker Machine Config and SSH Key
Follow:- https://medium.com/@cweinberger/docker-machine-export-and-import-34ae2899e9d7#:~:text=Docker%20Machine%20stores%20the%20configuration,machine%20configuration%20in%20a%20config.

Or 

Get Host, Username, Port and Docker Instance Details
```
$ cd ~/.docker/machine/machines/{machine-name}/
$ cat config.json
```

Get SSH Key
```
$ cd ~/.docker/machine/machines/{machine-name}/
$ cat id_rsa
```

NB: `{machine-name}`is docker machine created using bigga docs.
Above Host, Username, Port and Key are used in Part-2

For `ssh -i /path/<name>.pem username@host` use
`ssh -i /path/id_rsa username@host`. 
If permission issue do `sudo chmod 0400 /path/id_rsa`

### Part-1 : Configure Remote Instance
#### Steps :
  1. SSH to Docker Instance.
  `ssh username@host` or `ssh -i /path/<name>.pem username@host`
  2. Generate multiple SSH keys.
  ```
  $ ssh-keygen -t rsa -f ~/.ssh/id_rsa_backend -q -P ""
  $ ssh-keygen -t rsa -f ~/.ssh/id_rsa_bigga -q -P ""
  ```
  3. Create SSH Config file and open.
  ```
  $ cd ~/.ssh/
  $ touch config
  $ sudo nano config
  ```
  4. Paste this inside config file
  ```
  # backend account
  Host github.com-backend
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_backend

  # bigga account
  Host github.com-bigga
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa_bigga
  ```
  5. Copy generated public keys to Repo > Settings > Deploy keys
  Please make sure that, you should paste keys to specific repo.
  eg:- goto 
  ```
  https://github.com/<username>/backend/settings/keys
  https://github.com/<username>/bigga/settings/keys
  ```
  6. Clone Backend and Bigga
  ```
  $ git clone git@github.com-backend:<username>/backend.git
  $ git clone git@github.com-bigga:<username>/bigga.git
  ```
  NB: Where `github.com-backend` and `github.com-bigga` is SSH Host you added to ~/.ssh/config
  
  7. Setup and Install Docker Compose
  Follow:-
  https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04
  Or
	https://linuxize.com/post/how-to-install-and-use-docker-compose-on-ubuntu-18-04
  Location should be '/usr/local/bin/docker-compose'
  8. Check 'docker-compose' working by cmd
  ```
  $ docker-compose
  ``` 
  9. You are done with Part-1
### Part-2 : Configure GitHub Actions
#### Steps :
  1. Create a new workflow by navigating, Repo > Actions > New Workflow
  Or
  Create 'yaml' or 'yml' deployments inside repo `.github/workflows/`
  2. Copy this to yml file.
  ```
    # This is a basic workflow to help you get started with Actions

    `name: Test Server CI

    # Controls when the action will run. 
    on:
      # Triggers the workflow on push or pull request events but only for the develop branch
      push:
        branches: [ test-deploy ]
      pull_request:
        branches: [ test-deploy ]

      # Allows you to run this workflow manually from the Actions tab
      workflow_dispatch:

    # A workflow run is made up of one or more jobs that can run sequentially or in parallel
    jobs:
      # This workflow contains a single job called "build"
      build:
        # The type of runner that the job will run on
        runs-on: ubuntu-18.04

        # Steps represent a sequence of tasks that will be executed as part of the job
        steps:
          # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
          - uses: actions/checkout@v2

          - name: Executing Build & Deployment Commands Using SSH
            uses: appleboy/ssh-action@master
            with:
              host: ${{ secrets.TEST_HOST }}
              username: ${{ secrets.TEST_USERNAME }}
              key: ${{ secrets.TEST_KEY }}
              port: ${{ secrets.TEST_PORT }}
              script: |
                echo "*** Pull Backend ***"
                cd
                cd backend
                git checkout develop
                git pull origin develop
                
                echo "*** Pull Bigga ***"
                cd
                cd bigga
                git checkout community
                git pull origin community
                cp .env-test .env
                echo "*** Remove Unwanted Containers ***"
                docker system prune -f
                echo "*** Taking Build ***"
                docker-compose build
                echo "*** Deploy Build ***"
                docker-compose up -d`
  ```

  3. Should Add Secrets Keys `https://github.com/<username/<repo>/settings/secrets/actions`
  ie, Repo > Settings > Secrets

  | Key           | Description                                         |
  |:--------------|:----------------------------------------------------|
  | TEST_HOST     | Remote docker instance IP address                   |
  | TEST_USERNAME | Remote docker instance username                     |
  | TEST_PORT     | Remote docker instance port                         |
  | TEST_KEY      | Remote docker instance `private_key` / `.pem key`   |

  4. Change branch name and save
  5. You are done with Part-2.
