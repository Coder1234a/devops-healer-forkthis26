# autonomous devops healer

listen up. here is the rundown of how this repository is structured and how you need to run it. read this carefully so we are all on the same page and you accidentally don't break the environment on your first try.

### overview

we are working with a closed loop system that has two main parts.

1. the sandbox. inside the `sandbox/` directory is a standard python microservice and a postgres database. it will definitively crash when it tries to build and deploy.

2. the autonomous agent. this is your main focus. the healer agent python script runs a local server that listens for a pipeline failure signal. when it receives one, it reads the error logs, asks an llm for the correct code patch, and automatically pushes a new git branch to fix the repository.

your job is to plug your actual api key into the agent, start the server, and send a manual failure signal to watch it execute the repair loop.

### execution instructions

when you are ready to test the loop, open your terminal and run these commands exactly as written below.

step 1. install the required python packages to your local environment.

```bash
pip install -r requirements.txt
```

step 2. start the autonomous agent server. it will spin up on your local machine and sit idle waiting for the webhook trigger.

```bash
python healer_agent.py
```

step 3. leave that server running and open a second terminal window. you now need to simulate gitlab telling the agent that the pipeline failed. use this curl command to fire the webhook payload directly at the agent.

```bash
curl -X POST http://localhost:8000/webhook -H "Content-Type: application/json" -d '{"build_status": "failed", "build_id": "test_job_001"}'
```

once you run that last command, check your first terminal window. you will see the agent wake up, analyze the fake trace logs, generate a patch payload, and create a new git branch in your local repository. 

### repository push instructions

when you are ready to push your finalized code to your remote repository, run the following commands sequentially from the root directory. 

remember, we need to ensure git tracks our empty infrastructure folders, so we touch a dummy gitkeep file first.

```bash
touch sandbox/infrastructure-templates/.gitkeep
git init
git add .
git commit -m "initial commit of the autonomous devops agent and sandbox"
git branch -M main
git remote add origin <your_repository_url_here>
git push -u origin main
```

if you run into issues, double check that you actually inserted your llm api key in the python script. good luck.